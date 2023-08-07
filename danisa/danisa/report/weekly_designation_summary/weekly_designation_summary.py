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
	
	date_list = []
	current_date = from_date
	while current_date <= to_date:
		date_list.append(current_date)
		current_date += timedelta(days=1)
	columns, data = [], []
	conditions = get_conditions(filters)
	columns = get_columns(date_list)
	data = get_results(filters,date_list,conditions)
	return columns, data


def get_conditions(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND shift = %(shift)s " if filters.get("shift") else ""
	conds += " AND employee_group = %(employee_group)s " if filters.get("employee_group") else ""
	conds += " AND attendance_date between %(from_date)s AND %(to_date)s " if filters.get("from_date") and filters.get("to_date") else ""
	return conds

def get_columns(date_list):
	columns = [ _("Designation Name") + "::190"]
	for day in date_list:
		columns.append(day.strftime("%a") + "::70")
	columns += [_("Total Shifts") +":Int:80",_("Rate") + ":Currency:95",_("Amount") + ":Currency:95"]
	return columns

def get_results(filters,date_list,conds):
	company = filters.get("company")
	designations = frappe.db.get_list("Designation")
	data = []
	for designation in designations:
		total_shifts = 0
		if frappe.db.sql(f"select name from `tabAttendance` where docstatus = 1 {conds}  and designation = '{designation.name}'",filters):
			row = [designation.name]
			for date in date_list:
				query = f"""select count(*) as total from `tabAttendance` WHERE docstatus = 1 {conds} and attendance_date = '{date}' and designation = '{designation.name}'"""
				count = frappe.db.sql(query,filters,as_dict=1)[0]
				row.append(count.total)
				total_shifts += count.total
			row.append(total_shifts)
			amount = frappe.db.get_value("Designation",designation.name, "amount_per_shift")
			row.append(amount if amount else 0)
			if amount:
				total_amount = total_shifts * float(amount)
			else:
				total_amount = total_shifts * 0
			row.append(total_amount)
			data.append(row)
	return data
