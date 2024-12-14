from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Category, Product, Contact, BlogPost, Cart, CartItem
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart

class ProductListView(ListView):
    model = Product
    template_name = 'farm_app/products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_or_create_cart(self.request)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'farm_app/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_or_create_cart(self.request)
        return context

@require_POST
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        return JsonResponse({
            'error': 'Not enough stock available',
            'available_stock': product.stock
        }, status=400)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            return JsonResponse({
                'error': 'Not enough stock available',
                'available_stock': product.stock
            }, status=400)
        cart_item.save()
    
    return JsonResponse({
        'message': f'{product.name} added to cart',
        'cart_total': cart.get_total(),
        'cart_items': cart.get_total_items()
    })

@require_POST
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return JsonResponse({
            'message': f'{product.name} removed from cart',
            'cart_total': cart.get_total(),
            'cart_items': cart.get_total_items()
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not in cart'}, status=400)

def update_cart_item(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 0))
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if quantity <= 0:
            cart_item.delete()
            message = f'{product.name} removed from cart'
        else:
            if quantity > product.stock:
                return JsonResponse({
                    'error': 'Not enough stock available',
                    'available_stock': product.stock
                }, status=400)
            cart_item.quantity = quantity
            cart_item.save()
            message = f'{product.name} quantity updated'
        
        return JsonResponse({
            'message': message,
            'cart_total': cart.get_total(),
            'cart_items': cart.get_total_items()
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not in cart'}, status=400)

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'farm_app/cart.html', {'cart': cart})

def home(request):
    featured_products = Product.objects.all()[:4]
    return render(request, 'farm_app/home.html', {
        'featured_products': featured_products,
        'cart': get_or_create_cart(request)
    })

class BlogListView(ListView):
    model = BlogPost
    template_name = 'farm_app/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = BlogPost.objects.filter(is_featured=True)[:3]
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'farm_app/blog_detail.html'
    context_object_name = 'post'

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for your message. We will get back to you soon!')
        return redirect('contact')
    
    return render(request, 'farm_app/contact.html')
