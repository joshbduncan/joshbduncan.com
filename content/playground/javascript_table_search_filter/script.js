const searchInput = document.getElementById("search-input");
const searchTable = document.getElementById("search-table");
const rows = searchTable.querySelectorAll("tbody tr");

searchInput.addEventListener("input", function (e) {
  const q = e.target.value.toLowerCase();
  rows.forEach((row) => {
    const cells = Array.from(row.querySelectorAll("td"));
    const matchString = cells.map((n) => n.textContent.toLowerCase()).join(" ");
    const match = matchString.includes(q);
    row.classList.toggle("hide", !match);
  });
});
