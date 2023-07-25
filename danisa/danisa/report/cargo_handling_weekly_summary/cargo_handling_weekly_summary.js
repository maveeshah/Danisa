// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cargo Handling Weekly Summary"] = {
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
      default: frappe.datetime.add_days(frappe.datetime.nowdate(), -7),
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
      fieldname: "shift",
      label: __("Shift"),
      fieldtype: "Link",
      options: "Shift Type",
    },
    {
      fieldname: "operation",
      label: __("Operation"),
      fieldtype: "Select",
      options: ["Loading", "Offloading"],
    },
    {
      fieldname: "client",
      label: __("Client"),
      fieldtype: "Data",
    },
  ],
};
