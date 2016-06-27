var showToastMessage = function(message) {
    Materialize.toast(message, 4000, 'rounded');
};

var deletePost = function(url, id) {
    $.ajaxSetup(getAjaxSettings());

    $.post(url, {"post_id": id}, function(data) {
        $("#post_" + id).fadeOut(function() {
            $(this).remove();
        });
    })
    .fail(function() {
        showToastMessage("Não foi possível remover a publicação!");
    });
};

var deleteComment = function(url, id) {
    $.ajaxSetup(getAjaxSettings());

    $.post(url, {'comment_id': id}, function(data) {
        $("#comment_" + id).fadeOut(function() {
            $(this).remove();
        });
    })
    .fail(function() {
        showToastMessage("Não foi possível remover o comentário!");
    });
};

var init = function() {
    $(".delete-post").click(function(event) {
        event.preventDefault();
    });
};

$(init);
