from django.contrib import admin
from django.utils import timezone

from NedvizninaApp.models import Characteristic, RealEstate, Agent, AgentRealEstate, CharacteristicRealEstate


# Register your models here.
class AgentRealEstateInline(admin.StackedInline):
    model = AgentRealEstate
    extra = 0

class CharacteristicRealEstateInline(admin.StackedInline):
    model = CharacteristicRealEstate
    extra = 0

class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'description')
    inlines = [AgentRealEstateInline, CharacteristicRealEstateInline]
    def has_add_permission(self, request, obj=None):
        return request.user.is_authenticated and Agent.objects.filter(user=request.user).exists()
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            if request.user.is_authenticated:
                AgentRealEstate.objects.create(real_estate=obj, agent = Agent.objects.get(user=request.user))
    def has_delete_permission(self, request, obj=None):
        return not CharacteristicRealEstate.objects.filter(real_estate=obj).exists()
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser or request.user.is_authenticated and AgentRealEstate.objects.filter(real_estate=obj, agent = Agent.objects.get(user=request.user)).exists()
    def get_queryset(self, request):
        return super().get_queryset(request).filter(date_published=timezone.now().date())
    def has_view_permission(self, request, obj = ...):
        return True
    def has_module_permission(self, request):
        return True

class AgentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(RealEstate, RealEstateAdmin)
admin.site.register(Agent, AgentAdmin)