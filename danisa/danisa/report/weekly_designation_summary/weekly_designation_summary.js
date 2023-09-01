// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Weekly Designation Summary"] = {
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
      reqd: 1,
      default: frappe.datetime.nowdate(),
    },
    {
      fieldname: "employee_group",
      label: __("Employee Group"),
      fieldtype: "Link",
      options: "Employee Group",
      default: "Daily Rated"
    },
    {
      fieldname: "shift",
      label: __("Shift"),
      fieldtype: "Link",
      options: "Shift Type",
			get_query: () => {
				var company = ''
        if (frappe.query_report.get_filter_value('company')){
          company = frappe.query_report.get_filter_value('company');
        };
				var employee_group = ''
        if (frappe.query_report.get_filter_value('employee_group')){
          employee_group = frappe.query_report.get_filter_value('employee_group');
        };
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

