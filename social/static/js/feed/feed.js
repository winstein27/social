var deletePost = function(url, id) {
    $.ajaxSetup(getAjaxSettings());

    $.post(url, {"post_id": id}, function(data) {
        $("#post_" + id).fadeOut(function() {
            $(this).remove();
        });
    })
    .fail(function() {
        Materialize.toast("Não foi possível remover a publicação!", 4000, 'rounded');
    });
};

var init = function() {
    $(".delete-post").click(function(event) {
        event.preventDefault();
    });
};

$(init);
