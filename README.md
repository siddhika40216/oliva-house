# Oliva House

A web-based food ordering platform built with Flask, designed to provide a simple ordering experience for customers and an organised management interface for restaurant administrators.

Oliva House brings together menu browsing, cart management, online order placement and order tracking in one application. It also includes an admin panel for managing menu items and handling incoming customer orders.

## Features

### Customer Interface
- **Dynamic Food Menu:** Browse food items organised by categories.
- **Search and Filter:** Find dishes using the search bar and category filters.
- **Shopping Cart:** Add items, update quantities and remove products before checkout.
- **Order Placement:** Submit orders with customer details and delivery address.
- **Order Confirmation:** Receive an order ID after successful placement.
- **Order Tracking:** Track order details and monitor status using the order ID and registered phone number.

### Admin Panel
- **Admin Authentication:** Protected admin login and logout functionality.
- **Order Management:** View customer orders, contact details, ordered items and order totals.
- **Status Management:** Update orders through Pending, Preparing, Out for Delivery, Delivered and Cancelled.
- **Menu Management:** Perform CRUD (Create, Read, Update and Delete) operations on food items.
- **Availability Control:** Enable or disable menu items without deleting them.
- **Menu Search:** Search existing food items by name or category.

### Order Processing
- Server-side validation of customer and order details.
- Menu prices are retrieved from the database during order processing.
- Order details and individual order items are stored in the database.
- Order placement time and estimated delivery time are recorded.
- Database transactions and rollback handling for failed order operations.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database integration and ORM |
| SQLite | Relational database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layouts |
| JavaScript | Cart operations, search and interactive functionality |
| Jinja2 | Dynamic HTML rendering |

## Project Structure

```text
oliva-house/
│
├── app.py
├── seed_menu.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── admin_login.html
│   ├── admin_orders.html
│   ├── admin_menu.html
│   ├── order_confirmation.html
│   └── track_order.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
└── README.md
```

## Getting Started

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/siddhika40216/oliva-house.git
cd oliva-house
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Set the admin password before starting the application.

For Windows PowerShell:

```powershell
$env:OLIVA_ADMIN_PASSWORD = "your_admin_password"
```

You can also configure the Flask secret key:

```powershell
$env:OLIVA_SECRET_KEY = "your_secret_key"
```

Use your own secure values. Do not commit credentials or secret keys to the repository.

### 5. Initialise the menu data

If setting up a fresh database, run the menu seeding script:

```bash
python seed_menu.py
```

### 6. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## Application Routes

| Route | Description |
|---|---|
| `/` | Customer home page and food menu |
| `/place-order` | Processes customer orders |
| `/track-order` | Order tracking page |
| `/admin/login` | Admin login |
| `/admin/orders` | Admin order management |
| `/admin/menu` | Menu management |

## Database

The application uses SQLite with Flask-SQLAlchemy to manage menu items, customer orders and order details.

The database file is maintained locally and excluded from version control to avoid exposing customer information or local order records.

## Security and Validation

- Admin access is protected through session-based authentication.
- Customer phone numbers are validated before order placement.
- Menu availability is checked on the server.
- Order prices are calculated using database values rather than client-submitted prices.
- Invalid order data is rejected before database insertion.
- Database rollback handling is used when order processing fails.

## Future Improvements

- Online payment gateway integration.
- Email or SMS order notifications.
- Production deployment with a managed database.
- Improved admin analytics and sales reports.

## Author

**Siddhika Srivastava**

B.Tech Computer Science and Engineering

[GitHub](https://github.com/siddhika40216)

---

*Oliva House — A restaurant ordering and management web application.*