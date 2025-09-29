from django.contrib import admin
from .models import DietPlan

@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('food_preference', 'calories', 'allergy', 'created_at')
    list_filter = ('food_preference', 'allergy', 'created_at')
    search_fields = ('food_preference', 'allergy')
    ordering = ('-created_at',)