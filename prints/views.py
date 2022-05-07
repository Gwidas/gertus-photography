from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Print, Category
from .forms import PrintForm


def all_prints(request):
    """ A view to show all prints, including sorting and search queries """

    prints = Print.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                prints = prints.annotate(lower_name=Lower('name'))

                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = f'-{sortkey}'
                prints = prints.order_by(sortkey)

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

    current_sorting = f'{sort}_{direction}'

    context = {
        'prints': prints,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'prints/prints.html', context)


def print_detail(request, print_id):
    """ A view to show individual print details """

    print = get_object_or_404(Print, pk=print_id)

    context = {
        'print': print,
    }

    return render(request, 'prints/print_detail.html', context)


@login_required
def add_print(request):
    """ Add a print to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you have no Admin rights to do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES)
        if form.is_valid():
            print = form.save()
            messages.success(request, 'Successfully added print!')
            return redirect(reverse('print_detail', args=[print.id]))
        else:
            messages.error(request, 'Failed to add print. Please ensure the form is valid.')
    else:
        form = PrintForm()
        
    template = 'prints/add_print.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_print(request, print_id):
    """ Edit a print in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you have no Admin rights to do that.')
        return redirect(reverse('home'))

    print = get_object_or_404(Print, pk=print_id)
    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES, instance=print)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated print!')
            return redirect(reverse('print_detail', args=[print.id]))
        else:
            messages.error(request, 'Failed to update print. Please ensure the form is valid.')
    else:
        form = PrintForm(instance=print)
        messages.info(request, f'You are editing {print.name}')

    template = 'prints/edit_print.html'
    context = {
        'form': form,
        'print': print,
    }

    return render(request, template, context)


@login_required
def delete_print(request, print_id):
    """ Delete a print from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you have no Admin rights to do that.')
        return redirect(reverse('home'))

    print = get_object_or_404(Print, pk=print_id)
    print.delete()
    messages.success(request, 'Print deleted!')
    return redirect(reverse('prints'))