import frappe


def send_book_transaction_email(
    transaction_type,
    book_name,
    title,
    author,
    member,
    attachments=[],
    issue_date=None,
    book_issued=None,
    return_date=None,
    rent_fee=None,
    recipients=None
):
    """
    Send an email for either book issue or book return using Frappe's email system.

    :param transaction_type: 'Issue' or 'Return' (type of transaction)
    :param book_name: Name of the book
    :param title: Title of the book
    :param author: Author of the book
    :param member: Name of the member (book issuer/returner)
    :param issue_date: Issue date (for 'Issue' transaction)
    :param book_issued: Book issued (for 'Return' transaction)
    :param return_date: Return date (for 'Return' transaction)
    :param recipients: List of email addresses to send the email to
    """
    # Add BCC
    librarians = frappe.get_all('User', filters={'role': 'Librarian'}, fields=[
                                'name', 'email', 'full_name', 'enabled'])
    bcc = [lb.email for lb in librarians]

    # Prepare the context for the template
    context = {
        'transaction_type': transaction_type,
        'book_name': book_name,
        'title': title,
        'author': author,
        'member': member,
        'issue_date': issue_date,
        'book_issued': book_issued,
        'return_date': return_date,
        'rent_fee': rent_fee,

    }

    # Render the email HTML using Frappe's render_template method
    email_html = frappe.render_template(
        'lib_app/templates/book_transaction.html', context)

    # Define the subject and header based on the transaction type
    if transaction_type == 'Issue':
        subject = f"Book Issue Confirmation: {title}"
        header = f"Book Issue Confirmation: {title}"
    else:
        subject = f"Book Return Confirmation: {title}"
        header = f"Book Return Confirmation: {title}"

    # Send the email using Frappe's sendmail method
    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        content=email_html,
        header=header,
        attachments=attachments,
        delayed=False,
        bcc=bcc
    )


def send_workflow_action_email(doc):
    """
    This function sends an email when the document is either approved or rejected in a workflow.
    """
    if doc.workflow_state not in ['Approved', 'Rejected']:
        return
    # Render the email HTML using Frappe's render_template method

    context = {
        'workflow_state': doc.workflow_state,
        'member_name': doc.member,
        'doctype': doc.doctype,
        'name': '',
    }
    email_html = frappe.render_template(
        'lib_app/templates/approved_reject.html', context)

    if doc.workflow_state == "Approved":
        subject = f"Your {doc.doctype} {doc.name} has been Approved"
    elif doc.workflow_state == "Rejected":
        subject = f"Your {doc.doctype} {doc.name} has been Rejected"

    # Send the email
    frappe.sendmail(
        recipients=[],
        subject=subject,
        content=email_html,
        delayed=False
    )
