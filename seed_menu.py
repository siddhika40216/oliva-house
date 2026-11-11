
from app import app, db, MenuItem

sample_items = [
    # PIZZAS
    {
        "name": "Margherita Pizza",
        "description": "Classic tomato, mozzarella and fresh basil.",
        "price": 249,
        "category": "Pizza",
        "image": "https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Farmhouse Pizza",
        "description": "Loaded with capsicum, onion, mushrooms and cheese.",
        "price": 299,
        "category": "Pizza",
        "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Paneer Tikka Pizza",
        "description": "Indian-style paneer tikka with a cheesy topping.",
        "price": 329,
        "category": "Pizza",
        "image": "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?auto=format&fit=crop&w=700&q=80",
    },

    # BURGERS
    {
        "name": "Classic House Burger",
        "description": "Grilled patty, crisp greens and house sauce.",
        "price": 199,
        "category": "Burgers",
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Crispy Veg Burger",
        "description": "Crispy vegetable patty with lettuce and creamy mayo.",
        "price": 169,
        "category": "Burgers",
        "image": "https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Double Cheese Burger",
        "description": "A hearty burger layered with melted cheese.",
        "price": 249,
        "category": "Burgers",
        "image": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?auto=format&fit=crop&w=700&q=80",
    },

    # HEALTHY MEALS
    {
        "name": "Garden Fresh Bowl",
        "description": "Seasonal greens, fresh vegetables and seeds.",
        "price": 179,
        "category": "Healthy",
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Mediterranean Salad",
        "description": "Fresh cucumber, tomatoes, greens and feta-style cheese.",
        "price": 219,
        "category": "Healthy",
        "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Protein Power Bowl",
        "description": "A nourishing bowl with chickpeas, greens and grains.",
        "price": 269,
        "category": "Healthy",
        "image": "https://images.unsplash.com/photo-1511690743698-d9d85f2fbf38?auto=format&fit=crop&w=700&q=80",
    },

    # DESSERTS
    {
        "name": "Chocolate Celebration Cake",
        "description": "Soft chocolate layers with rich cocoa cream.",
        "price": 159,
        "category": "Desserts",
        "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "New York Cheesecake",
        "description": "Creamy cheesecake with a buttery biscuit base.",
        "price": 189,
        "category": "Desserts",
        "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=700&q=80",
    },
    {
        "name": "Chocolate Brownie",
        "description": "Rich, fudgy chocolate brownie for a sweet treat.",
        "price": 129,
        "category": "Desserts",
        "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=700&q=80",
    },
]

with app.app_context():
    db.create_all()

    for item_data in sample_items:
        existing_item = MenuItem.query.filter_by(
            name=item_data["name"]
        ).first()

        if existing_item:
            for key, value in item_data.items():
                setattr(existing_item, key, value)
        else:
            db.session.add(MenuItem(**item_data))

    db.session.commit()

    print("Oliva House menu and food images updated successfully!")
