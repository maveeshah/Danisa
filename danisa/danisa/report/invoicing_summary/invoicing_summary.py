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
	cond_shift = ""
	cond_shift += " and company = %(company)s " if filters.get("company") else ""
	cond_shift += " and employee_group = %(employee_group)s " if filters.get("employee_group") else ""
	shift_query = f"""SELECT name as shift 
					FROM `tabShift Type` 
					WHERE docstatus < 2
					{cond_shift} """
	shifts = frappe.db.sql(shift_query,filters)
	if not shifts:
		return columns, data

	shifts = [shift[0] for shift in shifts]
	columns = get_columns(shifts)
	conds = get_conds(filters)
	data = get_data(filters,shifts,conds,date_list)
	return columns, data


def get_conds(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get('company') else ""
	conds += " AND attendance_date between %(from_date)s and %(to_date)s " if filters.get('from_date') and filters.get('to_date') else ""
	conds += " AND employee_group = %(employee_group)s " if filters.get('employee_group') else ""
	conds += " AND department = %(department)s " if filters.get('department') else ""
	conds += " AND designation = %(designation)s " if filters.get('designation') else ""
	return conds

def get_columns(shifts):
	columns = [ _("Date") + ":Date:135",_("Day") + "::135"]
	for shift in shifts:
		columns += [_(f"{shift} Head Count") + ":Int:135",_(f"{shift} Overtime Hrs") + ":Int:135"]
	columns += [_("Total Head Count") + ":Int:135",_("Total Overtime Hrs") + ":Int:135"]
	columns += [_("Amount Head Count") + ":Currency:135",
	     			_("Amount Overtime Hrs") + ":Currency:135",
	     			_("Amount Management Fee") + ":Currency:135",
	     			_("Total Amount") + ":Currency:135"]
	return columns

def get_data(filters,shifts,conds,date_list):
	data = []
	for date in date_list:
		row = [date,date.strftime("%A")]
		for shift in shifts:
			query = """
						SELECT count(*) as total,
							IFNULL(SUM(
								CASE 
									WHEN ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00') < '00:00:00' THEN '0'
									ELSE 
										FORMAT(
											FLOOR(
												TIME_TO_SEC(
													ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
												) / 3600
											) + 
											FLOOR(
												MOD(
													TIME_TO_SEC(
														ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
													),
													3600
												) / 1800
											) * 0.5 +
											FLOOR(
												MOD(
													TIME_TO_SEC(
														ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
													),
													1800
												) / 900
											) * 0.25
											- rest_time,
											2
										)
								END
							),0) AS overtime
						FROM `tabAttendance`
						WHERE docstatus = 1 AND
						status = 'Present' AND
						shift = '{1}' AND
						attendance_date = '{2}'
						{0}""".format(conds,shift,date,filters)
			res = frappe.db.sql(query, filters,as_dict=1)[0]
			row.append(res.total)
			row.append(res.overtime)
		# SELECT count(*) as total,
		# 				SUM(CASE 
		# 					WHEN ADDTIME(TIMEDIFF(TIME(out_time), TIME(in_time)), '-08:00:00') < '00:00:00' 
		# 					THEN '00' 
		# 					ELSE SUBSTRING(ADDTIME(TIMEDIFF(TIME(out_time), TIME(in_time)), '-08:00:00'), 1,2)
		# 				END) AS overtime
		# 			FROM `tabAttendance`
		# 			WHERE docstatus = 1 AND
		# 			status = 'Present' AND
		# 			attendance_date = '{2}'
		query = """SELECT count(*) as total,
					IFNULL(SUM(
						CASE 
							WHEN ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00') < '00:00:00' THEN '0'
							ELSE 
								FORMAT(
									FLOOR(
										TIME_TO_SEC(
											ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
										) / 3600
									) + 
									FLOOR(
										MOD(
											TIME_TO_SEC(
												ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
											),
											3600
										) / 1800
									) * 0.5 +
									FLOOR(
										MOD(
											TIME_TO_SEC(
												ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
											),
											1800
										) / 900
									) * 0.25
									- rest_time,
									2
								)
						END
					),0) AS overtime
					FROM `tabAttendance`
					WHERE docstatus = 1 AND
					status = 'Present' AND
					attendance_date = '{2}'
					{0}""".format(conds,shift,date,filters)
		total_res = frappe.db.sql(query, filters,as_dict=1)[0]
		row.append(total_res.total)
		row.append(total_res.overtime)
		rates = frappe.db.get_list("Designation",filters={"name":filters.get("designation")},fields=["normal_rate","overtime_rate","management_fee"])
		normal_rate = overtime_rate = management_fee = 0
		if rates[0].normal_rate:
			normal_rate = rates[0].normal_rate
		if rates[0].overtime_rate:
			overtime_rate = rates[0].overtime_rate
		if rates[0].management_fee:
			management_fee = rates[0].management_fee
		total_amount_of_heads = float(total_res.total) * float(normal_rate)
		total_amount_of_overtime = float(total_res.overtime) * float(overtime_rate)
		total_management_amount = float(total_res.total) * float(management_fee)
		row.append(total_amount_of_heads)
		row.append(total_amount_of_overtime)
		row.append(total_management_amount)
		row.append(total_management_amount + total_amount_of_heads + total_amount_of_overtime)
		data.append(row)
	return data
