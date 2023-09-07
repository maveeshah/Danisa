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
	conds += " AND shift = %(shift)s " if filters.get("shift") else ""
	conds += "AND commodity_type = %(commodity_type)s " if filters.get("commodity_type") else ""
	return conds

def get_data(conditions,filters):
	query = f"""SELECT truck_no, delivery_no, operation, no_of_bagsbales,
				commodity, (SELECT godown_or__shed_no FROM `tabCargo Handling` WHERE name = `tabOperations`.parent) client
				FROM `tabOperations`
				WHERE parent in (
					SELECT name 
					FROM `tabCargo Handling`
					WHERE docstatus = 1 {conditions}
					)
				ORDER BY parent
				"""
	data = frappe.db.sql(query,filters)
	return data


def get_columns():
	return [ _("Truck No.") + "::190",
	 			_("Delivery. No.") + "::150",
	     _("No. of Bags/Bales") + "::115",
		 _("Commodity") + "::150",
		_(" Client") + "::150",]