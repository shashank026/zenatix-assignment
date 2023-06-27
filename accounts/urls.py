from django.urls import path
from accounts.views import AdminAddProduct, AdminBlockUnblockUser, AdminChangeOrderStatusView, AdminUpdateProductDetails, admindashboard, login_page, profile, register_page, activate_email, logout, add_to_cart, cart, remove_cart_item, placedOrder, adminlogin

urlpatterns = [
    path('login/', login_page, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register_page, name="register"),
    path('activate/<email_token>/', activate_email, name="activate_email"),
    path('cart/', cart, name='cart'),
    path('cart/<uid>/', add_to_cart, name='add_to_cart'),
    path('remove-cart/<cart_item_uid>/',
         remove_cart_item, name='remove_cart_item'),
    path('profile/', profile, name='user_profile'),
    path('place-order/', placedOrder, name='place_order'),
    path('admin-login/', adminlogin, name='admin_login'),
    path('admin/user-dashboard/', admindashboard, name='admin_dashboard'),
    path('api/admin/orders/status/', AdminChangeOrderStatusView, name="admin_order_status_change"),
    path('api/admin/block-user/', AdminBlockUnblockUser, name='admin_block_user'),
    path('api/admin/add-product/', AdminAddProduct, name='admin_add_product'),
    path('api/admin/update-product/', AdminUpdateProductDetails, name='update_product_details'),
]
