// Globání search timer
var searchTimeout = null;
var hideTimeout = null;

function search(el) {
    // Resetujeme timer
    if (searchTimeout != null) {
        clearTimeout(searchTimeout);
    }
    // Timer pro hledání
    searchTimeout = setTimeout( () => {
        // Získám hodnotu v textovém inputu
        let query = el.value;
        // Vypíšu
        console.log(query);

        fetch(`/api/search?q=${query}`)
          .then((response) => response.json())
          .then((data) => {
                let searchresults = document.getElementById("searchresults");
                if (data.products.length > 0) {
                    let content = "<ul>";
                    data.products.forEach( (product) => {
                        let [id, title] = product;

                        content += `<li><a href="/product/detail/${id}">${title}</a></li>`;
                    });
                    content += "</ul>";

                    searchresults.innerHTML = content;
                    searchresults.style.display = "block";
                    if (hideTimeout != null) {
                        clearTimeout(hideTimeout);
                    }
                    hideTimeout = setTimeout(() => {
                        searchresults.style.display = "none";
                    }, 3000);
                } else {
                    searchresults.innerHTML = "Nothing found";
                    searchresults.style.display = "block";
                }
          });
    }, 500);
}