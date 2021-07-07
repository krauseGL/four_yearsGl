from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal information', {'fields': ['first_name', 'last_name', 'patronymic', 'date_of_birth', 'series_passport', 'number_passport', 'school']}),

    )

    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_address', 'status', 'creature_date', )
    list_filter = ('status', 'creature_date', )
    pass


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

