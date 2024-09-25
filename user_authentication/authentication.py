from django.contrib.auth.backends import BaseBackend
from .models import Customer_Accounts  # Đảm bảo import mô hình của bạn
from django.utils import timezone

class CustomersBackend(BaseBackend):
    def customer_authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            customer = Customer_Accounts.objects.get(email=email)
            if customer.is_active and customer.check_password(password):
                if customer.is_customer:  # Kiểm tra xem có phải khách hàng không
                    customer.last_login = timezone.now()
                    customer.save()
                    return customer
        except Customer_Accounts.DoesNotExist:
            return None

    def get_customer(self, customer_id):
        try:
            return Customer_Accounts.objects.get(pk=customer_id)
        except Customer_Accounts.DoesNotExist:
            return None