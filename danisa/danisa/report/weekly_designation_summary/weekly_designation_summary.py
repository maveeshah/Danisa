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
	data = get_results(filters,date_list)

	return columns, data


def get_conditions(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND designation = %(designation)s " if filters.get("designation") else ""
	conds += " AND attendance_date between %(from_date)s AND %(to_date)s " if filters.get("from_date") and filters.get("to_date") else ""
	return conds

def get_columns(date_list):
	columns = [ _("Designation Name") + "::190"]
	for day in date_list:
		columns.append(day.strftime("%a") + "::70")
	columns += [_("Total Shifts") +":Int:80",_("Rate") + ":Currency:95",_("Amount") + ":Currency:95"]
	return columns

def get_results(filters,date_list):
	company = filters.get("company")
	designations = frappe.db.get_list("Designation",{"company":company})
	data = []
	for designation in designations:
		total_shifts = 0
		row = [designation.name]
		for date in date_list:
			if frappe.db.exists("Attendance",{"attendance_date":date,"designation":designation.name,"company":company}):
				count =	frappe.db.count("Attendance",filters={"attendance_date":date,"designation":designation.name,"company":company},debug=False)
				if count:
					row.append(count)
					total_shifts += count
			else:
				row.append(0)
		row.append(total_shifts)
		amount = frappe.db.get_value("Designation",designation.name, "amount_per_shift")
		row.append(amount if amount else 0)
		total_amount = total_shifts * amount
		row.append(total_amount)
		data.append(row)
	return data
