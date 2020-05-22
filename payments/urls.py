from django.urls import path
from . import views
urlpatterns = [
    path('', views.testing),
    path('confirm_order', views.create_order, name = 'create_order'),
    path('payment_status', views.payment_status, name = 'payment_status'),
]
