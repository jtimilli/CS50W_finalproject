document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelector("#make-deposit-btn")
    .addEventListener("click", function () {
      document.querySelector("#add-money").style.display = "block";
      document.querySelector("#add-money").style.opacity = "1";
    });

  document
    .querySelector("#close-deposit")
    .addEventListener("click", function () {
      document.querySelector("#add-money").style.opacity = "0";
      setTimeout(function () {
        document.querySelector("#add-money").style.display = "none";
      }, 500); // Wait for the transition to complete before setting display to "none"
    });
});
