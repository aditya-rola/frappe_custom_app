import frappe
from frappe.model.document import Document
from lib_app.utils.utils import send_book_transaction_email

class IssuedBook(Document):
    def on_submit(self):
        book = frappe.get_doc("Books", self.book)
        member = frappe.get_doc("Member", self.member)

        if int(book.quantity) > 0:
            book.quantity = int(book.quantity) - 1
            book.time_issued = int(book.time_issued) + 1
            # Update Member's issued books count
            if int(member.books_issued) < 3:
                member.books_issued = int(member.books_issued) + 1
                member.save()
            else:
                frappe.throw(f"Member '{member.name1}' has already issued the maximum allowed books.")
            book.save()

            # Update Member `my issued book` field
            member.append("my_issued_book",{
                 "book": book.name,
                "issued_book": self.issue_date,
                "returned_book": ""
            })
            member.save()
        else:
            frappe.throw(f"The book '{book.book_title}' is out of stock.")

        recipients = []
        recipients.append(member.email) if member.email else []

        pdf_content = frappe.attach_print(self.doctype, self.name, print_format="Standard")

        args = {
            'transaction_type' : 'Issue',
            'book_name' : self.book,
            'title' : self.book_title,
            'author' : self.author,
            'member' : self.member,
            'attachments' : [pdf_content],
            'issue_date' : self.issue_date,
            'recipients' : recipients
        }

        # Send Notification via Email
        frappe.enqueue(send_book_transaction_email,**args)

