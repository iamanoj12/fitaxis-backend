from django.db import models
from django.contrib.auth.models import User

class DietPlan(models.Model):
    food_preference = models.CharField(max_length=50)
    calories = models.IntegerField()
    allergy = models.CharField(max_length=50)
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.food_preference} - {self.calories} kcal"