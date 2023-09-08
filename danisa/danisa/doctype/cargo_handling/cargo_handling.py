# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class CargoHandling(Document):
	def validate(self):
		calc_total = 0
		if self.trucks:
			for row in self.trucks:
				calc_total += int(row.no_of_bagsbales)
			self.total_no_of_bags = calc_total
