from django.shortcuts import render
from .models import Product, Manager_Accounts
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from .authentication import ManagersBackend
from django.http import HttpResponseForbidden

# Create your views here.
@login_required(login_url='/manage/get/login')
def get_index(request):
    if not request.user.is_manager:
        return HttpResponseForbidden("You do not have permission to access this page.")
    return render(request, 'index.html')
def get_product(request):
    return render(request, 'productManagement.html')
def get_login(request):
    return render(request, 'loginManager.html')
def get_register(request):
    return render(request, 'registerManager.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        cfpassword = request.POST.get('cfpassword')
        # check if email existed
        if Manager_Accounts.objects.filter(email=email).exists():
            return JsonResponse({'error': 'email already exists'}, status=400)
        # check if cfpassword matched
        if password != cfpassword:
            return JsonResponse({'error': 'Confirm password does not match'}, status=400)
        # create account and save in database
        new_user = Manager_Accounts(
            email=email,  password=make_password(password)
        )
        new_user.save()
        return JsonResponse({'success': 'Registration successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Sử dụng phương thức authenticate
        user = ManagersBackend().manager_authenticate(request, email=email, password=password)
        if user:
            user.backend = 'manager.authentication.ManagersBackend'  # Đặt đúng đường dẫn đến backend của bạn
            # Xác thực thành công, đăng nhập người dùng
            auth_login(request, user) # dùng login của django để lưu session
            return JsonResponse({'success': 'Login successful'}, status=200)
        else:
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
# def login(request):
#     if(request.method == 'POST'):
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         try:
#             user = Accounts.objects.get(email=email)
#             if check_password(password, user.password):
#             # Xác thực thành công, đăng nhập người dùng
#                 auth_login(request, user, backend='manager.authentication.AccountsBackend')
#                 return JsonResponse({'success': 'Login successful'}, status=200)
#             else:
#                 return JsonResponse({'error': 'Invalid email or password'}, status=400)
#         except Accounts.DoesNotExist:
#             return JsonResponse({'error': 'Email or password is incorrect'}, status=400)
#     return JsonResponse({'error': 'Invalid mehod!'}, status=405)

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('Image')
        new_product = Product.objects.create(
            name=name, 
            category=category, 
            description=description, 
            price=price, 
            quantity=quantity, 
            image=image, 
        )
        new_product.save()
        return JsonResponse({'success': 'Create Product Success'}, status = 200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_all_products(request):
    if request.method == 'GET':
        # Lấy từ khóa tìm kiếm từ query params, nếu không có thì để trống
        query = request.GET.get('q', '')
        # Nếu có từ khóa tìm kiếm, lọc theo từ khóa
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(category__icontains=query) | 
                Q(description__icontains=query)
            )
        else:
            # Nếu không có từ khóa, lấy tất cả sản phẩm
            products = Product.objects.all()
        # Chuyển đổi danh sách sản phẩm thành định dạng JSON
        data = [
            {
            'id': product.id, 
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'price': product.price,
            'quantity': product.quantity,
            'image_url': product.image.url if product.image else None,  # Đường dẫn tới ảnh của sản phẩm
            }
        for product in products
        ]
        return JsonResponse({'products': data}, status=200)
def delete_product(request, product_id):
    if request.method == 'DELETE':  # Sử dụng phương thức DELETE
        try:
            product = Product.objects.get(id=product_id)
            # Kiểm tra và xóa file hình ảnh nếu nó tồn tại
            # if product.image:
            #     image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
            #     if os.path.isfile(image_path):
            #         os.remove(image_path)
            product.delete()
            return JsonResponse({'success': 'Product deleted successfully'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def update_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    if(request.method == 'POST'):
            # lấy dữ liệu từ form
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('Image')
        # Cập nhật thông tin sản phẩm
        product.name = name
        product.category = category
        product.description = description
        product.price = price
        product.quantity = quantity
        if image:
            product.image = image
        product.save()
        return JsonResponse({'success': 'Product updated successfully'}, status=200)
    else: 
        data = {
            'id': product.id,  # Thêm id vào dữ liệu trả về
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'price': product.price,
            'quantity': product.quantity,
            'image_url': product.image.url,  # Đường dẫn tới ảnh của sản phẩm
        }
        return JsonResponse({'products': data}, status=200)
