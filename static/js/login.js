$(document).ready(function() {

var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

//this function for the LOGIN PAGE
$("#login_button").click(function() {
    var email = $("#floatingLoginInput").val();
    var password = $("#floatingLoginPassword").val();
  req = $.ajax({
    url: window.location.origin + "/login/",
    type: "POST",
    data: {email:email, password:password},
    success: function(response) {
      if (response.status === "success") {
        window.open(window.location.origin + "/user/", "_self");
      } else {
        $("#error").text(response.error);
      }
    }
    });
});

})