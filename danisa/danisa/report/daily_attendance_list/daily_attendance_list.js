// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Attendance List"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
		},
		{
			fieldname: "attendance_date",
			label: __("Attendance Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.nowdate(),
		},
		{
			fieldname: "employee_group",
			label: __("Employee Group"),
			fieldtype: "Link",
			options: "Employee Group",
		},
		{
			fieldname: "designation",
			label: __("Designation"),
			fieldtype: "Link",
			options: "Designation",
			get_query: () => {
				var company = frappe.query_report.get_filter_value('company');
				var employee_group = frappe.query_report.get_filter_value('employee_group');
				return {
					filters: {
						'company': company,
						'employee_group': employee_group
					}
				}
			}
		},

		{
			fieldname: "shift",
			label: __("Shift"),
			fieldtype: "Link",
			options: "Shift Type",
			get_query: () => {
				var company = frappe.query_report.get_filter_value('company');
				var employee_group = frappe.query_report.get_filter_value('employee_group');
				return {
					filters: {
						'company': company,
						'employee_group': employee_group
					}
				}
			}
		},

	],
};
