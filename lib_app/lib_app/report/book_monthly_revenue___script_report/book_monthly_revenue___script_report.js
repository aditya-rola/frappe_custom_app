// Copyright (c) 2024, admin and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Book Monthly Revenue --Script report"] = {
  filters: [
    {
      fieldname: "month",
      label: __("Month"),
      fieldtype: "Select",
      options: [
        { label: "January", value: "1" },
        { label: "February", value: "2" },
        { label: "March", value: "3" },
        { label: "April", value: "4" },
        { label: "May", value: "5" },
        { label: "June", value: "6" },
        { label: "July", value: "7" },
        { label: "August", value: "8" },
        { label: "September", value: "9" },
        { label: "October", value: "10" },
        { label: "November", value: "11" },
        { label: "December", value: "12" },
      ],
      reqd: 0,
    },
    {
      fieldname: "book",
      label: __("Book"),
      fieldtype: "Link",
      options: "Books",
      reqd: 0,
    },
  ],
  onload(report) {
    // add an action button to visit ToDo List View
    report.page.add_inner_button("Go to Return Book List", () => {
      frappe.set_route("List", "Return Book");
    });
    report.page.add_inner_button("Add Issued Book", () => {
      let d = new frappe.ui.Dialog({
        title: __("Add Issued Book"),
        fields: [
          {
            fieldname: "book",
            fieldtype: "Link",
            in_list_view: 1,
            label: "Book",
            options: "Books",
            reqd: 1,
          },
          {
            fieldname: "member",
            fieldtype: "Link",
            in_list_view: 1,
            label: "Member",
            options: "Member",
            reqd: 1,
          },
          {
            fieldname: "issue_date",
            fieldtype: "Date",
            label: "Issue Date",
            reqd: 1,
          },
        ],
        size: "small",
        primary_action_label: "Submit",
        primary_action(values) {
          values.doctype = "Issued Book";

          // Add Data in Database
          frappe.db
            .insert(values)
            .then((doc) => {
              // Submit the document
              frappe.call({
                method: "frappe.client.submit",
                args: { doc: doc },
                callback: function (response) {
                  console.log(response.message);
                  frappe.msgprint(
                    `Document ${response.message.name} created and submitted successfully.`
                  );
                },
              });
            })
            .catch((err) => {
              frappe.msgprint(`Error: ${err.message}`);
            });

          // Hide dailog
          d.hide();
        },
      });

      d.show();
    });
  },
};
