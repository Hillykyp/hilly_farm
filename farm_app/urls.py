from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.BlogListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update-cart-item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
