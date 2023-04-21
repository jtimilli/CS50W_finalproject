document.addEventListener("DOMContentLoaded", () => {
  // Enable tooltip effect for bootstrap
  $('[data-toggle="tooltip"]').tooltip();

  document.querySelector("#make-deposit").addEventListener("click", deposit);
  document
    .querySelector("#account_number")
    .addEventListener("click", toggleAccountNumber);
});

// Updates using account with amount deposited
function deposit() {
  // Test to change modal button inner text
  value = document.querySelector("#deposit_amount").value;

  //check to vlaue is not empty
  if (value.length > 0) {
    $("#myModal").modal("hide");

    // Send API request to update bank account
    fetch("deposit/", {
      method: "POST",
      body: JSON.stringify({
        amount: value,
      }),
    })
      .then(response => response.json())
      .then(result => console.log(result));
  }
}

// Toggle the account number from hidden to vidisble
function toggleAccountNumber() {
  account_number = this.dataset.account_number;
  content = this.innerText;
  if (content != account_number) {
    this.innerText = account_number;
    setTimeout(() => {
      this.innerText = "**********";
    }, 5000);
  } else this.innerText = "**********";

  console.log(content);
}
