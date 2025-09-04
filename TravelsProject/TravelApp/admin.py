from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError

from .models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields':('contact', 'is_guide')}),
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            travels=models.Count('travel'),
        ).filter(travels__lt=3)

admin.site.register(CustomUser, CustomUserAdmin)

class TravelAdmin(admin.ModelAdmin):
    list_display = ('destination', 'price', 'creator')
    exclude = ('creator', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user

            if request.user.is_guide:
                # proverka za destinacija so isto ime
                if Travel.objects.filter(destination=obj.destination).exists():
                    raise ValidationError(f"Патувањето со дестинација '{obj.destination}' веќе постои.")
                #proverka za max 5 destinacii
                travel_count = Travel.objects.filter(creator=request.user).count()
                if travel_count>=5:
                    raise ValidationError("Туристички водич може да има максимум 5 активни дестинации.")
                #proverka za vkupna cenaa <=50 000
                total_price = Travel.objects.filter(creator=request.user).aggregate(
                    total = models.Sum('price')
                )['total'] or 0
                if total_price + (obj.price or 0)>50000:
                    raise ValidationError(f"Вкупната цена на дестинациите за еден туристички водич не смее да изнесува повеќе од 50 000")
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        if request.user.is_superuser and getattr(request.user, 'is_guide', False):
            return True
        return request.user.is_authenticated
    def has_view_permission(self, request, obj = ...):
        if request.user.is_superuser and getattr(request.user, 'is_guide', False):
            return True
        return request.user.is_authenticated
    def has_add_permission(self, request):
        return request.user.is_authenticated and getattr(request.user, 'is_guide', False)
    def has_change_permission(self, request, obj=None):
        if not (request.user.is_authenticated and getattr(request.user, "is_guide", False)):
            return False
        if obj is None:
            return True
        return obj.creator == request.user








admin.site.register(Travel, TravelAdmin)