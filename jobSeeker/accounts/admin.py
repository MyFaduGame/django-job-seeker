from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, EmployerProfile

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('role',)}),
    )

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'location', 'verified', 'created_at')
    search_fields = ('company_name', 'user__username', 'user__email')
    list_filter = ('verified', 'location')

    actions = ['verify_employers']

    def verify_employers(self, request, queryset):
        updated = queryset.update(verified=True)
        self.message_user(request, f"{updated} employer(s) verified.")
    verify_employers.short_description = "Mark selected employers as verified"
