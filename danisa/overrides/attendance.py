
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	cint,
	cstr,
	format_date,
	get_datetime,
	get_link_to_form,
	getdate,
	nowdate,
)

from hrms.hr.doctype.shift_assignment.shift_assignment import has_overlapping_timings
from hrms.hr.utils import get_holiday_dates_for_employee, validate_active_employee


class DuplicateAttendanceError(frappe.ValidationError):
	pass


class OverlappingShiftAttendanceError(frappe.ValidationError):
	pass


class Attendance(Document):
	def validate_duplicate_record(self):
		duplicate = self.get_duplicate_attendance_record()

		if duplicate:
			frappe.throw(
				_("Attendance for employee {0} is already marked for the date {1}: {2}").format(
					frappe.bold(self.employee),
					frappe.bold(format_date(self.attendance_date)),
					get_link_to_form("Attendance", duplicate),
				),
				title=_("Duplicate Attendance"),
				exc=DuplicateAttendanceError,
			)

	def get_duplicate_attendance_record(self) -> str | None:
		Attendance = frappe.qb.DocType("Attendance")
		query = (
			frappe.qb.from_(Attendance)
			.select(Attendance.name)
			.where(
				(Attendance.employee == self.employee)
				& (Attendance.docstatus < 2)
				& (Attendance.attendance_date == self.attendance_date)
				& (Attendance.designation == self.designation)
				& (Attendance.name != self.name)
			)
		)

		if self.shift:
			query = query.where(
				((Attendance.shift.isnull()) | (Attendance.shift == ""))
				| (
					((Attendance.shift.isnotnull()) | (Attendance.shift != "")) & (Attendance.shift == self.shift)
				)
			)

		duplicate = query.run(pluck=True)

		return duplicate[0] if duplicate else None

	def validate_overlapping_shift_attendance(self):
		attendance = self.get_overlapping_shift_attendance()

		if attendance:
			frappe.throw(
				_("Attendance for employee {0} is already marked for an overlapping shift {1}: {2}").format(
					frappe.bold(self.employee),
					frappe.bold(attendance.shift),
					get_link_to_form("Attendance", attendance.name),
				),
				title=_("Overlapping Shift Attendance"),
				exc=OverlappingShiftAttendanceError,
			)

	def get_overlapping_shift_attendance(self) -> dict:
		if not self.shift:
			return {}

		Attendance = frappe.qb.DocType("Attendance")
		same_date_attendance = (
			frappe.qb.from_(Attendance)
			.select(Attendance.name, Attendance.shift)
			.where(
				(Attendance.employee == self.employee)
				& (Attendance.docstatus < 2)
				& (Attendance.attendance_date == self.attendance_date)
				& (Attendance.designation == self.designation)
				& (Attendance.shift != self.shift)
				& (Attendance.name != self.name)
			)
		).run(as_dict=True)

		if same_date_attendance and has_overlapping_timings(self.shift, same_date_attendance[0].shift):
			return same_date_attendance[0]
		return {}
