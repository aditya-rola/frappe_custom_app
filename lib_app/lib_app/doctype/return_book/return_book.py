import frappe
from frappe.model.document import Document
from datetime import datetime
from lib_app.utils.utils import send_book_transaction_email

class ReturnBook(Document):
    def before_save(self):

        # Cross Check Book
        issed_bk = frappe.get_doc("Issued Book",self.issue_id)
        # validate issued id 
        if issed_bk.book != self.book or issed_bk.member != self.member:
            frappe.throw("Incorrect Book or Issue id or Member", title="Check Issue Id or Book or Member Selection")

        # Ensure return date is not earlier than issue date
        return_date = datetime.strptime(self.return_date, "%Y-%m-%d").date()
        if return_date < self.issue_date:
            frappe.throw("Return Date cannot be earlier than Issue Date.")

        difference = (return_date - self.issue_date).days

        # Rent fee calculation - charge extra based on the number of late days
        if difference > 0:
            self.rent_fee = self.rent_fee * difference  # Assuming rent is per day
        else:
            self.rent_fee = self.rent_fee  
            
        
    def on_submit(self):
        # Only update member's outstanding debt if the status is 'Active'
        member = frappe.get_doc("Member", self.member)
        if self.status == "Active":
            member.outstanding_debt = float(member.outstanding_debt) + float(self.rent_fee)  
            member.save()
        
        # Update member Issued book Table with Return Date
        child_tbl = frappe.get_all("Issued Books Table",filters=[{"book":self.book},{"issued_book":self.issue_date},{"parent": self.member}])
        if child_tbl:
            child_tbl_val = frappe.get_doc("Issued Books Table", child_tbl[0])
            child_tbl_val.returned_book = self.return_date
            child_tbl_val.save()
        
        recipients = []
        recipients.append(member.email) if member.email else []

        pdf_content = frappe.attach_print(self.doctype, self.name, print_format="Standard")
        args = {
            'transaction_type' : 'Return',
            'book_name' : self.book,
            'title' : self.book_title,
            'author' : self.author,
            'member' : self.member,
            'attachments' : [pdf_content],
            'book_issued' : self.book,
            'return_date' : self.return_date,
            'rent_fee' : self.rent_fee,
            'recipients' : recipients
        }

        # Send Notification via Email
        frappe.enqueue(send_book_transaction_email,**args)
