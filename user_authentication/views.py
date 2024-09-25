from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Customer_Accounts
from .authentication import CustomersBackend
from django.contrib.auth import login as auth_login, logout as auth_logout
import logging
logger = logging.getLogger(__name__)

# Create your views here.    
def get_register(request):
    return render(request, 'register.html')
def get_login(request):
    return render(request, 'login.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cfpassword = request.POST.get('cfpassword')

        # check if email existed
        if Customer_Accounts.objects.filter(email=email).exists():
            return JsonResponse({'error': 'email already exists'}, status=400)
        # check if cfpassword matched
        if password != cfpassword:
            return JsonResponse({'error': 'Confirm password does not match'}, status=400)
        # create account and save in database
        new_customer = Customer_Accounts(
            email=email, phone=phone, password=make_password(password)
        )
        new_customer.save()
        return JsonResponse({'success': 'Registration successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def login(request):
    logger.info("Login attempt received")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        logger.info(f"Email: {email}, Password: {password}")
        # Sử dụng phương thức authenticate
        user = CustomersBackend().customer_authenticate(request, email=email, password=password)
        print(user.is_active, user.is_customer)
        if user:
            logger.info(f"User {user.email} authenticated successfully.")
            user.backend = 'user_authentication.authentication.CustomersBackend'  # Đặt đúng đường dẫn đến backend của bạn
            # Xác thực thành công, đăng nhập người dùng
            auth_login(request, user) # dùng login của django để lưu session
            return JsonResponse({'success': 'Login successful'}, status=200)
        else:
            logger.warning("Authentication failed.")
            return JsonResponse({'error': 'Invalid email or password'}, status=400)
    return JsonResponse({'error': 'Invalid method!'}, status=405)

def logout(request):
    if request.method == 'POST':
        try:
            auth_logout(request)
            return JsonResponse({'success': True, 'message': 'You have successfully logged out.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)