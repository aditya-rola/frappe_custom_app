frappe.ui.form.on('Books', {
	refresh(frm) {
	
	if (frappe.user.has_role("Librarian")) {
		frm.add_custom_button(__('Issue Book'), function () {
			frappe.new_doc('Issued Book', {
				book: frm.doc.name
			});
		}, __('Transaction Type'));

		// Add "Issue Book" button
		frm.add_custom_button(__('Return Book'), function () {
			frappe.new_doc('Return Book', {
				book: frm.doc.name
			});
		}, __('Transaction Type'));
	}
	}
})