var result = document.getElementById('result');
var search_button = document.getElementById('search-button');

$(document).ready(function () {
    $('#search').keyup(function () {
        //sanitize input

        var searchTerm = $(this).val();
        searchTerm = searchTerm.replace(/[^a-zA-Z0-9]/g, '');


        search_button.href = "/user/search?searchTerm=" + $(this).val();

        if (searchTerm != '') {
            $.ajax({
                url: "/user/search",
                method: "POST",
                data: {
                    searchTerm: searchTerm
                },
                success: function (data) {

                    result.innerHTML = '';

                    for (var i = 0; i < data.length; i++) {
                        result.innerHTML += '<a class="dropdown-item" href="/user/profile/' + data[i].username + '">' + data[i].username + '</a>';
                    }
                }
            });
        }
    });
});