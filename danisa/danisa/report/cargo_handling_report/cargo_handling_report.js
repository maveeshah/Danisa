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
      fieldname: "date",
      label: __("Date"),
      fieldtype: "Date",
      default: frappe.datetime.nowdate(),
      reqd: 1,
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
    // {
    //   fieldname: "operation",
    //   label: __("Operation"),
    //   fieldtype: "Select",
    //   options: ["Loading", "Offloading"],
    // },
    {
      fieldname: "godown",
      label: __("Godown"),
      fieldtype: "Data",
    },
  ],
};
