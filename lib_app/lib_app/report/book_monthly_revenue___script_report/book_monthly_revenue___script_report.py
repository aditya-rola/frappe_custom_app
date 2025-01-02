import frappe
from frappe.utils import flt
from datetime import datetime
import calendar

def execute(filters=None):
    # Define the report columns
    columns = [
        {"fieldname": "book", "label": "Book", "fieldtype": "Data", "options": "Books", "width": 200},
        {"fieldname": "book_title", "label": "Books Title", "fieldtype": "Data", "width": 150},
        {"fieldname": "author", "label": "Books Author", "fieldtype": "Data", "width": 150},
        {"fieldname": "revenue", "label": "Revenue", "fieldtype": "Int", "width": 150},
    ]

    book_filter = filters.get("book") if filters else None
    month_filter = filters.get("month") if filters else None
    year = 2025

    # Calculate the start and end date for the selected month
    if month_filter:
        start_date = datetime(year, int(month_filter), 1).date()
        _, last_day = calendar.monthrange(year, int(month_filter))
        end_date = datetime(year, int(month_filter), last_day).date()
    else:
        start_date = end_date = None

    # Create filter conditions for the query
    # filter_condition = {}
    # if book_filter:
    #     filter_condition["book"] = book_filter
    # if month_filter:
    #     filter_condition["return_date"] = ["between", [start_date, end_date]]

    # # Fetch data from the "Return Book" doctype using the filters
    # return_books = frappe.get_list(
    #     "Return Book",
    #     fields=["book", "author", "book_title", "rent_fee"],
    #     filters=filter_condition
    # )

    # # Aggregate revenue by book
    # revenue_by_book = {}
    # for entry in return_books:
    #     key = (entry["book"], entry["book_title"], entry["author"])
    #     revenue_by_book.setdefault(key, 0)
    #     revenue_by_book[key] += flt(entry["rent_fee"])

    # # Prepare the data for the report
    # data = [
    #     {
    #         'book': key[0],
    #         'book_title': key[1],
    #         'author': key[2],
    #         'revenue': value,
    #     } for key, value in revenue_by_book.items()
    # ]

    # direct SQL queries 
    filter_condition = f"WHERE book = '{book_filter}' {'AND' if book_filter and month_filter else 'OR'} return_date BETWEEN '{start_date}' AND '{end_date}'" 
    data = frappe.db.sql(f"""
            SELECT 
                book, book_title, author, SUM(rent_fee) AS revenue 
            FROM `tabReturn Book` 
            {filter_condition if filter_condition else ''}
            GROUP BY book;
    """, as_dict=True)

    # Prepare the chart data
    chart_data = {
        "labels": [book["book"] for book in data],  # X-axis labels
        "datasets": [
            {
                "name": "Revenue Of Book",  # Label for the dataset
                "values": [flt(rev["revenue"]) for rev in data]  # Y-axis values
            }
        ]
    }

    chart = {
        "data": chart_data,
        "type": "bar",
    }
    # Return the report columns, data, and chart
    return columns, data, None, chart
