# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from datetime import timedelta


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
	data = get_data(conditions,filters,date_list)
	columns = get_columns(date_list)
	frappe.msgprint(frappe.as_json(data))
	frappe.msgprint(frappe.as_json(columns))
	return columns, data


def get_conditions(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND date between %(from_date)s and %(to_date)s " if filters.get("from_date") and filters.get("to_date") else ""
	conds += " AND shift = %(shift)s " if filters.get("shift") else ""
	conds += " AND operation = %(operation)s " if filters.get("operation") else ""
	conds += " AND godown = %(godown)s " if filters.get("godown") else ""
	
	return conds

def get_data(conditions,filters,date_list):
	commodities = frappe.db.get_list("Commodity Type")
	data = []
	for commodity in commodities:
		total = 0
		query = f"""SELECT name
					FROM `tabOperations`
					WHERE parent in (
						SELECT name 
						FROM `tabCargo Handling`
						WHERE docstatus = 1 {conditions} 
						and commodity_type = '{commodity.name}'
						)
					ORDER BY parent
					"""
		res = frappe.db.sql(query,filters)
		if res:
			row = [commodity.name]
			for date in date_list:
				query = f"""select ifnull(sum(no_of_bagsbales),0) as total 
							from `tabOperations` 
							WHERE parent in (
								SELECT name 
								FROM `tabCargo Handling`
								WHERE docstatus = 1 {conditions}
								and date = '{date}'
								and commodity_type = '{commodity.name}'
								)"""
				count = frappe.db.sql(query,filters,as_dict=1)[0]
				frappe.msgprint(frappe.as_json(date))
				frappe.msgprint(frappe.as_json(count))
				row.append(count.total)
				total += count.total
			row.append(total)
			amount = frappe.db.get_value("Commodity Type",commodity.name, "rate")
			row.append(amount if amount else 0)
			if amount:
				total_amount = total * float(amount)
			else:
				total_amount = total * 0
			row.append(total_amount)
			data.append(row)


	return data


def get_columns(date_list):
	columns =  [_("Commodity Type") + ":Link/Commodity Type:150",]
	for day in date_list:
		columns.append(day.strftime("%a") + "::70")
	columns += [_("Total Bags/Bales") +":Int:80",_("Rate") + ":Currency:95",_("Amount") + ":Currency:95"]
	return columns	