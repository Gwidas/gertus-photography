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

    for item_id, item_data in bag.items():
        print = get_object_or_404(Print, pk=item_id)
        total += item_data * print.price
        print_count += item_data
        bag_items.append({
            'item_id': item_id,
            'quantity': item_data,
            'print': print,
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
