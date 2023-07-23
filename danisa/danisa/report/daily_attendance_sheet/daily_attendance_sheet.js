// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Attendance Sheet"] = {
  filters: [
    {
      fieldname: "company",
      label: __("Company"),
      fieldtype: "Link",
      options: "Company",
      reqd: 1,
    },
    // {
    //   fieldname: "date_range",
    //   label: __("Date/Date Range"),
    //   fieldtype: "Select",
    //   options: ["Date", "Date Range"],
    //   default: "Date Range",
    //   on_change: function (query_report) {
    //     const filter_based_on =
    //       frappe.query_report.get_filter_value("date_range");

    //     frappe.query_report.toggle_filter_display(
    //       "from_date",
    //       filter_based_on === "Date"
    //     );
    //     frappe.query_report.toggle_filter_display(
    //       "to_date",
    //       filter_based_on === "Date"
    //     );
    //     frappe.query_report.toggle_filter_display(
    //       "attendance_date",
    //       filter_based_on === "Date Range"
    //     );

    //     frappe.query_report.refresh();
    //   },
    // },
    {
      fieldname: "attendance_date",
      label: __("Attendance Date"),
      fieldtype: "Date",
	  reqd: 1,
    //   hidden: 1,
    //   on_change: function (query_report) {
    //     const attendance_date =
    //       frappe.query_report.get_filter("attendance_date");
    //     const from_date = frappe.query_report.get_filter("from_date");
    //     const to_date = frappe.query_report.get_filter("to_date");

    //     if (attendance_date) {
    //       frappe.query_report.set_filter_value("from_date", "");
    //       frappe.query_report.set_filter_value("to_date", "");
    //     }
    //   },
    },
    // {
    //   fieldname: "from_date",
    //   label: __("From Date"),
    //   fieldtype: "Date",
    //   on_change: function (query_report) {
    //     const attendance_date =
    //       frappe.query_report.get_filter("attendance_date");
    //     const from_date = frappe.query_report.get_filter("from_date");

    //     if (from_date) {
    //       frappe.query_report.set_filter_value("attendance_date", "");
    //     }
    //   },
    // },
    // {
    //   fieldname: "to_date",
    //   label: __("To Date"),
    //   fieldtype: "Date",
    // },
    {
      fieldname: "designation",
      label: __("Designation"),
      fieldtype: "Link",
      options: "Designation",
    },
  ],
};
