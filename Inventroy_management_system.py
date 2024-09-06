import time

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, amount):
        self.quantity += amount

    def calculate_total_value(self):
        return self.price * self.quantity


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.product_id not in self.products:
            self.products[product.product_id] = product
        else:
            self.products[product.product_id].update_quantity(product.quantity)

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]

    def update_stock(self, product_id, quantity):
        if product_id in self.products:
            self.products[product_id].update_quantity(quantity)

    def get_inventory_value(self):
        total_value = 0
        for product in self.products.values():
            total_value += product.calculate_total_value()
        return total_value

    def get_product(self, product_id):
        if product_id in self.products:
            return self.products[product_id]
        return None

    def display_inventory(self):
        for product in self.products.values():
            print(f"ID: {product.product_id}, Name: {product.name}, Price: {product.price}, Quantity: {product.quantity}")


class Transaction:
    def __init__(self, inventory):
        self.inventory = inventory
        self.sales_log = []

    def buy_product(self, product_id, quantity):
        product = self.inventory.get_product(product_id)
        if product and product.quantity >= quantity:
            product.update_quantity(-quantity)
            total_cost = product.price * quantity
            self.sales_log.append({
                'product_id': product_id,
                'product_name': product.name,
                'quantity': quantity,
                'total_cost': total_cost,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            return total_cost
        return 0

    def restock_product(self, product_id, quantity):
        product = self.inventory.get_product(product_id)
        if product:
            product.update_quantity(quantity)

    def display_sales_log(self):
        if not self.sales_log:
            print("No sales have been made yet.")
        for sale in self.sales_log:
            print(f"Product ID: {sale['product_id']}, Name: {sale['product_name']}, "
                  f"Quantity Sold: {sale['quantity']}, Total: {sale['total_cost']}, Date: {sale['timestamp']}")


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role


def main_menu(role):
    if role == 'admin':
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Update Stock")
        print("4. View Inventory")
        print("5. View Total Inventory Value")
        print("6. View Sales Log")
        print("7. Exit")
    elif role == 'customer':
        print("1. Buy Product")
        print("2. View Inventory")
        print("3. Exit")
    return input("Select an option: ")


def get_product_details():
    while True:
        try:
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            return Product(product_id, name, price, quantity)
        except ValueError:
            print("Invalid input. Please enter valid price and quantity.")


def login():
    while True:
        username = input("Enter your username: ")
        role = input("Enter role (admin/customer): ").lower()
        if role in ['admin', 'customer']:
            return User(username, role)
        print("Invalid role. Please enter 'admin' or 'customer'.")


def main():
    inventory = Inventory()
    transaction = Transaction(inventory)
    user = login()

    while True:
        choice = main_menu(user.role)
        if user.role == 'admin':
            if choice == '1':
                product = get_product_details()
                inventory.add_product(product)
            elif choice == '2':
                product_id = input("Enter product ID to remove: ")
                inventory.remove_product(product_id)
            elif choice == '3':
                product_id = input("Enter product ID to update stock: ")
                quantity = int(input("Enter quantity to add or subtract: "))
                inventory.update_stock(product_id, quantity)
            elif choice == '4':
                inventory.display_inventory()
            elif choice == '5':
                total_value = inventory.get_inventory_value()
                print(f"Total inventory value: {total_value}")
            elif choice == '6':
                transaction.display_sales_log()
            elif choice == '7':
                break
            else:
                print("Invalid option, try again.")
        elif user.role == 'customer':
            if choice == '1':
                product_id = input("Enter product ID to buy: ")
                quantity = int(input("Enter quantity to buy: "))
                cost = transaction.buy_product(product_id, quantity)
                if cost > 0:
                    print(f"Purchased {quantity} units. Total cost: {cost}")
                else:
                    print("Not enough stock available.")
            elif choice == '2':
                inventory.display_inventory()
            elif choice == '3':
                break
            else:
                print("Invalid option, try again.")


if __name__ == "__main__":
    main()
