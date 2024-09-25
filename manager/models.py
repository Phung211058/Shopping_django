from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=20)
    quantity = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')
    def __str__(self):
        return self.name
    
class Manager_Accounts(models.Model):
    email = models.EmailField(max_length=50)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_manager = models.BooleanField(default=True)  # Phân biệt loại người dùng
    last_login = models.DateTimeField(null=True, blank=True)  # Thêm trường last_login
    is_active = models.BooleanField(default=True)  # Thêm trường is_active
    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()
    @property
    def is_authenticated(self):
        # Luôn trả về True, vì đây là đối tượng người dùng đã được xác thực
        return True
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)