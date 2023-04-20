$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();

  document.querySelector("#make-deposit").addEventListener("click", deposit);
});

function deposit() {
  alert("test");
  $("#add-money").modal("toggle");
}
