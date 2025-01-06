import frappe
from lib_app.utils.utils import send_workflow_action_email

@frappe.whitelist()
def get_all_books():
    all_bk = frappe.get_all("Books",fields=["book_title", "author", "quantity", "rent_fee", "name"])
    return all_bk