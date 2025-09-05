from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError

from .models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('contact', 'is_baker', )}),
    )
    def has_delete_permission(self, request, obj = ...):
        return request.user.is_superuser
    def has_change_permission(self, request, obj = ...):
        return request.user.is_superuser
    def has_add_permission(self, request):
        return request.user.is_superuser

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            bakers = models.Count('cake')
        ).filter(bakers__lt=5)

admin.site.register(CustomUser, CustomUserAdmin)

class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'baker')
    exclude = ('baker',)

    def save_model(self, request, obj, form, change):
        obj.baker = request.user
        if not change:
            # if request.user.is_baker:
                cakes_per_baker = Cake.objects.filter(baker=request.user)
                #Вкупната цена на тортите на еден пекар не смее да надминува 10 000.
                num_cakes = cakes_per_baker.count() #site cakes od 1 baker
                sum=0
                for cake in cakes_per_baker:
                    sum+=cake.price
                sum+=obj.price
                if sum>=10000:
                    raise ValidationError("Вкупната цена на тортите на еден пекар не смее да надминува 10 000.")
                #Еден пекар може да има максимум 10 торти во дадено време.

                if cakes_per_baker.count() > 10:
                    raise ValidationError("Еден пекар може да има максимум 10 торти во дадено време.")
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        return True
    def has_view_permission(self, request, obj=...):
        return True

    def has_add_permission(self, request):
        return request.user.is_authenticated and getattr(request.user, 'is_baker', False)
    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and getattr(request.user, 'is_baker', False)
    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and getattr(request.user, 'is_baker', False)

admin.site.register(Cake, CakeAdmin)