# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}
	columns, data = [], []
	conditions = get_conditions(filters)
	data = get_data(conditions,filters)
	columns = get_columns()
	return columns, data


def get_conditions(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND attendance_date = %(date)s " if filters.get("date") else ""
	conds += " AND designation = %(designation)s " if filters.get("designation") else ""
	conds += " AND employee_group = %(employee_group)s " if filters.get("employee_group") else ""
	return conds

def get_data(conditions,filters):
	query = f"""SELECT employee_name, id_number, shift,
				amount_paid
				FROM `tabAttendance`
				WHERE docstatus = 1 {conditions}
				"""
	data = frappe.db.sql(query,filters)
	return data


def get_columns():
	return [ _("Employee Name") + "::190",
	 			_("ID. No.") + "::150",
	     _("Shift") + "::115",
		 _("Amount Paid") + "::150",]