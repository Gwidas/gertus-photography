from django.shortcuts import render
from .models import Print


def all_prints(request):
    """ A view to show all prints, including sorting and search queries """

    prints = Print.objects.all()

    context = {
        'prints': prints,
    }

    return render(request, 'prints/prints.html', context)
