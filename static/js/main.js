
document.addEventListener("DOMContentLoaded", () => {
    const categoryButtons = document.querySelectorAll(".category-card");
    const searchInput = document.getElementById("menu-search");
    const menuCards = document.querySelectorAll(".food-card");
    const emptyMessage = document.getElementById("empty-message");

    const cartButton = document.getElementById("cart-button");
    const cartOverlay = document.getElementById("cart-overlay");
    const closeCartButton = document.getElementById("close-cart");
    const cartItemsContainer = document.getElementById("cart-items");
    const cartCount = document.getElementById("cart-count");
    const cartEmpty = document.getElementById("cart-empty");
    const cartSubtotal = document.getElementById("cart-subtotal");

    let selectedCategory = "All";
    let cart = {};

    try {
        cart = JSON.parse(localStorage.getItem("olivaCart")) || {};
    } catch {
        cart = {};
    }

    function filterMenu() {
        const searchText = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        menuCards.forEach((card) => {
            const category = card.dataset.category.toLowerCase();
            const text = card.textContent.toLowerCase();

            const matchesCategory =
                selectedCategory === "All" ||
                category === selectedCategory.toLowerCase();

            const matchesSearch = text.includes(searchText);
            card.hidden = !(matchesCategory && matchesSearch);

            if (!card.hidden) visibleCount++;
        });

        emptyMessage.hidden = visibleCount !== 0;
    }

    categoryButtons.forEach((button) => {
        button.addEventListener("click", () => {
            selectedCategory = button.dataset.category;

            categoryButtons.forEach((item) => {
                item.classList.remove("active");
            });

            button.classList.add("active");
            filterMenu();
        });
    });

    searchInput.addEventListener("input", filterMenu);

    function saveCart() {
        localStorage.setItem("olivaCart", JSON.stringify(cart));
    }

    function renderCart() {
        cartItemsContainer.replaceChildren();

        let totalItems = 0;
        let subtotal = 0;

        Object.values(cart).forEach((item) => {
            totalItems += item.quantity;
            subtotal += item.price * item.quantity;

            const row = document.createElement("div");
            row.className = "cart-item";

            const details = document.createElement("div");
            const name = document.createElement("h3");
            const price = document.createElement("p");

            name.textContent = item.name;
            price.textContent =
                `₹${item.price} × ${item.quantity}`;

            details.append(name, price);

            const quantityControls = document.createElement("div");
            quantityControls.className = "quantity-controls";

            const minus = document.createElement("button");
            minus.type = "button";
            minus.textContent = "−";
            minus.setAttribute("aria-label", `Remove one ${item.name}`);

            const quantity = document.createElement("span");
            quantity.textContent = item.quantity;

            const plus = document.createElement("button");
            plus.type = "button";
            plus.textContent = "+";
            plus.setAttribute("aria-label", `Add one ${item.name}`);

            minus.addEventListener("click", () => {
                changeQuantity(item.name, -1);
            });

            plus.addEventListener("click", () => {
                changeQuantity(item.name, 1);
            });

            quantityControls.append(minus, quantity, plus);
            row.append(details, quantityControls);
            cartItemsContainer.append(row);
        });

        cartCount.textContent = totalItems;
        cartSubtotal.textContent =
            `₹${subtotal.toLocaleString("en-IN")}`;

        cartEmpty.hidden = totalItems !== 0;
        saveCart();
    }

    function changeQuantity(name, change) {
        if (!cart[name]) return;

        cart[name].quantity += change;

        if (cart[name].quantity <= 0) {
            delete cart[name];
        }

        renderCart();
    }

    document.querySelectorAll(".add-button").forEach((button) => {
        button.addEventListener("click", () => {
            const name = button.dataset.name;
            const price = Number(button.dataset.price);

            if (!name || !Number.isFinite(price) || price < 0) return;

            if (cart[name]) {
                cart[name].quantity += 1;
            } else {
                cart[name] = {
                    name: name,
                    price: price,
                    quantity: 1
                };
            }

            renderCart();
        });
    });

    cartButton.addEventListener("click", () => {
        cartOverlay.hidden = false;
    });

    closeCartButton.addEventListener("click", () => {
        cartOverlay.hidden = true;
    });

    cartOverlay.addEventListener("click", (event) => {
        if (event.target === cartOverlay) {
            cartOverlay.hidden = true;
        }
    });

    
const checkoutButton = document.getElementById("checkout-button");
const checkoutForm = document.getElementById("checkout-form");

checkoutButton.addEventListener("click", () => {
    if (Object.keys(cart).length === 0) {
        alert("Please add an item to your bag first.");
        return;
    }

    checkoutForm.hidden = false;
    checkoutForm.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
});



    // Submit checkout form and save the order
  
    const placeOrderButton = document.getElementById("place-order-button");

    checkoutForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (Object.keys(cart).length === 0) {
            alert("Please add an item to your bag first.");
            return;
        }

        const customerName = document.getElementById("customer-name").value.trim();
        const phone = document.getElementById("customer-phone").value.trim();
        const address = document.getElementById("customer-address").value.trim();

        if (!customerName || !address || !/^[0-9]{10}$/.test(phone)) {
            alert("Please enter valid delivery details.");
            return;
        }

        const orderData = {
            customer_name: customerName,
            phone: phone,
            address: address,
            items: Object.values(cart).map((item) => ({
                name: item.name,
                quantity: item.quantity
            }))
        };

        placeOrderButton.disabled = true;
        placeOrderButton.textContent = "Placing order...";

        try {
            const response = await fetch("/place-order", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(orderData)
            });

            const result = await response.json();

            if (!response.ok) {
                alert(result.error || "Could not place your order.");
                return;
            }

       
            cart = {};
            localStorage.removeItem("olivaCart");

            window.location.href =
                `/order-confirmation/${result.order_id}`;
            return;



        } catch (error) {
            console.error("Order submission failed:", error);
            alert("Could not connect to the server. Please try again.");
        } finally {
            placeOrderButton.disabled = false;
            placeOrderButton.textContent = "Place Order";
        }
    });


    renderCart();
    filterMenu();
});
