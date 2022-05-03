from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('prints'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51KjeLuDYsM1IjQsVrxsSXoej9vPOPRoBfoAhWCbv1gG5LHliSN3RVr1RivlnjSZLze2emDQphoswAwP4yD5OBzjJ002XDk2TZ4',
        'client_secret': 'test client secret', 
    }

    return render(request, template, context)
