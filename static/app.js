
const searchInput = document.getElementById("menu-search");
const foodCards = document.querySelectorAll(".food-card");
const categoryButtons = document.querySelectorAll(".category-card");
const cartCount = document.getElementById("cart-count");
const emptyMessage = document.getElementById("empty-message");

let selectedCategory = "All";
let cartTotalItems = 0;

function filterMenu() {
    const searchText = searchInput.value.toLowerCase().trim();
    let visibleItems = 0;

    foodCards.forEach(function (card) {
        const itemName = card.querySelector("h3").textContent.toLowerCase();
        const itemDescription = card.querySelector(".food-details > p")
            .textContent.toLowerCase();
        const itemCategory = card.dataset.category;

        const matchesCategory =
            selectedCategory === "All" ||
            itemCategory === selectedCategory;

        const matchesSearch =
            itemName.includes(searchText) ||
            itemDescription.includes(searchText);

        if (matchesCategory && matchesSearch) {
            card.hidden = false;
            visibleItems++;
        } else {
            card.hidden = true;
        }
    });

    emptyMessage.hidden = visibleItems !== 0;
}

searchInput.addEventListener("input", filterMenu);

categoryButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        selectedCategory = button.dataset.category;

        categoryButtons.forEach(function (categoryButton) {
            categoryButton.classList.remove("active");
        });

        button.classList.add("active");
        filterMenu();
    });
});

document.querySelectorAll(".add-button").forEach(function (button) {
    button.addEventListener("click", function () {
        cartTotalItems++;
        cartCount.textContent = cartTotalItems;

        button.textContent = "✓";

        setTimeout(function () {
            button.textContent = "+";
        }, 500);
    });
});
