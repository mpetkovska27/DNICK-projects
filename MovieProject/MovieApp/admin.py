from django.contrib import admin
from .models import Movie, Review
# Register your models here.

class ReviewAdmin(admin.TabularInline):
    model = Review
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','average_rating' )
    list_filter = ('genre',)
    search_fields = ('title', 'genre')
    inlines = [ReviewAdmin]

admin.site.register(Movie, MovieAdmin)

