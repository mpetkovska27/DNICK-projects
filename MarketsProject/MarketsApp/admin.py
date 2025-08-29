from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import Market, Employee, MarketProduct, Product


# Register your models here.


class MarketProductInline(admin.StackedInline):
    model = MarketProduct
    extra = 1

class MarketAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('user_added',)
    inlines = [MarketProductInline]

    def save_model(self, request, obj, form, change):
        obj.user_added = request.user
        obj.save()
    #Не е дозволено додавање и бришење на маркети доколку корисникот не е суперкорисник
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Market, MarketAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname',)
    #при креирање на вработен, корисникот се доделува автоматски според најавениот корисник
    exclude = ('user_added',)
    def save_model(self, request, obj, form, change):
        #drug nacin za has_change_permissions
        if not change: #ako se raboti za istiot najaven, go zacuvuva vo user_added
            obj.user_added = request.user
        elif obj.user_added != request.user:
            raise PermissionDenied("Nemash pravo da go promenish vraboteniot!")
        obj.save()
    #Откако еден вработен е најавен, ќе биде дефинирам и зачуван, истиот може да се промени
    #и избрише само од корисникот кој го креирал вработениот
    def has_delete_permission(self, request, obj=None):
        if obj and obj.user_added != request.user: #ojb dali e null i uslov
            return False
        return True
    # def has_change_permission(self, request, obj=None):
    #     if obj and obj.user_added != request.user: #ojb dali e null i uslov
    #         return False
    #     return True

admin.site.register(Employee, EmployeeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('type', 'isHomemade',)
    search_fields = ('type',)
admin.site.register(Product, ProductAdmin)

