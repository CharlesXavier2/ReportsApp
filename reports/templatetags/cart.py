from django import template

register = template.Library()


@register.filter
def is_in_cart(item_id, cart) :
    keys = cart.keys()
    for id in keys :
        if id == str(item_id) : return True
    return False

@register.filter
def cart_quantity(item_id, cart) :
    keys = cart.keys()
    for id in keys :
        if id == str(item_id) : return cart[id]
    return 0