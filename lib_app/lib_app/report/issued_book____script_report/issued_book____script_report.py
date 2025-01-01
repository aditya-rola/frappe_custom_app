# Copyright (c) 2024, admin and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"fieldname": "member", "label": "Member", "fieldtype": "Link", "options": "Member", "width": 200},
        {"fieldname": "issued_count", "label": "Books Issued", "fieldtype": "Int", "width": 150},
    ]

    issued_books = frappe.get_all(
        "Issued Book",
        fields=["member"],
    )

    member_counts = {}
    for entry in issued_books:
        member = entry["member"]
        if member in member_counts:
            member_counts[member] += 1
        else:
            member_counts[member] = 1

    data = [{"member": member, "issued_count": count} for member, count in member_counts.items()]

    frappe.msgprint(repr(data))
    chart_data = {
        "labels": [row["member"] for row in data], 
        "datasets": [
            {
                "name": "Books Issued",# Y-axis values
                "values":[row["issued_count"] for row in data]
            }
        ],
    }

    chart = {
        "data": chart_data,
        "type": "bar",
    }


    return columns, data, None, chart, None
