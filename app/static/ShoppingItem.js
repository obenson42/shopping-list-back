// classes
class ShoppingItem {
    constructor(id, title, bought, position) {
        this.id = id;
        this.title = title;
        this.bought = bought;
        this.position = position;
    }
}

class ItemList {
    constructor() {
        this.allItems = [];
    }

    setContent(data) {
        this.allItems = [];
        for (let x of data) {
            const item = new ShoppingItem(x["id"], x["title"], x["bought"], x["position"]);
            this.allItems.push(item);
        }
        this.displayList();
    }

    // button methods
    viewAll(btn) {
        if(btn) {
            // disable button
            $(btn).prop("disabled", true);
            // add spinner to button
            $(btn).html(
                '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
            );
        }
        const self = this;
        $.getJSON("/items/", function (data) {
            self.setContent(data["shopping_items"]);
        })
            .fail(function () {
                alert("Problem getting shopping item list");
            })
            .always(function () {
                if(btn) {
                    // remove spinner to button
                    $(btn).html(
                        'View All'
                    );
                    // enable button
                    $(btn).prop("disabled", false);
                }
            });
    }

    addItem() {
        const itemTitle = sanitize($("#item_title").val());
        const itemBought = $("#item_year").val();
        const itemPosition = $("#item_position").val();
        // add item
        const self = this;
        $.ajax({
            method: "PUSH",
            url: "/item/",
            data: { id: 0, title: itemTitle, bought: itemBought, position: itemPosition},
            dataType: "json"
        })
            .done(function (result) {
                // clear the inputs
                self.clearForm();
                // get the list again so user can see item has gone
                self.viewAll();
            })
            .fail(function () {
                alert("Problem adding shopping item");
            });
    }

    updateItem() {
        const itemID = $("#item_id").val();
        const itemTitle = sanitize($("#item_title").val());
        const itemAuthorFirstName = sanitize($("#item_author_first_name").val());
        const itemAuthorSurname = sanitize($("#item_author_surname").val());
        const itemYear = sanitize($("#item_year").val());
        const self = this;
        $.ajax({
            method: "PUT",
            url: "/item/",
            data: { id: itemID, title: itemTitle, author_first_name: itemAuthorFirstName, author_surname: itemAuthorSurname, year: itemYear },
            dataType: "json"
        })
            .done(function (result) {
                // clear the inputs
                self.clearForm();
                // get the list again so user can see item has gone
                self.viewAll();
            })
            .fail(function () {
                alert("Problem updating item");
            });
    }

    deleteItem() {
        const itemID = $("#item_id").val();
        const self = this;
        $.ajax({
            method: "DELETE",
            url: "/item/?" + $.param({ "id": itemID }),
            dataType: "json"
        })
            .done(function (result) {
                // clear the inputs
                self.clearForm();
                // get the list again so user can see item has gone
                self.viewAll();
            })
            .fail(function () {
                alert("Problem deleting item");
            });
    }

    search(btn) {
        // disable button
        $(btn).prop("disabled", true);
        // add spinner to button
        $(btn).html(
            '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
        );
        // get field values and send to search
        const itemTitle = sanitize($("#item_title").val());
        const itemAuthorFirstName = sanitize($("#item_author_first_name").val());
        const itemAuthorSurname = sanitize($("#item_author_surname").val());
        const itemYear = sanitize($("#item_year").val());
        const self = this;
        $.getJSON("/items_search/?title=" + itemTitle + "&author_first_name=" + itemAuthorFirstName + "&author_surname=" + itemAuthorSurname + "&year=" + itemYear, function (data) {
            self.setContent(data["items"]);
        })
            .fail(function () {
                alert("Problem searching item list");
            })
            .always(function () {
                // remove spinner to button
                $(btn).html(
                    'Search'
                );
                // enable button
                $(btn).prop("disabled", false);
            });
    }

    // form clearing/updating from user interaction
    clearForm() {
        // clear any previous highlighted row
        this.clearPrevHighlight();
        // clear the inputs
        $("#item_id").val(0);
        $("#item_title").val("");
        $("#item_author_first_name").val("");
        $("#item_author_surname").val("");
        $("#item_year").val("");
        // disable buttons dependent on a table row having been clicked
        $("#btn_search").prop("disabled", true);
        $("#btn_add_item").prop("disabled", true);
        $("#btn_update_item").prop("disabled", true);
        $("#btn_delete_item").prop("disabled", true);
        // disable link to author page
        $("#link_current_author").removeClass("text-primary");
        $("#link_current_author").addClass("text-muted");
        // hide editions page
        $("#page_editions").hide("slow");
    }

    clearPrevHighlight() {
        // clear previous row hightlight if there was one
        const prevID = $("#item_id").val();
        if (prevID !== "0") {
            // un-highlight row
            $("#item" + prevID + " td").each(function () {
                $(this).css({ backgroundColor: "" });
            });
        }
    }

