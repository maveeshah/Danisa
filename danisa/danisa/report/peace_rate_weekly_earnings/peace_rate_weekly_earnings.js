// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Peace Rate Weekly Earnings"] = {
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
      default: frappe.datetime.add_days(frappe.datetime.nowdate(), -6),
      reqd: 1,
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
      reqd: 1,
      default: "Peace Rate",
    },
    {
      fieldname: "designation",
      label: __("Designation"),
      fieldtype: "Link",
      options: "Designation",
      reqd: 1,
      get_query: () => {
        var company = frappe.query_report.get_filter_value("company");
        var employee_group =
          frappe.query_report.get_filter_value("employee_group");
        return {
          filters: {
            employee_group: employee_group,
            company: company,
          },
        };
      },
    },
  ],
};
