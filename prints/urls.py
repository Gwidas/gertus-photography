from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_prints, name='prints'),
    path('<print_id>', views.print_detail, name='print_detail'),
    path('add/', views.add_print, name='add_print'),
    path('edit/<int:print_id>/', views.edit_print, name='edit_print'),
    path('delete/<int:print_id>/', views.delete_print, name='delete_print'),
]