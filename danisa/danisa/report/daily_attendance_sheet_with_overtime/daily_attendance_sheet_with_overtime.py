# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}
	columns, data = [], []
	# att = frappe.db.sql("""SELECT name,designation 
	# 	     FROM `tabAttendance` 
	# 	     WHERE docstatus = 1 
	# 	     AND status = 'Present' 
	# 	     and designation is not null """,as_dict=1)
	# for attendance in att:
	# 	res_time = frappe.db.get_value("Designation",attendance.designation,"rest_time")
	# 	if res_time:
	# 		frappe.db.update("Attendance",attendance.name,"rest_time",res_time)
	# 	else:
	# 		frappe.db.update("Attendance",attendance.name,"rest_time",0)


	conditions = get_conditions(filters)
	columns = get_columns()
	data = get_results(filters,conditions)

	return columns, data


def get_conditions(filters):
	conds = ""
	conds += " AND company = %(company)s " if filters.get("company") else ""
	conds += " AND attendance_date = %(attendance_date)s " if filters.get("attendance_date") else ""
	conds += " AND designation = %(designation)s " if filters.get("designation") else ""
	conds += " AND department = %(department)s " if filters.get("department") else ""
	conds += " AND employee_group	 = %(employee_group)s " if filters.get("employee_group") else ""
	return conds

def get_columns():
	return  [ _("Employee Name") + "::190", _("ID. No.") + "::150",_("Shift") + "::150",_("Place of Work") + "::150",_("Time In") + "::150",_("Time Out") + "::150",_("Overtime") + "::150"]
	

def get_results(filters,conditions):

	# query = """
	# 		SELECT 
	# 			employee_name, 
	# 			id_number, 
	# 			shift, 
	# 			place_of_work,
	# 			SUBSTRING(time(in_time), 1, 5) AS in_time, 
	# 			SUBSTRING(time(out_time), 1, 5) AS out_time,
	# 			CASE 
	# 				WHEN ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00') < '00:00:00' THEN '0'
	# 				ELSE 
	# 					FORMAT(
	# 						FLOOR(
	# 							TIME_TO_SEC(
	# 								ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
	# 							) / 3600
	# 						) + 
	# 						FLOOR(
	# 							MOD(
	# 								TIME_TO_SEC(
	# 									ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
	# 								),
	# 								3600
	# 							) / 1800
	# 						) * 0.5 +
	# 						FLOOR(
	# 							MOD(
	# 								TIME_TO_SEC(
	# 									ADDTIME(TIMEDIFF(out_time, in_time), '-08:00:00')
	# 								),
	# 								1800
	# 							) / 900
	# 						) * 0.25,
	# 						2
	# 					)
	# 			END AS overtime
	# 		FROM `tabAttendance`
	# 		WHERE docstatus = 1 {0}
	# """.format(conditions,filters)

	query = """
			SELECT 
				employee_name, 
				id_number, 
				shift, 
				place_of_work,
				SUBSTRING(time(in_time), 1, 5) AS in_time, 
				SUBSTRING(time(out_time), 1, 5) AS out_time,
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
				END AS overtime
			FROM `tabAttendance`
			WHERE docstatus = 1 {0}
	""".format(conditions,filters)
	data = []
	results = frappe.db.sql(query, filters)
	total_ot = 0.00
	for row in results:
		total_ot += float(row[-1])
		data.append(row)
	row_end = ['Total','','','','','',total_ot]
	data.append(row_end)
	return data
