// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cargo Handling', {
	refresh: function (frm) {
		if (frm.doc.company) {
			frm.trigger("set_shift_and_godown_query");
		}
	},
	onload: function (frm) {
		if (frm.doc.company) {
			frm.trigger("set_shift_and_godown_query");
		}
	},
	company: function (frm) {
		if (frm.doc.company) {
			frm.trigger("set_shift_and_godown_query");
		}
	},
	validate: function (frm) {
		frm.set_value('total_no_of_bags', 0);
		let total_bags = 0;
		frm.doc.trucks.forEach(function (d) { total_bags += parseInt(d.no_of_bagsbales); });
		frm.set_value('total_no_of_bags', total_bags);
	},

	set_shift_and_godown_query: function (frm) {
		frm.set_query("godown_or__shed_no", function () {
			let company = "";
			if (frm.doc.company) {
				company = frm.doc.company;
			}
			return {
				filters: {
					company: company,
				},
			};
		});

		frm.set_query("shift", function () {
			let company = "";
			let emp_group = "Peace Rate";
			if (frm.doc.company) {
				company = frm.doc.company;
			}
			return {
				filters: {
					company: company,
					employee_group: emp_group,
				},
			};
		});

		frm.set_query("designation", function () {
			let company = "";
			if (frm.doc.company) {
				company = frm.doc.company;
			}
			return {
				filters: {
					company: company,
					employee_group: "Peace Rate",
				},
			};
		});
		frm.set_query("commodity_type", function () {
			let company = "";
			if (frm.doc.company) {
				company = frm.doc.company;
			}
			return {
				filters: {
					company: company,
				},
			};
		});

		frm.set_query("commodity", "trucks", function (doc, cdt, cdn) {
			let company = "";
			if (frm.doc.company) {
				company = frm.doc.company;
			}
			return {
				filters: {
					company: company,
				}
			};

		});
	},
});

frappe.ui.form.on("Operations", "no_of_bagsbales", function (frm, cdt, cdn) {
	frm.set_value('total_no_of_bags', 0);
	let total_bags = 0;
	frm.doc.trucks.forEach(function (d) { total_bags += parseInt(d.no_of_bagsbales); });
	frm.set_value('total_no_of_bags', total_bags);
});
