frappe.ui.form.on("Test Company Pin Code", {
  cmpny_name: function (frm) {
    console.log("chanegsssssss", frm);
    frm.set_query("pin_code", (doc) => {
      console.log(doc);
      return {
        filters: {
          provider_id: doc.cmpny_name,
        },
      };
    });
  },

  pin_code: (frm) => {
    console.log(frm);
    let pin_cd = frappe.db.get_doc("Pin Code", frm.doc.pin_code);
    let res = pin_cd.then(
      (val) => {
        console.log(val);
        frm.set_query("cmpny_name", (doc) => {
          return {
            filters: {
              name: val.provider_id,
            },
          };
        });
      },
      (err) => {
        console.error(err);
        frm.set_query("cmpny_name", (doc) => {
          return {
            filters: {
              name: "",
            },
          };
        });
      }
    );
  },
});
