from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('cart/',views.ShopCart,name='cart'),
    path('checkout/',views.CartCheckout,name='checkout'),
    path('detail/<pk>',views.CartDetail,name='detail'),
    path('search/',views.search,name='search'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('setting/',views.AccountInfo,name='setting'),
 ]