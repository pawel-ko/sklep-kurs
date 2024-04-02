from enum import Enum

from shop.errors import TemporaryOutOfStock, ProductNotAvailable, NotValidInput
from shop.order import Order
from shop.persistence import save_order_in_file, show_history_orders
from shop.store import Store


class Action(Enum):
    NEW_ORDER = "1"
    HISTORY = "2"


def handle_customer():
    say_hello()
    selected_action = select_action()
    if selected_action is Action.NEW_ORDER:
        order = init_order()
        while want_more_products():
            add_product_to_order(order, Store.AVAILABLE_PRODUCTS)
        print_order_summary(order)
        save_order_in_file(order)
    else:
        show_history_orders()


def select_action():
    selected_action = input("Nowe zamówienie - 1; historia zamówienień - 2 ")
    try:
        return Action(selected_action.strip())
    except ValueError:
        print("Wybrano inną odpowiedź. Domyślny wybór to nowe zamówienie.")
        return Action.NEW_ORDER


def say_hello():
    print("Witaj w naszym sklepie!")


def init_order():
    customer_name = input("Imie: ")
    customer_last_name = input("Nazwisko: ")
    return Order(customer_name, customer_last_name)


def want_more_products():
    selection = input("Czy chcesz dodać produkty do zamówienia? T/N: ")
    if selection.upper() != "T" and selection.upper() != "N":
        print("Opcje są tylko dwie - zakładam, że chcesz coś zamówić ;)")
        return True
    return selection.upper() == "T"


def add_product_to_order(order, available_products):
    print("Oto dostępne produkty:")
    for index, available_product in enumerate(available_products):
        print(f"{index}) {available_product.product}")

    try:
        product_index_str = input("Wybierz numer: ")
        product_index = parse_product_index(product_index_str, max_index=len(available_products) - 1)

        quantity_str = input("Podaj liczbę sztuk: ")
        quantity = parse_quantity(quantity_str)
    except NotValidInput as input_error:
        print(f"Wystąpił błąd. {input_error}")
        return

    try:
        order.add_product_to_order(available_products[product_index].product, quantity)
    except TemporaryOutOfStock as error:
        print(f"Niestety mamy dostępne tylko {error.available_quantity} sztuk produktu {error.product_name}")
    except ProductNotAvailable as error:
        print(f"Produkt {error.product_name} nie jest dostępny. Wybierz inny.")


def parse_product_index(product_index_str, max_index):
    try:
        product_index = int(product_index_str)
    except ValueError:
        raise NotValidInput(f"Numer produktu powinien być liczbą.")

    if not 0 <= product_index <= max_index:
        raise NotValidInput(f"Numer produktu powienien mieścić się w przedziale 0 - {max_index}")

    return product_index


def parse_quantity(quantity_str):
    try:
        quantity = int(quantity_str)
    except ValueError:
        raise NotValidInput(f"Podana wartośc nie jest liczbą")

    if quantity <= 0:
        raise NotValidInput(f"Należy podać wartość większą od 0.")

    return quantity


def print_order_summary(order):
    print("Twoje zamówienie to:")
    print(order)
    print("Dziękujemy i zapraszamy ponownie!")
