var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

var deletePost = function(url, id) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if(!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            }
        }
    });

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
