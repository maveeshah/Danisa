# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MultiAttendanceTool(Document):

	@frappe.whitelist()
	def get_emp_list(self):
		ret_list = []
		query = f"""SELECT name,employee_name,id_number
					FROM `tabEmployee`
					WHERE company = '{self.company}'
					"""
		employees = frappe.db.sql(query,as_dict=1)
		# if self.employee_group or self.shift or self.designation:
		# 	conds = ""
		# 	conds += " AND employee_group = %(employee_group)s " if self.employee_group else ""
		# 	conds += " AND shift = %(shift)s " if self.shift else ""
		# 	conds += " AND designation = %(designation)s " if self.designation else ""
		# 	conds += " AND company = %(company)s " if self.company else ""
		# 	filtered_employees = frappe.db.sql(f"""SELECT DISTINCT(employee),employee,name,id_number
		# 		     								FROM `tabAttendance` 
		# 		     								WHERE docstatus = 1 
		# 		     								{conds}""",as_dict=1)[0]
		# 	if filtered_employees:
		# 		for emp in filtered_employees:
		# 			ret_list.append(emp)
		# return ret_list if ret_list else employees
		return employees if employees else []
	@frappe.whitelist()
	def mark_attendance(self):
		if self.employees:
			for employee in self.employees:
				attendance_to_be_marked = frappe.new_doc("Attendance")
				attendance_to_be_marked.employee = employee.employee
				attendance_to_be_marked.employee_name = employee.employee_name
				attendance_to_be_marked.status = self.status
				attendance_to_be_marked.id_number = employee.id_number
				attendance_to_be_marked.designation = self.attendance_designation
				attendance_to_be_marked.shift = self.attendance_shift
				attendance_to_be_marked.attendance_date = self.attendance_date
				attendance_to_be_marked.company = self.company
				attendance_to_be_marked.amount = self.attendance_amount
				attendance_to_be_marked.amount_paid = self.attendance_amount_paid
				attendance_to_be_marked.save(ignore_permissions=True)
				attendance_to_be_marked.submit()
			return "Success"
		return "Failure"
