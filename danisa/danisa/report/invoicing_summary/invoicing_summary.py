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
	shifts = frappe.db.get_list("Attendance",fields=['shift'])
	set_shift = set(shifts)
	shifts = list([shift for shift in shifts])
	columns = get_columns(shifts)
	conds = get_conds(filters)
	data = get_data(filters,shifts,conds,date_list)
	return columns, data


def get_conds(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get('company') else ""
	conds += " AND attendance_date between %(from_date)s and %(to_date)s " if filters.get('from_date') and filters.get('to_date') else ""
	conds += " AND employee_group = %(employee_group)s " if filters.get('employee_group') else ""
	# conds += " AND department = %(department)s " if filters.get('department') else ""
	conds += " AND designation = %(designation)s " if filters.get('designation') else ""
	return conds

def get_columns(shifts):
	columns = [ _("Employee Name") + "::190",_("ID No.") + "::190",_("Phone No") + "::190"]
	for shift in shifts:
		columns += [_(f"{shift} Head Count") + ":Int:95",_(f"{shift} Overtime Hrs") + ":Int:95"]
	columns += [_("Total Head Count") + ":Int:95",_("Total Overtime Hrs") + ":Int:95"]
	columns += [_("Amount Head Count") + ":Currency:95",
	     			_("Amount Overtime Hrs") + ":Currency:95",
	     			_("Amount Management Fee") + ":Currency:95",
	     			_("Total Amount") + ":Currency:95"]
	return columns

def get_data(filters,shifts,conds,date_list):
	data = []
	for date in date_list:
		row = [date,date.strftime("%A")]
		for shift in shifts:
			query = """
						SELECT count(*) as total
							sum(CASE 
								WHEN ADDTIME(TIMEDIFF(TIME(out_time), TIME(in_time)), '-08:00:00') < '00:00:00' 
								THEN '00' 
								ELSE SUBSTRING(ADDTIME(TIMEDIFF(TIME(out_time), TIME(in_time)), '-08:00:00'), 1,2)
							END) AS overtime
						FROM `tabAttendance`
						WHERE docstatus = 1
						status = 'Present'
						shift = '{1}' {0}
			""".format(conds,shift,filters)			
			res = frappe.db.sql(query, filters)
			frappe.throw(frappe.as_json(res))