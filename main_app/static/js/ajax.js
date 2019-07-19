
function searchSuccess(data, textStatus, jqXHR, thisNode)
{
    var tmp = data.split('\n');
    var options = data.substr(data.indexOf('\n')+1);
    //window.alert(options);
    $(tmp[0]).html(options);
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
