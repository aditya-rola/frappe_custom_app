# Copyright (c) 2024, admin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Payments(Document):
	
	def on_change(self):
		print("!!!!!!!!!!!!!!!!!!!!!!!! CALLL VALIODATE METHOD  !!!!!!!!!!!!!!!!!!!!!")
		self.deduct_fee_and_sendmail_on_approval()

	

	def deduct_fee_and_sendmail_on_approval(self):
		# Check if the status has changed to "Approved"
		if self.workflow_state == 'Approved':
			member = frappe.get_doc("Member", self.member)
			current_fee = member.outstanding_debt
			print(f"Current Fee: {current_fee}, Rent Fee: {self.rent_fee}, Remaining Fee: {remaining_fee}")

			remaining_fee = current_fee - self.rent_fee
			member.outstanding_debt = remaining_fee
			member.save(ignore_permissions=True)
			# frappe.db.commit()
		else:
			print(f"Workflow state is not 'Approved' - it is: {self.workflow_state}")
