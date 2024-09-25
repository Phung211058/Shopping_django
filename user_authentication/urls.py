from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get/login', views.get_login, name='get_login'),  # Đường dẫn cho trang login
    path('login', views.login, name='login_customer'),  # xử lý chức năng login
    path('get/register', views.get_register, name='get_register'),  # Đường dẫn cho trang register
    path('register', views.register, name='register_customer'),  # xử lý chức năng register
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)