// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Weekly Attendance Sheet"] = {
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
      default: frappe.datetime.add_days(frappe.datetime.nowdate(), -7),
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
      label: __("Designation"),
      fieldtype: "Link",
      options: "Designation",
    },
  ],
  onload: function (report) {
    const from_date_field = frappe.query_report.get_filter("from_date");
    const to_date_field = frappe.query_report.get_filter("to_date");

    if (from_date_field) {
      from_date_field.$input.on("change", function () {
        validateDateRange();
      });
    }

    if (to_date_field) {
      to_date_field.$input.on("change", function () {
        validateDateRange();
      });
    }
  },
};

function validateDateRange() {
  const from_date = frappe.query_report.get_filter_value("from_date");
  const to_date = frappe.query_report.get_filter_value("to_date");

  const fromDateObj = new Date(from_date);
  const toDateObj = new Date(to_date);
  const maxDateDifference = 7; // Maximum allowed difference between dates

  // Compare dates and show error message if invalid
  if (
    fromDateObj > toDateObj ||
    (toDateObj - fromDateObj) / (1000 * 60 * 60 * 24) > maxDateDifference
  ) {
    frappe.msgprint(
      __(
        "Invalid date range. The 'To Date' must be greater than or equal to 'From Date' and the difference between the two dates cannot be greater than 7 days."
      )
    );
    frappe.query_report.set_filter_value("to_date", frappe.datetime.nowdate());
  }
}
