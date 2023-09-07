// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cargo Handling Report"] = {
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
      fieldname: "designation",
      label: __("Section/Group"),
      fieldtype: "Link",
      options: "Designation",
			get_query: () => {
				var company = frappe.query_report.get_filter_value('company');
				return {
					filters: {
            'employee_group': "Peace Rate",
						'company': company
					}
				}
			}
    },
    {
      fieldname: "commodity_type",
      label: __("Commodity Type"),
      fieldtype: "Link",
      options: "Commodity Type",
    },
    {
      fieldname: "shift",
      label: __("Shift"),
      fieldtype: "Link",
      options: "Shift Type",
      get_query: () => {
        var company = frappe.query_report.get_filter_value('company');
        return {
          filters: {
            'company': company,
            'employee_group': "Peace Rate"
          }
        }
      }
    },
  ],
};
