# 🍽️ Restaurant Management API

A Django REST Framework API for managing a restaurant's backend operations including categories, menu items, ingredients, orders, reservations, and user roles.

---

## 🚀 Features

- 📦 Organize food items into categories
- 🧂 Track ingredients with quantities, units, and stock thresholds
- 🍲 Build menu items from ingredients with images and prices
- 🛒 Handle food orders with related items and quantities
- 📅 Manage table reservations with status and time
- 👥 Support role-based access for:
  - `Admin`: Full access
  - `Staff`: Manage orders, reservations, and availability
  - `Customer`: View menu, make reservations and orders

---

## 🧱 Models Overview

- **Category**: Groups menu items (e.g., Main Courses, Desserts)
- **Table**: Represents physical restaurant tables
- **Ingredient**: Stock items used to prepare menu dishes
- **MenuItem**: A dish with a price, description, image, and ingredient breakdown
- **IngredientItem**: Links ingredients to a menu item and amount used
- **Order**: Records customer orders with status, time, and items
- **Reservation**: Customer table bookings with date/time
- **Users**: Role-based permissions for admin, staff, and customers

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/m7mad-ayman/Resturant-API.git
   cd Resturant-API
   
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create a superuser (Django admin)**:
   ```bash
   python manage.py createsuperuser

6. **Run the server**:
   ```bash
   python manage.py runserver
