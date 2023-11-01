$(document).ready(function() {
    $('search-form').on('submit',function (e) {
        e.preventDefault();

        var searchQuery = $('#search-input').val();

        $.ajax({
            url: "{% url 'api' %}",
            data: { search: searchQuery},
            method: 'GET',
            success: function (data) {
                $('.search-results').html(data);
            }
        })
    })
})

