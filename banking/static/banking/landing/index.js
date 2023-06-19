document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#login-btn").addEventListener("click", () => {
    window.location.href = "/login/";
  });

  document.querySelector("#signup-btn").addEventListener("click", () => {
    window.location.href = "/register/";
  });
});
