
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".status-select").forEach(select => {
    const apply = () => {
      select.className = "form-control status-select";
      if (select.value) {
        select.classList.add("status-" + select.value.toLowerCase());
      }
    };
    apply();
    select.addEventListener("change", apply);
  });
});


