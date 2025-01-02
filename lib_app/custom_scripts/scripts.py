import frappe
from lib_app.utils.utils import send_workflow_action_email

def deduct_fee_and_sendmail_on_approval(doc, method):
    frappe.log("---------------------- METHOD CALL ------------------")
    print("---------------------- METHOD CALL ------------------")
    # Check if the status has changed to "Approved"
    if doc.workflow_state == 'Approved':
        member = frappe.get_doc("Member", doc.member)
        current_fee = member.outstanding_debt
        print(f"Current Fee: {current_fee}, Rent Fee: {doc.rent_fee}, Remaining Fee: {remaining_fee}")

        remaining_fee = current_fee - doc.rent_fee
        member.outstanding_debt = remaining_fee
        member.save(ignore_permissions=True)
        frappe.db.commit()
    else:
        print(f"Workflow state is not 'Approved' - it is: {doc.workflow_state}")
