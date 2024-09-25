# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home, name='home'),  # Đường dẫn cho trang home
    path('shop', views.get_shop, name='shop'),  # Đường dẫn cho trang shop
    path('whyus', views.get_whyus, name='whyus'),  # Đường dẫn cho trang why us
    path('testimonial', views.get_testimonial, name='testimonial'),  # Đường dẫn cho trang testimonial
    path('contact', views.get_contact, name='contact'),  # Đường dẫn cho trang contact
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add', views.add_to_cart, name='add_cart'),
]
