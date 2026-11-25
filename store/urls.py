
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('plants/', views.plants, name='plants'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('cart/', views.cart_view, name='cart'),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/remove/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'cart/update/<int:product_id>/',
        views.update_cart,
        name='update_cart'
    ),

    path('signin/', views.signin, name='signin'),

    path('signup/', views.signup, name='signup'),

    path('signout/', views.signout, name='signout'),
]