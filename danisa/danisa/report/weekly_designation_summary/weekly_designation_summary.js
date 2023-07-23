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
		},
		{
		  fieldname: "to_date",
		  label: __("To Date"),
		  fieldtype: "Date",
		  reqd: 1,
		},
		{
		  fieldname: "shift",
		  label: __("Shift"),
		  fieldtype: "Link",
		  options: "Shift Type",
		},
	  ],
};
