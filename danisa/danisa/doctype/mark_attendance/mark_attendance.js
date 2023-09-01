// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mark Attendance", {
  onload: function (frm) {
    frm.trigger("set_shift_and_designation_query");
  },

  company: function (frm) {
    frm.trigger("set_shift_and_designation_query");
    me.frm.set_query("name_series", "add_employee", function(doc, cdt, cdn) {
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

  attendance_date(frm) {
    frm.trigger("validate_date_match");
  },

  in_time(frm) {
    frm.trigger("validate_date_match");
    frm.trigger("calculate_and_validate_time_diff");
  },

  validate_date_match(frm) {
    if (frm.doc.in_time && frm.doc.attendance_date) {
      var inTimeDatePart = frappe.datetime
        .obj_to_user(new Date(frm.doc.in_time))
        .substring(0, 10);
      var attendanceDate = frappe.datetime.obj_to_user(frm.doc.attendance_date);

      if (inTimeDatePart !== attendanceDate) {
        frappe.msgprint(
          __(
            "In-time attendance_date must match the selected attendance attendance_date."
          )
        );
        frm.doc.in_time = "";
        frm.refresh_fields(["in_time"]);
      }
    }
  },

  out_time(frm) {
    frm.trigger("calculate_and_validate_time_diff");
  },

  calculate_and_validate_time_diff(frm) {
    if (frm.doc.in_time && frm.doc.out_time) {
      var timeIn = new Date(frm.doc.in_time);
      var timeOut = new Date(frm.doc.out_time);
      var timeDifference = (timeOut - timeIn) / (1000 * 60 * 60); // Difference in hours

      if (timeDifference < 0) {
        frappe.msgprint(__("Time Out must be ahead of Time In."));
        frm.doc.out_time = "";
        frm.refresh_fields("out_time");
      }
    }
  },

  set_shift_and_designation_query: function (frm) {
    frm.set_query("designation", function () {
      let company = "";
      let emp_group = "";
      if (frm.doc.company) {
        company = frm.doc.company;
      }
      if (frm.doc.employee_group) {
        emp_group = frm.doc.employee_group;
      }
      return {
        filters: {
          company: company,
          employee_group: emp_group,
        },
      };
    });

    frm.set_query("shift", function () {
      let company = "";
      let emp_group = "";
      if (frm.doc.company) {
        company = frm.doc.company;
      }
      if (frm.doc.employee_group) {
        emp_group = frm.doc.employee_group;
      }
      return {
        filters: {
          company: company,
          employee_group: emp_group,
        },
      };
    });
  },
});