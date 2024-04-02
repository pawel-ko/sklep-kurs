from shop.store import Store
from shop.persistence import load_inventory, save_inventory
from shop import user_interface


def run_homework():
    Store.AVAILABLE_PRODUCTS = load_inventory()
    user_interface.handle_customer()
    save_inventory(Store.AVAILABLE_PRODUCTS)


if __name__ == '__main__':
    run_homework()
