import frappe
from lib_app.utils.utils import send_workflow_action_email

def deduct_fee_and_sendmail_on_approval(doc, method):
    # Check if the status has changed to "Approved"
    if doc.status == 'Approved':
        member = frappe.get_doc("Member", doc.member)
        current_fee = member.outstanding_debt

        remaining_fee = current_fee - doc.rent_fee
        member.outstanding_debt = remaining_fee
        member.save()
        

