$(document).ready(function() {

var csrftoken = $('meta[name=csrf-token]').attr('content')

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

//this function for the REGISTER PAGE
document.getElementById("username").addEventListener("input", function() {
  const username = this.value;
  let status = document.getElementById("status");

  status.innerHTML = "";

  if (username.length < 6) {
    status.innerHTML = "Username must be at least 6 characters.";
  } else if (username.length > 25) {
    status.innerHTML = "Username must be no more than 25 characters.";
  } else if (!/^[a-zA-Z0-9]+$/.test(username)) {
    status.innerHTML = "Username can only contain letters and numbers.";
  }
});

document.getElementById("email").addEventListener("input", function() {
  const email = this.value;
  let status = document.getElementById("status");

  status.innerHTML = "";

  if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
    status.innerHTML = "Please enter a valid email.";
  }
});

document.getElementById("password").addEventListener("input", function() {
  const password = this.value;
  let status = document.getElementById("status");

  status.innerHTML = "";

  if (password.length < 8) {
    status.innerHTML = "Password must be at least 8 characters.";
  } else if (password.length > 25) {
    status.innerHTML = "Password must be no more than 25 characters.";
  }
});

document.getElementById("passwordConfirm").addEventListener("input", function() {
  const passwordConfirm = this.value;
  const password = document.getElementById("password").value;
  let matchStatus = document.getElementById("MatchStatus");

  matchStatus.innerHTML = "";

  if (passwordConfirm !== password) {
    matchStatus.innerHTML = "Passwords do not match.";
    matchStatus.style.color = "red";
  } else {
    matchStatus.innerHTML = "Passwords match.";
    matchStatus.style.color = "green";
  }
});

document.getElementById("myForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const passwordConfirm = document.getElementById("passwordConfirm").value;
  let status = document.getElementById("status");
  let matchStatus = document.getElementById("MatchStatus");

  if (username.length < 6 || username.length > 25) {
    status.innerHTML = "Username must be between 6 and 25 characters.";
    return;
  }

  if (!/^[a-zA-Z0-9]+$/.test(username)) {
  status = "Username can only contain letters and numbers.";
  return;
  }

  if (!/^\w+([.-]?\w+)@\w+([.-]?\w+)(.\w{2,3})+$/.test(email)) {
  status.innerHTML = "Please enter a valid email.";
  return;
  }

  if (password.length < 8 || password.length > 25) {
  status.innerHTML = "Password must be between 8 and 25 characters.";
  return;
  }

  if (passwordConfirm !== password) {
  matchStatus.innerHTML = "Passwords do not match.";
  matchStatus.style.color = "red";
  return;
  }
  // Here you can send the form data to the server using AJAX or any other method.

    const submitBtn = document.getElementById("signup_btn");

  if (username.length >= 6 && username.length <= 25 &&
      /^[a-zA-Z0-9]+$/.test(username) &&
      /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email) &&
      password.length >= 8 && password.length <= 25 &&
      passwordConfirm === password) {
    submitBtn.disabled = false;
  } else {
    submitBtn.disabled = true;
  }

  // For example, using jQuery:

  req = $.ajax({
  type: "POST",
  url: window.location.origin + "/register",
  data: { username: username, email: email, password: password },
  success: function(response) {
    window.open(window.location.origin + "/login/", "_self");
  },
  error: function(jqXHR, textStatus, errorThrown, data) {
    let errorMessage = JSON.parse(jqXHR.responseText).error;
    status.innerHTML = errorMessage;
    status.style.color = "red";
  }

});

})

});