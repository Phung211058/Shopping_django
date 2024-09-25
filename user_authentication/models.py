from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Customer_Accounts(models.Model):
    email = models.EmailField(max_length=50, )
    phone = models.CharField(max_length=10,  )
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_customer = models.BooleanField(default=True)
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

class Customer_Address(models.Model):
    customer = models.ForeignKey(Customer_Accounts, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=10, )
    city = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    commune = models.CharField(max_length=30)
    detail_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
