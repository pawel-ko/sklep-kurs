import os
import csv
import json

from shop.order import Order
from shop.order_element import OrderElement
from shop.product import ProductCategory, Product
from shop.store import AvailableProduct


def show_history_orders():
    first_name = input("Podaj imie: ")
    last_name = input("Podaj nazwisko: ")
    orders = load_orders(first_name, last_name)
    print(f"Zamówienia dla: {first_name} {last_name}")
    for order in orders:
        print(order)


def save_order_in_file(order, file_name="orders.json"):
    new_order_data = {
        "client_first_name": order.client_first_name,
        "client_last_name": order.client_last_name,
        "order_elements": [
            {
                "product": {
                    "name": order_element.product.name,
                    "category": order_element.product.category.name,
                    "unit_price": order_element.product.unit_price,
                    "identifier": order_element.product.identifier,
                },
                "quantity": order_element.quantity
            } for order_element in order.order_elements
        ],
    }
    try:
        with open(file_name, "r") as orders_file:
            orders_data = json.load(orders_file).get("orders", {})
    except FileNotFoundError:
        orders_data = {}

    client_id = f"{order.client_first_name}-{order.client_last_name}"
    if client_id not in orders_data:
        orders_data[client_id] = []
    orders_data[client_id].append(new_order_data)

    with open(file_name, "w") as orders_file:
        json.dump({"orders": orders_data}, orders_file, indent=4)


def load_orders(client_first_name, client_last_name, file_name="orders.json"):
    try:
        with open(file_name, "r") as orders_file:
            orders_by_clients_data = json.load(orders_file).get("orders", {})
    except FileNotFoundError:
        orders_by_clients_data = {}

    client_id = f"{client_first_name}-{client_last_name}"
    if client_id not in orders_by_clients_data:
        return []
    orders = orders_by_clients_data[client_id]
    return [
        Order(
            client_first_name=order["client_first_name"],
            client_last_name=order["client_last_name"],
            order_elements=[OrderElement(
                quantity=order_element["quantity"],
                product=Product(
                    name=order_element["product"]["name"],
                    category=ProductCategory[order_element["product"]["category"]],
                    unit_price=order_element["product"]["unit_price"],
                    identifier=order_element["product"]["identifier"],
                )
            ) for order_element in order["order_elements"]],
        ) for order in orders
    ]


def load_inventory():
    file_path = os.path.join("data", "inventory.csv")
    with open(file_path, newline="") as inventory_file:
        csv_reader = csv.DictReader(inventory_file)
        return [
            AvailableProduct(
                name=row["name"],
                category=ProductCategory[row["category"]],
                quantity=int(row["quantity"]),
                unit_price=float(row["unit_price"]),
                identifier=int(row["identifier"]),
            )
            for row in csv_reader
        ]


def save_inventory(current_inventory):
    file_path = os.path.join("data", "inventory.csv")
    with open(file_path, mode="w", newline="") as inventory_file:
        headers = ["name", "category", "unit_price", "identifier", "quantity"]
        csv_writer = csv.DictWriter(inventory_file, fieldnames=headers)
        csv_writer.writeheader()
        for available_product in current_inventory:
            product = available_product.product
            csv_writer.writerow(
                {
                    "name": product.name,
                    "category": product.category.name,
                    "quantity": available_product.quantity,
                    "unit_price": product.unit_price,
                    "identifier": product.identifier,
                }
            )


def save_order_in_file_txt(order):
    file_path = os.path.join("data", "orders.txt")
    with open(file_path, mode="a") as order_file:
        order_file.write(str(order))
        order_file.write("\n")