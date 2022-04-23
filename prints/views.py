from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Print, Category


def all_prints(request):
    """ A view to show all prints, including sorting and search queries """

    prints = Print.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            prints = prints.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('prints'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            prints = prints.filter(queries)

    context = {
        'prints': prints,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'prints/prints.html', context)

def print_detail(request, print_id):
    """ A view to show individual product details """

    print_error = get_object_or_404(Print, pk=print_id)

    context = {
        'print': print_error,
    }

    return render(request, 'prints/print_detail.html', context)