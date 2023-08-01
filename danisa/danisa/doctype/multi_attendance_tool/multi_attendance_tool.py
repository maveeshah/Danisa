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
		if self.employee_group or self.shift or self.designation:
			filtered_employees = frappe.db.sql(f"""SELECT DISTINCT(employee),employee,name,id_number
				     								FROM `tabAttendance` 
				     								WHERE docstatus = 1 
				     								AND designation = f'{self.designation}'""",as_dict=1)[0]
			if filtered_employees:
				for emp in filtered_employees:
					ret_list.append(emp)
		return ret_list if ret_list else employees
	
	@frappe.whitelist()
	def mark_attendance(self):
		if self.employees:
			for employee in self.employees:
				attendance_to_be_marked = frappe.new_doc("Attendance")
				attendance_to_be_marked.employee = employee.employee
				attendance_to_be_marked.employee_name = employee.employee_name
				attendance_to_be_marked.status = employee.status
				attendance_to_be_marked.id_number = employee.id_number
				attendance_to_be_marked.designation = employee.designation
				attendance_to_be_marked.shift = employee.shift
				attendance_to_be_marked.attendance_date = self.attendance_date
				attendance_to_be_marked.company = self.company
				attendance_to_be_marked.save(ignore_permissions=True)
				attendance_to_be_marked.submit()
			return "Success"
		return "Failure"
