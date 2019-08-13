
function searchSuccess(data, textStatus, jqXHR, thisNode)
{
    var tmp = data.split('\n');
//    window.alert(data);
    $(tmp[0]).html(data);
}

function happyFunction(e, thisNode) {
        $.ajax({
            type: "POST",
            url: "ajax/recipe/ing_unit",
            data: {
                search_text: thisNode.value,
                form_id: thisNode.id,
               'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    };