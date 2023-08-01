// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on('Multi Attendance Tool', {
  refresh: function (frm) {
    if (frm.doc.employees) {
      frm.add_custom_button(__('Mark Attendance'), function () {
        return frappe.call({
          doc: frm.doc,
          method: 'mark_attendance',
          callback: function (response) {
            if (response && response.message) {
              if (response.message == 'Success'){
                frappe.msgprint("Attendance Marked",alert=true)
              }
              else{
                frappe.throw("Couldn't Mark Attendance")
              }
            }
          }
        })
      })
    }
  },
  fetch_employees: function (frm) {
    return frappe.call({
      doc: frm.doc,
      method: 'get_emp_list',
      callback: function (response) {
        if (response && response.message) {
          var employee_list = response.message // Assuming the response contains a list of employees
          console.log(employee_list)
          frm.doc.employees = []
          employee_list.forEach(function (row) {
            var child_row = frappe.model.add_child(
              frm.doc,
              'Attendance Tool Table',
              'employees'
            )
            frappe.model.set_value(
              child_row.doctype,
              child_row.name,
              'employee',
              row.name
            )
            frappe.model.set_value(
              child_row.doctype,
              child_row.name,
              'employee_name',
              row.employee_name
            )
            frappe.model.set_value(
              child_row.doctype,
              child_row.name,
              'id_number',
              row.id_number
            )
          })
          frm.refresh_field('employees')
        }
      }
    })
  }
})
