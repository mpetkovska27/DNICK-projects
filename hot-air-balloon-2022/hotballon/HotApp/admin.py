from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline

from .models import Pilot, Ballon, Let, AvioKompanija, AvioKompanijaPilot


# Register your models here.
# За пилотите и авиокомпаниите во листата да се прикажуваат само нивните имиња (и презиме за пилотот)

#Потребно е да овозможите додавање на објекти преку Админ панелот со забелешка дека пилотите-соработници
#на една авиокомпанија се додаваат во делот за авиокомпанија

class PilotAdmin(admin.ModelAdmin):
    list_display = ('ime', 'prezime',)
admin.site.register(Pilot, PilotAdmin)

class BallonAdmin(admin.ModelAdmin):
    list_display = ('tip', 'imeNaProizveduvac',)
admin.site.register(Ballon, BallonAdmin)

class AvioKompanijaPilotAdmin(admin.StackedInline):
    model = AvioKompanijaPilot
    extra = 1  #dali da se pokazuva 1 ili 3 na pr

class AvioKompanijaAdmin(admin.ModelAdmin):
    inlines = [AvioKompanijaPilotAdmin, ] #tuka ja pravi vrskata
    list_display = ('ime',)
admin.site.register(AvioKompanija, AvioKompanijaAdmin)

class LetAdmin(admin.ModelAdmin):
    # При креирање на летот, корисникот се доделува автоматски според најавениот корисник
    def save_model(self,request, obj, form, change):
        obj.kreator = request.user #onoj koj e najaven se cuva vo request
        super().save_model(request, obj, form, change) #prodolzi so procesiranje kon baza
    #Откако еден лет е дефиниран и зачуван, истиот може да се промени само до корисникот кој го креирал
    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.kreator:
            return True
        return False
    #Не е дозволено брижење на летовите
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Let, LetAdmin)



