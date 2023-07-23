# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}
	columns, data = [], []
	conditions = get_conditions(filters)
	columns = get_columns()
	data = get_results(filters,conditions)

	return columns, data


def get_conditions(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND attendance_date = %(attendance_date)s " if filters.get("attendance_date") else ""
	return conds

def get_columns():
	return  [ _("Employee Name") + "::190", _("ID. No.") + "::150",_("Shift") + "::150",_("Place of Work") + "::150",_("Time In") + "::150",_("Time Out") + "::150"]
	

def get_results(filters,conditions):
	query = """
		SELECT employee_name, id_number, shift, place_of_work,
			in_time, out_time
		FROM `tabAttendance`
		WHERE docstatus = 1 {0}
	""".format(conditions)

	return frappe.db.sql(query, filters)
