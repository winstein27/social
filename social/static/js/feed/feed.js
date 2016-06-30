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

var like = function(url, post_id) {
    $.ajaxSetup(getAjaxSettings());

    $.post(url, {'post_id': post_id}, function(likes_count) {
        icon = $("#like_" + post_id);
        icon.removeAttr("class");

        post_likes_number = $("#" + post_id + "_likes");

        if(Number(likes_count) < Number(post_likes_number.text())) {
            icon.addClass("material-icons grey-text text-darken-2");
        }
        else {
            icon.addClass("material-icons light-green-text text-accent-4");
        }

        post_likes_number.text(likes_count);
    })
    .fail(function() {
        showToastMessage('Não foi possível gostar desta publicação!');
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

    $(".like-button").click(function(event) {
        event.preventDefault();
    });
};

$(init);
