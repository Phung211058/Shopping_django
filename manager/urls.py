# home/urls.py
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.get_index, name='index'),  # Đường dẫn cho trang home
    path('get/login', views.get_login, name='get_login'),  # Đường dẫn cho trang login
    path('get/register', views.get_register, name='get_register'),  # Đường dẫn cho trang register
    path('login', views.login, name='login_manager'),  # Chức năng login
    path('register', views.register, name='register_manager'),  # Chắc năng register
    path('logout/', views.logout, name='logout'), # Đăng xuất
    path('product', views.get_product, name='product'),  # Đường dẫn cho trang product list
    path('create_product', views.create_product, name='create_product'),  # Tạo product mới
    path('get_all_products', views.get_all_products, name='get_all_products'), # Hiển thị sản phẩm
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'), # Xóa sản phẩm
    path('update_product/<int:product_id>/', views.update_product, name='update_product'), # Sửa sản phẩm
] 