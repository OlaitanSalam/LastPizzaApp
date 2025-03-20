from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Pizza, CartItem, Cart, Order,OrderItem

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "phone_number", "address",'country', )}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active", "groups", "user_permissions"),
        }),
    )
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("email",)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user', 'created_at', 'total_price')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Don't add extra blank forms


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'is_paid', 'created_at', 'updated_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__email',)
    inlines = [OrderItemInline]

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Pizza)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(CartItem)



