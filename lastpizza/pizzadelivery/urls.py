from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('add_to_cart/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pizza_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete_from_cart/<int:pizza_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('billing', views.billing, name='billing'),
    path('profile', views.profile, name='profile'),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path('order-failed', views.order_failed, name='order_failed'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="passwordreset/password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="passwordreset/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="passwordreset/password_rest_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="passwordreset/reset_complete.html"), name='password_reset_complete'),
    path('fancybutton', views.fancybutton, name='fancybutton'),
    

   
   
]
