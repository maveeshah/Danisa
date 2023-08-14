# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from datetime import timedelta
from frappe import _



def execute(filters=None):
	if not filters:
		filters = {}
	from_date = getdate(filters.get("from_date"))
	to_date = getdate(filters.get("to_date"))
	att = frappe.db.get_list("Attendance",filters={"designation":"Terminal B"},fields=["name"])
	for i in att:
		rate = frappe.db.get_value("Designation","Terminal B","pay_rate")
		frappe.db.sql(f"update `tabAttendance` set pay_rate_ = {rate} where name = '{i.name}'")	
	date_list = []
	current_date = from_date
	while current_date <= to_date:
		date_list.append(current_date)
		current_date += timedelta(days=1)

	columns, data = [], []
	columns = get_columns(date_list)
	conds = get_conds(filters)
	data = get_results(filters,date_list,conds)
	return columns, data


def get_conds(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND designation = %(designation)s " if filters.get("designation") else ""
	conds += " AND employee_group = %(employee_group)s " if filters.get("employee_group") else ""
	conds += " AND attendance_date between %(from_date)s AND %(to_date)s " if filters.get("from_date") and filters.get("to_date") else ""
	return conds


def get_columns(date_list):
	columns = [ _("Employee Name") + "::190", _("ID. No.") + "::150",_("Phone No") + "::150"]
	for day in date_list:
		columns.append(day.strftime("%a") + "::70")
	columns += [_("Total Shifts") +":Int:80",_("Amount") + ":Currency:95"]
	return columns

def get_results(filters,date_list,conds):
	att_map = get_attendance_list(conds, filters)
	emp_map = get_employee_details(filters)
	data = []
	for emp in sorted(att_map):
		amount = total_shifts = 0
		emp_det = emp_map.get(emp)
		if not emp_det:
			continue
		row = [emp_det.employee_name, emp_det.id_number, emp_det.cell_number]
		for date in date_list:
			status = att_map.get(emp).get(date, ["None"])
			if  status[0] == "Present":
				counts = frappe.db.sql(f"""SELECT count(*)as total,  sum(ifnull(pay_rate_,0)) as amount FROM `tabAttendance` WHERE attendance_date = '{date}' 
			   								AND employee = '{emp_det.name}'
											AND docstatus = 1 and status = 'Present'
											{conds} """,filters,as_dict=1)[0]
				row.append(counts.total)
				amount += counts.amount
				total_shifts += counts.total
			else:
				row.append(0)
		row.append(total_shifts)
		row.append(amount)	
		data.append(row)
	return data
			 
def get_attendance_list(conditions, filters):
	attendance_list = frappe.db.sql("""select employee, attendance_date as day_of_month,
		amount,	status, designation from tabAttendance 
		where docstatus = 1 %s order by employee, attendance_date""" % conditions, filters, as_dict=1)

	att_map = {}
	for d in attendance_list:
		att_map.setdefault(d.employee, frappe._dict()).setdefault(d.day_of_month, "")
		att_map[d.employee][d.day_of_month] = [d.status,d.designation]

	return att_map

def get_employee_details(filters):
	emp_conds = " "
	emp_map = frappe._dict()
	for d in frappe.db.sql("""select name, employee_name, branch, id_number,cell_number,company,
		designation from tabEmployee where status = 'Active' %s """  % emp_conds, filters, as_dict=1):
		emp_map.setdefault(d.name, d)

	return emp_map

