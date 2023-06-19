document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".submit-btn").addEventListener("click", validate);
  showError("");
});

function validate() {
  var firstName = document.getElementsByName("first_name")[0].value;
  var lastName = document.getElementsByName("last_name")[0].value;
  var email = document.getElementsByName("email")[0].value;
  var accountType = document.getElementsByName("account_type")[0].value;
  var username = document.getElementsByName("username")[0].value;
  var password = document.getElementsByName("password")[0].value;
  var confirmPassword = document.getElementsByName("confirm_password")[0].value;

  if (
    firstName === "" ||
    lastName === "" ||
    email === "" ||
    accountType === "Select an account" ||
    username === "" ||
    password === "" ||
    confirmPassword === ""
  ) {
    showError("All fields are reuquired");
    return false;
  }

  return true;
}

function showError(message) {
  var errorBlock = document.getElementsByClassName("alert-danger fields")[0];

  if (message == "") {
    errorBlock.style.display = "none";
  } else {
    errorBlock.textContent = message;
    errorBlock.style.display = "block";

    setTimeout(function () {
      errorBlock.style.display = "none";
    }, 3000);
  }
}
