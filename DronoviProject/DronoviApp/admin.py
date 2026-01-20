from django.utils import timezone

from django.contrib import admin
from django.db.models import Q

from .models import *


# Register your models here.

class DronAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return Pilot.objects.filter(user=request.user, br_rezervacii__gt=3).exists()
    def has_module_permission(self, request):
        return True
    def has_view_permission(self, request, obj=None):
        return True

class PilotAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser
    def has_module_permission(self, request):
        return True
    def has_view_permission(self, request, obj=None):
        return True

class PilotReservationAdmin(admin.StackedInline):
    model=PilotRezervacija
    extra=0
    def has_module_permission(self, request):
        return True
    def has_view_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj):
        return True

class RezervacijaAdmin(admin.ModelAdmin):
    exclude = ('odgovoren',)
    inlines = (PilotReservationAdmin,)
    def has_add_permission(self, request):
        return request.user.is_authenticated and Pilot.objects.filter(user=request.user).exists()
    def save_model(self, request, obj, form, change):
        if not change:
            obj.odgovoren = Pilot.objects.get(user=request.user)
        super().save_model(request, obj, form, change)
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        if obj.status !='C':
            return False
        pilotce = Pilot.objects.filter(user=request.user).first()
        if obj.odgovoren == pilotce:
            return True
        return PilotRezervacija.objects.filter(rezervacija=obj, pilot=pilotce).exists()
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        if obj.status !='C':
            return False
        pilotcinja = PilotRezervacija.objects.filter(rezervacija=obj).exists()
        if obj.odgovoren.user == request.user and pilotcinja==False:
            return True
        return False
    def has_module_permission(self, request):
        return True
    def has_view_permission(self, request, obj=...):
        return True
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        today = timezone.now().date()
        pilot = Pilot.objects.get(user=request.user)
        if pilot:
            return qs.filter(
                Q(odgovoren=pilot, status__in=['A', 'C'], datum__gte=today) |
                Q(status='Z')
            )
        return qs.none()





admin.site.register(Dron, DronAdmin)
admin.site.register(Pilot, PilotAdmin)
admin.site.register(Rezervacija, RezervacijaAdmin)
