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
	conds += " AND date = %(date)s " if filters.get("date") else ""
	conds += " AND to = %(to)s " if filters.get("to") else ""
	conds += " AND area_assigned = %(area_assigned)s " if filters.get("area_assigned") else ""
	return conds

def get_data(conditions,filters):
	query = f"""SELECT task_or_services_required, no_of_casuals, from as from_to, to as no_to
				FROM `tabTask or Services Required`
				WHERE parent in (
					SELECT name 
					FROM `tabLabour Requisition Form`
					WHERE docstatus = 1 {conditions}
					)
				ORDER BY parent
				"""
	data = frappe.db.sql(query,filters)
	return data


def get_columns():
	return [ _("Task or Services Required") + "::190",
	 			_("No. of Casuals") + "::150",
	     _("From") + "::115",
		 _("To") + "::150",]