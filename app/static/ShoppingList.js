function goPageItems() {
    $("#page_items").show("slow");
    $("#link_items").addClass("active");
}

$(document).ready(function () {
    // add event to inputs
    $("#link_items").click(function (event) {
        event.preventDefault();
        goPageItems();
    });
});

function sanitize(string) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        "/": '&#x2F;',
    };
    const reg = /[&<>"'/]/ig;
    return string.replace(reg, (match)=>(map[match]));
}