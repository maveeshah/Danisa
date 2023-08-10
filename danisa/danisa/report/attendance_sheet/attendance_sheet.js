// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Sheet"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.add_days(frappe.datetime.nowdate(), -6),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.nowdate(),
			reqd: 1,
		},
		{
			fieldname: "employee_group",
			label: __("Employee Group"),
			fieldtype: "Link",
			options: "Employee Group",
			// get_query: () => {
			// 	var company = frappe.query_report.get_filter_value('company');
			// 	return {
			// 		filters: {
			// 			'company': company
			// 		}
			// 	}
			// }
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
						'employee_group': employee_group,
						'company': company
					}
				}
			}
		},
	],
};
