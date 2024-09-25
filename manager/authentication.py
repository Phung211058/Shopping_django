from django.contrib.auth.backends import BaseBackend
from .models import Manager_Accounts  # Đảm bảo import mô hình của bạn
from django.utils import timezone

class ManagersBackend(BaseBackend):
    def manager_authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            account = Manager_Accounts.objects.get(email=email)
            if account.is_active and account.check_password(password):
                if account.is_manager:  # Kiểm tra xem có phải quản lý không
                    account.last_login = timezone.now()
                    account.save()
                    return account
        except Manager_Accounts.DoesNotExist:
            return None

    def get_user(self, account_id):
        try:
            return Manager_Accounts.objects.get(pk=account_id)
        except Manager_Accounts.DoesNotExist:
            return None
