frappe.ui.form.on("Return Book", {
  refresh: function (frm) {
    console.log(frm);
    if (frappe.user.has_role("Librarian") && frm.doc.docstatus == 1) {
      frm.add_custom_button(__("Payment"), function () {
        const paymentData = {
          member: frm.doc.member,
          book: frm.doc.book,
          return_id: frm.doc.name
        };
        console.log("Data being passed to Payments doc:", paymentData);
        frappe.new_doc("Payments", paymentData);
      });
    }
  },
});
