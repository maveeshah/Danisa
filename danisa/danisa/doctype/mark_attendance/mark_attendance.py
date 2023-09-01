# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MarkAttendance(Document):
	def on_submit(self):
		if self.add_employee:
			approver = frappe.db.get_value("User",frappe.session.user,"first_name")
			for employee in self.add_employee:
				attendance_to_be_marked = frappe.new_doc("Attendance")
				attendance_to_be_marked.employee = employee.name_series
				attendance_to_be_marked.employee_name = employee.employee_name
				attendance_to_be_marked.status = self.status
				attendance_to_be_marked.id_number = employee.id_number
				attendance_to_be_marked.department = self.department_name
				attendance_to_be_marked.employee_group = self.employee_group
				attendance_to_be_marked.place_of_work = employee.place_of_work
				attendance_to_be_marked.phone_no = employee.cell_number
				attendance_to_be_marked.designation = self.designation
				attendance_to_be_marked.shift = self.shift
				attendance_to_be_marked.attendance_date = self.attendance_date
				attendance_to_be_marked.company = self.company
				attendance_to_be_marked.in_time = self.in_time
				attendance_to_be_marked.out_time = self.out_time
				attendance_to_be_marked.amount = self.amount
				attendance_to_be_marked.pay_rate_ = self.pay_rate
				attendance_to_be_marked.amount_paid = self.amount_paid
				attendance_to_be_marked.approver_name = approver
				attendance_to_be_marked.mark_attendance_link = self.name
				attendance_to_be_marked.save(ignore_permissions=True)
				attendance_to_be_marked.submit()

	# def on_cancel(self):
	# 	# Find and cancel associated Attendance records
	# 	attendances_to_cancel = frappe.get_all(
	# 		"Attendance",
	# 		filters={"mark_attendance_link": self.name, "docstatus": 1},
	# 		fields=["name"]
	# 	)
	# 	for attendance in attendances_to_cancel:
	# 		frappe.db.set_value("Attendance", attendance.name, "workflow_state", "Discarded")
	# 		# attendance_doc = frappe.get_doc("Attendance", attendance.name)
	# 		# attendance_doc.cancel()

	# def on_trash(self):
	# 	# Delete associated Attendance records
	# 	attendances_to_delete = frappe.get_all(
	# 		"Attendance",
	# 		filters={"mark_attendance_link": self.name},
	# 		fields=["name"]
	# 	)
	# 	for attendance in attendances_to_delete:
	# 		frappe.delete_doc("Attendance", attendance.name, ignore_permissions=True)


@frappe.whitelist()
def get_parent_field(child_name):
    child_doc = frappe.get_doc("Employee Names", child_name)
    parent_doc = frappe.get_doc("Mark Attendance", child_doc.parent)
    parent_field_value = parent_doc.company
    return parent_field_value

