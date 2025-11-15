import json

# ==========================
# Custom Exceptions
# ==========================

class InvalidRoomTypeError(Exception):
    pass

class NotEnoughBedsError(Exception):
    pass


# ==========================
# Room & Data Storage
# ==========================

rooms = {
    "single": {"available": 3, "price": 200},
    "double": {"available": 2, "price": 350},
    "family": {"available": 1, "price": 500}
}

customers = set()
history = []


# ==========================
# Admin Credentials
# ==========================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"


# ==========================
# Decorators
# ==========================

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executing {func.name}...")
        result = func(*args, **kwargs)
        print(f"[LOG] Completed {func.name}.")
        return result
    return wrapper


# ==========================
# Higher Order Function
# ==========================

def apply_discount(discount):
    def price_calculator(price):
        return price - (price * discount)
    return price_calculator


# ==========================
# Booking Logic
# ==========================

@log_action
def book_room(room_type, quantity):
    if room_type not in rooms:
        raise InvalidRoomTypeError("Invalid room type")

    available = rooms[room_type]["available"]
    if quantity > available:
        raise NotEnoughBedsError(f"Only {available} rooms available")

    # discount: 10%
    discount_func = apply_discount(0.10)
    final_price = discount_func(rooms[room_type]["price"]) * quantity

    rooms[room_type]["available"] -= quantity

    return {
        "room_type": room_type,
        "quantity": quantity,
        "price": final_price
    }


# ==========================
# Admin Functions
# ==========================

def admin_login():
    username = input("\nAdmin username: ")
    password = input("Admin password: ")
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD


def admin_menu():
    print("""
--- Admin Menu ---
1. View all rooms
2. View booking history
3. Add new room type
4. Delete room type
5. Update room availability
6. Save data to JSON file
7. Exit admin
""")


def view_rooms():
    print("\n--- Rooms ---")
    for room, info in rooms.items():
        print(f"{room}: {info}")


def view_history():
    print("\n--- Booking History ---")
    for h in history:
        print(h)


def add_room_type():
    room = input("Enter new room name: ").lower()
    price = int(input("Enter price: "))
    quantity = int(input("Enter availability: "))
    rooms[room] = {"available": quantity, "price": price}
    print(f"Room '{room}' added!")


def delete_room_type():
    room = input("Enter room name to delete: ").lower()
    if room in rooms:
        del rooms[room]
        print(f"Room '{room}' deleted!")
    else:
        print("Room does not exist.")


def update_room_quantity():
    room = input("Enter room type: ").lower()
    if room in rooms:
        qty = int(input("Enter new quantity: "))
        rooms[room]["available"] = qty
        print("Updated successfully.")
    else:
        print("Room not found.")


def save_to_json():
    data = {
        "rooms": rooms,
        "bookings": history
    }
    with open("hotel_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Data saved to hotel_data.json")


# ==========================
# Main Booking System
# ==========================

def user_booking_system():
    while True:
        print("\nType 'admin' for admin login.")
        print("Type 'exit' to exit.")
        print()

        choice = input("Continue or admin? ").lower()

        if choice == "exit":
            break

        if choice == "admin":
            if admin_login():
                run_admin_panel()
            else:
                print("Invalid admin credentials.")
            continue

        name = input("Enter your name: ").strip()
        customers.add(name)
        room_type = input("Enter room type: ").lower()
        quantity = int(input("Number of beds: "))

        try:
            record = book_room(room_type, quantity)
            history.append(record)
            print("Booking successful:", record)
        except Exception as e:
            print("Error:", e)

    print("\nSystem closed.")
    print("Customers:", customers)


# ==========================
# Admin Panel Loop
# ==========================

def run_admin_panel():
    while True:
        admin_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            view_rooms()
        elif choice == "2":
            view_history()
        elif choice == "3":
            add_room_type()
        elif choice == "4":
            delete_room_type()
        elif choice == "5":
            update_room_quantity()
        elif choice == "6":
            save_to_json()
        elif choice == "7":
            break
        else:
            print("Invalid option")


# ==========================
# RUN SYSTEM
# ==========================

user_booking_system()