    // called by inputs when text is entered, updates which buttons are disabled
    fieldsChanged() {
        const itemID = $("#item_id").val();
        const itemTitle = $("#item_title").val();
        const itemAuthorFirstName = $("#item_author_first_name").val();
        const itemAuthorSurname = $("#item_author_surname").val();
        const itemYear = $("#item_year").val();
        const itemAuthorID = $("#item_author_id").val();
        $("#btn_search").prop("disabled", (itemTitle === "" && itemAuthorFirstName === "" && itemAuthorSurname === "" && itemYear === ""));
        $("#btn_add_item").prop("disabled", (itemID !== "0" || itemTitle === "" || itemAuthorFirstName === "" || itemAuthorSurname === "" || itemYear === ""));
        $("#btn_update_item").prop("disabled", (itemID === "0"));
    }

    // get likely author name from db based on first few characters of first name
    // also update available buttons
    authorLookupFirstName() {
        this.fieldsChanged();
        const itemAuthorFirstName = sanitize($("#item_author_first_name").val());
        if (itemAuthorFirstName.length > 3) {
            const pos = itemAuthorFirstName.length;
            $.getJSON("/author_search/?" + $.param({ "first_name": itemAuthorFirstName, "surname": "" }), function (data) {
                const x = data["authors"][0];
                if (x) {
                    const author = new Author(x["id"], x["first_name"], x["surname"], x["date_birth"], x["date_death"]);
                    $("#item_author_id").val(x.id);
                    $("#item_author_first_name").val(x.first_name);
                    $("#item_author_surname").val(x.surname);
                    $("#item_author_firstname").caretTo(pos);
                }
            })
                .fail(function () {
                    alert("Problem in author lookup");
                });
        }
    }

    // get likely author name from db based on first few characters of surname
    // also update available buttons
    authorLookupSurname() {
        this.fieldsChanged();
        const itemAuthorSurname = sanitize($("#item_author_surname").val());
        if (itemAuthorSurname.length > 3) {
            const pos = itemAuthorSurname.length;
            $.getJSON("/author_search/?" + $.param({ "first_name": "", "surname": itemAuthorSurname }), function (data) {
                const x = data["authors"][0];
                if (x) {
                    const author = new Author(x["id"], x["first_name"], x["surname"],  x["date_birth"], x["date_death"]);
                    $("#item_author_id").val(x.id);
                    $("#item_author_first_name").val(x.first_name);
                    $("#item_author_surname").val(x.surname);
                    $("#item_author_surname").caretTo(pos);
                }
            })
                .fail(function () {
                    alert("Problem in author lookup");
                });
        }
    }

    // JSON to HTML functions
    displayList() {
        let out = "";
        for (let i = 0; i < this.allItems.length; i++) {
            const item = this.allItems[i];
            out += '<tr id="item' + item.id + '">';
            out += '<td>' + item.title + '</td>';
            out += '<td>' + item.bought + '</td>';
            out += '<td>' + item.position + '</td>';
            out += '</tr>';
        }
        $("#item_list").find("tbody").empty();
        $("#item_list").find("tbody").append(out);
        // disable buttons dependent on a table row having been clicked
        $("#btn_update_item").prop("disabled", true);
        $("#btn_delete_item").prop("disabled", true);
    }

    fillFieldsFromItem(item) {
        $("#item_id").val(item.id);
        $("#item_title").val(item.title);
        $("#item_position").val(item.position);
        // update which buttons are disabled
        $("#btn_add_item").prop("disabled", true);
        $("#btn_update_item").prop("disabled", true); // can't update until user changes something
        $("#btn_delete_item").prop("disabled", false);
    }

    get numItems() {
        return this.allItems.length;
    }

    item(i) {
        return this.allItems[i];
    }

    itemByID(id) {
        return this.allItems.find(obj => obj.id === id);
    }
}

// create an instance of ItemList for all the UI to link to
gItemList = new ItemList();

$(document).ready(function () {
    // add event to inputs
    $("#item_title").on("input", function () {
        gItemList.fieldsChanged();
    });
    $("#item_year").on("input", function () {
        gItemList.fieldsChanged();
    });
    // add events to buttons
    $("#btn_view_all_items").click(function () {
        gItemList.viewAll(this);
    });
    $("#btn_search").click(function () {
        gItemList.search(this);
    });
    $("#btn_add_item").click(function () {
        gItemList.addItem();
    });
    $("#btn_update_item").click(function () {
        gItemList.updateItem();
    });
    $("#btn_clear_form_item").click(function () {
        gItemList.clearForm();
    });
    $("#btn_delete_item").click(function () {
        gItemList.deleteItem();
    });
    // add event to table rows
    $("#item_list").delegate('tr', 'click', function () {
        gItemList.clearPrevHighlight();
        // fill inputs with values for clicked row
        const id = parseInt($(this).attr("id").substring(4));
        for (let i = 0; i < gItemList.numItems; i++) {
            const item = gItemList.item(i);
            if (item['id'] === id) {
                gItemList.fillFieldsFromItem(item);
                // highlight row clicked on so user can check they clicked the right one
                $("td", this).each(function () {
                    $(this).css({ backgroundColor: "#f8f9fa" });
                });
                break;
            }
        }
    });
});
