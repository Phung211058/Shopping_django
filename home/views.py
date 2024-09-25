from django.shortcuts import render, get_object_or_404
from manager.models import Product  # Import model Product
from .models import Cart, CartItem, Customer_Accounts
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
# Create your views here.
def get_home(request):
    # Kiểm tra xem request.user có phải là người dùng hợp lệ hay không
    
    products = Product.objects.all()  # Lấy tất cả sản phẩm
    return render(request, 'home.html', {'products': products})
def get_shop(request):
    return render(request, 'shop.html')
def get_whyus(request):
    return render(request, 'whyus.html')
def get_testimonial(request):
    return render(request, 'testimonial.html')
def get_contact(request):
    return render(request, 'contact.html')
def product_detail(request, product_id):
    # Lấy sản phẩm từ database
    product = get_object_or_404(Product, id=product_id)
    # Truyền sản phẩm vào template
    context = {
        'product': product,
    }
    return render(request, 'detailProduct.html', context)
# @login_required(login_url='/user/get/login')
def view_cart(request):
    if not hasattr(request.user, 'is_customer'):
        return HttpResponseForbidden("You do not have permission to access this page.")
    if not request.user.is_customer:
        return HttpResponseForbidden("You do not have permission to access this page.")
    customer = get_object_or_404(Customer_Accounts, email=request.user.email)  # Hoặc bất kỳ cách nào bạn xác định người dùng
    cart, created = Cart.objects.get_or_create(customer=customer)
    items = cart.cartitem_set.all()
    {'cart': cart, 'items': items}
    return render(request, 'cart.html', )
# @login_required(login_url='/user/get/login')
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'error': 'Product ID is missing'}, status=400)

        # Lấy sản phẩm, nếu không tìm thấy sẽ trả về 404
        product = get_object_or_404(Product, id=product_id)
        
        # Kiểm tra xem customer có tồn tại không
        try:
            customer = Customer_Accounts.objects.get(email=request.user.email)
        except Customer_Accounts.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        # Lấy hoặc tạo giỏ hàng
        cart, created = Cart.objects.get_or_create(customer=customer)

        # Lấy hoặc tạo CartItem
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({'success': 'Product added to cart successfully'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
