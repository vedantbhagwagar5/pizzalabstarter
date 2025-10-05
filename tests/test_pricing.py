from src.pizza import Menu, Pizza, total_with_tax, apply_promos

def sample_menu():
    return Menu.from_yaml("data/menu.yaml")

def test_basic_pricing():
    m = sample_menu()
    p = Pizza(size="medium", toppings=["pepperoni", "onions"])
    price = m.price_pizza(p)
    # base 11 + pep 1.5 + onions 1.0 = 13.5
    assert abs(price - 13.5) < 1e-6

def test_two_large_promo_applies():
    m = sample_menu()
    pizzas = [Pizza("large", ["pepperoni"]), Pizza("large", ["extra_cheese"])]
    discount = apply_promos(m, pizzas, "LARGE2")
    # 10% of large subtotal: (14+1.5) + (14+1.75) = 31.25 → 3.13 off
    assert abs(discount - 3.13) < 1e-6

def test_order_total_with_tax_and_promo():
    m = sample_menu()
    pizzas = [Pizza("small", []), Pizza("medium", ["mushrooms"])]
    result = total_with_tax(m, pizzas, "STUDENT10")
    # subtotal = 8 + (11+1.25) = 20.25; 10% off => 18.225; tax 5.5% => 19.23
    assert result["subtotal"] == 20.25
    assert result["discount"] == 2.03  # rounded
    assert abs(result["total"] - 19.23) < 0.01
