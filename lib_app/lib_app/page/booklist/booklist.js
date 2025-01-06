frappe.pages["booklist"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "List of Books",
    single_column: true,
  });

  // Set primary action button with custom styles
  let $btnAddNew = page.set_primary_action(
    "Add New",
    () => create_new_book(),
    "octicon octicon-plus"
  );
  $btnAddNew.addClass("btn btn-primary shadow-sm mb-4");

  // Add a custom field for linking to the "Books" DocType
  page.bookLinkField = page.add_field({
    fieldname: "book_link",
    label: __("Book"),
    fieldtype: "Link",
    options: "Books",
  });

  // Create a section for displaying the book list
  page.bookListSection = $(
    '<section class="bg-white overflow-auto rounded-0 rounded-bottom" id="book-list-section"></section>'
  );
  page.bookListSection.appendTo(page.main);

  // Function to load and display the list of books in a styled div layout
  page.load_book_list = function () {
    page.bookListSection.html(
      '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>'
    );

    frappe.call({
      method: "frappe.client.get_list",
      // method: "lib_app.custom_scripts.scripts.get_all_books",
      args :{
        doctype: "Books",
        fields: ["name","book_title","author"],
        limit_page_length: 100, 
      },
      callback: function (response) {
        if (response.message && response.message.length) {
          var booksHtml = `
			  <div class="result">
				<header class="level list-row-head text-muted">
				  <div class="level-left list-header-subject">
					<div class="list-row-col ellipsis list-subject level">
					  <input class="level-item list-check-all" type="checkbox" title="Select All">
					  <span class="level-item list-liked-by-me hidden-xs">
						<span title="Likes">
						  <svg class="icon icon-sm">
							<use class="like-icon" href="#icon-heart"></use>
						  </svg>
						</span>
					  </span>
					  <span class="level-item">ID</span>
					</div>
					<div class="list-row-col ellipsis hidden-xs tag-col hide">
					  <span>Tag</span>
					</div>
					<div class="list-row-col ellipsis hidden-xs">
					  <span>Book Title</span>
					</div>
          <div class="list-row-col ellipsis hidden-xs">
					  <span>Author</span>
					</div>
				  </div>
				  <div class="level-left checkbox-actions" style="display: none;">
					<div class="level list-subject">
					  <input class="level-item list-check-all" type="checkbox" title="Select All">
					  <span class="level-item list-header-meta"></span>
					</div>
				  </div>
				</header>
			`;

          response.message.forEach(function (book) {
            booksHtml += `
				<div class="list-row-container" tabindex="1">
				  <div class="level list-row">
					<div class="level-left ellipsis">
					  <div class="list-row-col ellipsis list-subject level">
						<span class="level-item select-like">
						  <input class="list-row-checkbox" type="checkbox" data-doctype="Books" data-name="${book.name}">
						  <span class="list-row-like hidden-xs" style="margin-bottom: 1px;">
							<span class="like-action not-liked" data-liked-by="[]" data-doctype="Books" data-name="${book.name}" title="">
							  <svg class="icon icon-sm">
								<use class="like-icon" href="#icon-heart"></use>
							  </svg>
							</span>
							<span class="likes-count">0</span>
						  </span>
						</span>
						<span class="level-item bold ellipsis">
						  <a class="ellipsis book-name-link" data-doctype="Books" data-name="${book.name}" href="#" title="${book.book_title}">
							${book.name}
						  </a>
						</span>
					  </div>
					  <div class="list-row-col tag-col hide hidden-xs ellipsis">
						<div class="tags-empty">-</div>
					  </div>
					  <div class="list-row-col ellipsis hidden-xs">
						<span class="ellipsis" title="Book Title: ${book.book_title}">
						  <a class="filterable ellipsis" data-filter="book_title,=,${book.book_title}">
							${book.book_title}
						  </a>
						</span>
					  </div>
             <div class="list-row-col ellipsis hidden-xs">
						<span class="ellipsis" title="Book Author: ${book.author}">
						  <a class="filterable ellipsis" data-filter="author,=,${book.author}">
							${book.author}
						  </a>
						</span>
					  </div>
					</div>
				  </div>
				</div>
			  `;
          });

          // Update the book list section with the generated div-based layout
          booksHtml += `</div>`;
          page.bookListSection.html(booksHtml);

          // Bind click event to book name link
          $(".book-name-link").on("click", function (e) {
            e.preventDefault();
            var bookName = $(this).data("name");
            show_book_details(bookName);
          });
        } else {
          page.bookListSection.html(
            '<div class="text-center text-muted">No books found.</div>'
          );
        }
      },
    });
  };

  // Call to load book list on page load
  page.load_book_list();
};

// Function to create a new book
function create_new_book() {
  let d = new frappe.ui.Dialog({
    title: __("Add Book"),
    fields: [
      {
        fieldname: "book_title",
        fieldtype: "Data",
        in_list_view: 1,
        label: "Book Title",
        reqd: 1,
      },
      {
        fieldname: "author",
        fieldtype: "Data",
        label: "Author",
      },
      {
        fieldname: "rent_fee",
        fieldtype: "Float",
        label: "Rent Fee",
      },
      {
        fieldname: "time_issued",
        fieldtype: "Int",
        label: "Time Issued",
      },
      {
        fieldname: "quantity",
        fieldtype: "Int",
        label: "Quantity",
      },
    ],
    size: "small",
    primary_action_label: "Submit",
    primary_action(values) {
      values.doctype = "Books"; // Set the DocType to Books
      console.log(values);

      // Add the new book data to the database
      frappe.db
        .insert(values)
        .then((doc) => {
          // If the insert is successful, you can either submit the document or take further actions
          frappe.call({
            method: "frappe.client.submit",
            args: { doc: doc },
            callback: function (response) {
              frappe.msgprint(
                __(
                  `Book ${response.message.name} created and submitted successfully.`
                )
              );
            },
          });
        })
        .catch((err) => {
          frappe.msgprint(__(`Error: ${err.message}`));
        });

      // Hide the dialog after submission
      d.hide();
    },
  });

  d.show();
}

function show_book_details(bookName) {
  frappe.call({
    method: "frappe.client.get",
    args: {
      doctype: "Books",
      name: bookName,
    },
    callback: function (response) {
      if (response.message) {
        var book = response.message;
        var detailsHtml = `
			<div>
			  <h4>Book Details</h4>
			  <p><strong>Book Title:</strong> ${book.book_title}</p>
			  <p><strong>Author:</strong> ${book.author}</p>
			  <p><strong>Quantity:</strong> ${book.quantity}</p>
			  <p><strong>Rent Fee:</strong> ${book.rent_fee}</p>
			</div>
		  `;

        // Create a new Dialog using frappe.ui.Dialog
        var dialog = new frappe.ui.Dialog({
          title: `Details for ${book.book_title}`,
          fields: [
            {
              fieldtype: "HTML",
              label: "Book Details",
              fieldname: "book_details",
              read_only: 1,
            },
          ],
          primary_action: function () {
            this.hide();
          },
          primary_action_label: __("Close"),
        });

        // Set the HTML content for the dialog
        dialog.fields_dict.book_details.set_value(detailsHtml);

        // Show the dialog
        dialog.show();
      }
    },
  });
}
