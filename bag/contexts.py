from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from prints.models import Print

def bag_contents(request):
    """Counts itmes and total amount"""

    bag_items = []
    total = 0
    print_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        print_td = get_object_or_404(Print, pk=item_id)
        total += quantity * print_td.price
        print_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'print_td': print_td,
        })

    if total < settings.STANDART_DELIVERY_PRECENTAGE:
        delivery = total * Decimal(settings.STANDART_DELIVERY_PRECENTAGE / 100)

    else:
        delivery = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'delivery': delivery,
        'print_count': print_count,
        'grand_total': grand_total,
    }

    return context
