var showPasswordMessage = function(classes, message) {
    $("#div-message").removeAttr("class").addClass(classes);
    $("#password-message").text(message);
};

var init = function() {
    $('ul.tabs').tabs();

    $("#chage-password").submit(function(event) {
        event.preventDefault();

        var url = $(this).attr("action");

        $.ajaxSetup(getAjaxSettings());

        $.post(url, $(this).serialize(), function(url) {
            showPasswordMessage("light-green accent-3", "Senha alterada com sucesso!");
            window.location.replace(url);
        })
        .fail(function() {
            showPasswordMessage("red accent-4", "Verifique os dados informados!");
        });
    });
};

$(init);
