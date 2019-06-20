
function searchSuccess(data, textStatus, jqXHR, thisNode)
{
    $('#search-results').html(data);
}

function happyFunction(e, thisNode) {
        $.ajax({
            type: "POST",
            url: "/recipe/work/",
            data: {
               'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    };