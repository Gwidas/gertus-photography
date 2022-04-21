from django.shortcuts import render, get_object_or_404
from .models import Print


def all_prints(request):
    """ A view to show all prints, including sorting and search queries """

    prints = Print.objects.all()

    context = {
        'prints': prints,
    }

    return render(request, 'prints/prints.html', context)

def print_detail(request, print_id):
    """ A view to show individual product details """

    print = get_object_or_404(Print, pk=print_id)

    context = {
        'print': print,
    }

    return render(request, 'prints/print_detail.html', context)