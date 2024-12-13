//////////////////////////////////////
// Advanced Table Search Filtererrr //
//////////////////////////////////////

// Setup:
//  1. Page **must** include table with the id "search-table" (only one)
//  2. Page **must** include text input with id "search-input" (only one)
//  3. Table **may** include data-attribute "data-search-ignore-cols"
//     that will ignore any columns listed in the data attribute.
//     Columns to be ignored must be listed by index number (0-based)
//     and separated just a single comma(e.g. data-search-ignore-cols="0,2,1")

// check to see if search input is on page
const searchInput = document.getElementById("search-input");
if (searchInput != null) {
  // find the search table, cols to be search, and get the table rows
  const searchTable = document.getElementById("search-table");
  // check to see if search should ignore any specific columns
  const ignoreCols = searchTable.dataset.searchIgnoreCols
    ? searchTable.dataset.searchIgnoreCols.split(",").map(Number)
    : false;
  const rows = searchTable.querySelectorAll("tbody tr");
  // listen for input in the search field
  searchInput.addEventListener("keyup", function (e) {
    // grab the query text from the input
    const q = e.target.value.toLowerCase();
    // iterate over all table ros
    rows.forEach((row) => {
      const cols = row.querySelectorAll("td");
      // if search column indexes should be ignored
      const filteredCols = ignoreCols
        ? Array.from(cols).filter((_, n) => ignoreCols && !ignoreCols.includes(n))
        : Array.from(cols);
      // join all searched row text into one string for searching
      const colsText = filteredCols.map((n) => n.textContent.toLowerCase()).join(" ");
      // if the query string isn't in the row text hide the row
      row.classList.toggle("hide", !colsText.includes(q));
    });
  });
}
