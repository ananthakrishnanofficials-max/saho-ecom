"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ( account_view, category_detail, fashion_view, live_search, orders_view, register_view, login_view, home,settings_view,product_details,
    fashion_page, electronics, healthcare, grocery, about, subcategory_products, toggle_wishlist,user_logout,cart,add_to_cart,checkout,increase_qty,decrease_qty,remove_cart,payment_view,payment_success,payment_failed,category_page,category_products,festival_list,festival_detail,
)
from myecom import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/', views.chatbot, name='chatbot'),
    path('products/', views.product_list, name='product_list'),
    path('saho-plus/', views.saho_plus_view, name='saho_plus'),
    path('addresses/', views.addresses_view, name='addresses'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('payment-options/', views.payment_options_view, name='payment_options'),
    path("bot/", views.chatbot_view, name="chatbot"),
    path('bot/', views.chatbot, name='chatbot'),
    path('mobile/', views.mobile, name='mobile'),
    # Add this right next to your other wishlist URL
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('category/<str:category_name>/', category_page, name='category'),
    path("subcategory/<slug:slug>/",subcategory_products,name="subcategory_products"),
    path('payment/<int:product_id>/', payment_view, name='payment'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-failed/', payment_failed, name='payment_failed'),
    path('cart/', cart, name='cart'),
    path('increase_qty/<int:item_id>/', increase_qty, name='increase_qty'),
    path('decrease_qty/<int:item_id>/', decrease_qty, name='decrease_qty'),
    path('remove_cart/<int:item_id>/', remove_cart, name='remove_cart'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('wishlist/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path("product/<int:pk>/",product_details, name="product_details"),
    path('category/<slug:slug>/', category_products, name='category_products'),
    path('register/', register_view, name='register'),
    path('live-search/', live_search, name='live_search'),
    path('logout/', user_logout, name='logout'),
    path('festival/<int:festival_id>/', festival_detail, name='festival_detail'),
    path('festival/', festival_list, name='festival'),
    path("category/<int:category_id>/", category_detail, name="category_detail"),
    path('homedecor/', views.home_decor, name='homedecor'),
    path("category/<slug:category_slug>/", views.category_page, name="category_page"),

    path('fashion/', fashion_page, name='fashion'),
    path("fashion/", fashion_view, name="fashion"),
    path('electronics/', electronics, name='electronics'),
    path('healthcare/', healthcare, name='healthcare'),
    path('grocery/', grocery, name='grocery'),
    path("products/", views.product_list, name="product_list"),
    path('about/', about, name='about'), 
    path('account/', account_view, name='account'),
    path('orders/', orders_view, name='orders'),
    path('settings/', settings_view, name='settings'),
    path('login/', login_view, name='login'),
    path('', home, name='home'),# Default route to home page
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

                       

  