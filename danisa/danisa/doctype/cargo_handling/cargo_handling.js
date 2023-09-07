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

	set_shift_and_godown_query: function (frm) {
		frm.set_query("godownshed_no", function () {
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
				},
			};
		});
	},
});

frappe.ui.form.on("Operations", "no_of_bagsbales", function (frm, cdt, cdn) {
	let total_bags = 0;
	frm.doc.trucks.forEach(function (d) { total_bags += parseInt(d.no_of_bagsbales); });
	frm.set_value('total_no_of_bags', total_bags);
});
