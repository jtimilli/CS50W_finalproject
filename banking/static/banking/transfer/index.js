document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#receiverAccountNumber")
    .addEventListener("input", checkReceiver);
});

function checkReceiver() {
  const accountNumber = this.value;
  const errorDiv = document.querySelector(".receiver-error");
  const receiverInput = document.querySelector("#receiverAccountNumber");

  errorDiv.textContent = ""; // Clear previous error message

  if (accountNumber.length < 10) {
    errorDiv.classList.remove("alert");
    receiverInput.classList.remove("success");
  } else if (accountNumber.length === 10) {
    fetch("/check_reciever_account", {
      method: "POST",
      body: JSON.stringify({
        accountNumber: accountNumber,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.found) {
          // Account number found
          errorDiv.textContent = "";
          errorDiv.classList.remove("alert");
          receiverInput.classList.add("success");
        } else {
          // Account number not found
          errorDiv.textContent = "Invalid account number";
          errorDiv.classList.add("alert");
          receiverInput.classList.remove("success");
        }
      });
  } else {
    errorDiv.textContent = "Account number must be 10 characters long";
    errorDiv.classList.add("alert");
    receiverInput.classList.remove("success");
  }
}
