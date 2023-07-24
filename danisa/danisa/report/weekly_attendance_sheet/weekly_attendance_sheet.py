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
	columns = get_columns(date_list)
	conds = get_conds(filters)
	data = get_results(filters,date_list,conds)
	return columns, data


def get_columns(date_list):
	columns = [ _("Employee Name") + "::190", _("ID. No.") + "::150",_(" Attendance Date") + ":Date:115",
	     _(" Shift") + ":Link/Shift Type:115",_(" Place of Work") + "::150",
		_(" Time In") + "::150",_(" Time Out") + "::150"]
	return columns

def get_conds(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND attendance_date between %(from_date)s and %(to_date)s " if filters.get("from_date") and filters.get("to_date") else ""
	conds += " AND designation = %(designation)s " if filters.get("designation") else ""
	return conds

def get_results(filters,date_list,conds):
	query = f"""select employee_name,id_number, attendance_date, shift, place_of_work, ifnull(in_time,'Not Marked') as in_time,
				ifnull(out_time, 'Not Marked') as out_time from tabAttendance 
				where docstatus = 1 {conds} order by attendance_date, employee"""
	data = frappe.db.sql(query,filters)
	return data
