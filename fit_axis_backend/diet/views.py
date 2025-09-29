from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DietPlan
from .serializers import DietPlanSerializer
import json

@api_view(['POST'])
def generate_diet(request):
    if request.method == 'POST':
        try:
            # Get data from request
            food = request.data.get('food', '')
            calories = request.data.get('calories', 0)
            allergy = request.data.get('allergy', '')
            
            # Generate a diet plan based on the inputs
            plan = generate_diet_plan(food, calories, allergy)
            
            # Save to database
            diet_plan = DietPlan.objects.create(
                food_preference=food,
                calories=calories,
                allergy=allergy,
                plan=plan
            )
            
            # Serialize and return response
            serializer = DietPlanSerializer(diet_plan)
            return Response({'plan': plan}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def generate_diet_plan(food, calories, allergy):
    """
    Generate a diet plan based on food preference, calories, and allergies
    This is a simplified version - in a real app, this could use ML or more complex logic
    """
    
    # Sample diet plans based on food preference
    vegetarian_plans = {
        "low": [
            "Breakfast: Oatmeal with fruits and nuts (300 kcal)",
            "Snack: Greek yogurt with berries (150 kcal)",
            "Lunch: Quinoa salad with vegetables (400 kcal)",
            "Snack: Apple with almond butter (200 kcal)",
            "Dinner: Lentil soup with whole grain bread (350 kcal)",
            "Total: ~1400 kcal"
        ],
        "medium": [
            "Breakfast: Smoothie bowl with granola (400 kcal)",
            "Snack: Hummus with vegetables (200 kcal)",
            "Lunch: Chickpea curry with brown rice (550 kcal)",
            "Snack: Trail mix (250 kcal)",
            "Dinner: Stuffed bell peppers with quinoa (450 kcal)",
            "Total: ~1850 kcal"
        ],
        "high": [
            "Breakfast: Avocado toast with eggs (500 kcal)",
            "Snack: Protein smoothie (300 kcal)",
            "Lunch: Buddha bowl with tofu (650 kcal)",
            "Snack: Nuts and dried fruits (300 kcal)",
            "Dinner: Veggie stir-fry with noodles (700 kcal)",
            "Total: ~2450 kcal"
        ]
    }
    
    non_vegetarian_plans = {
        "low": [
            "Breakfast: Scrambled eggs with toast (300 kcal)",
            "Snack: Cottage cheese with cucumber (150 kcal)",
            "Lunch: Grilled chicken salad (400 kcal)",
            "Snack: Protein bar (200 kcal)",
            "Dinner: Baked fish with vegetables (350 kcal)",
            "Total: ~1400 kcal"
        ],
        "medium": [
            "Breakfast: Greek yogurt with granola (400 kcal)",
            "Snack: Turkey and cheese roll-ups (200 kcal)",
            "Lunch: Grilled salmon with quinoa (550 kcal)",
            "Snack: Protein shake (250 kcal)",
            "Dinner: Chicken stir-fry with rice (450 kcal)",
            "Total: ~1850 kcal"
        ],
        "high": [
            "Breakfast: Protein pancakes with berries (500 kcal)",
            "Snack: Hard-boiled eggs and nuts (300 kcal)",
            "Lunch: Beef burger with sweet potato (650 kcal)",
            "Snack: Greek yogurt with honey (300 kcal)",
            "Dinner: Grilled steak with mashed potatoes (700 kcal)",
            "Total: ~2450 kcal"
        ]
    }
    
    # Adjust plan based on calories
    if calories < 1500:
        calorie_level = "low"
    elif calories < 2500:
        calorie_level = "medium"
    else:
        calorie_level = "high"
    
    # Select appropriate plan based on food preference
    if food.lower() == "vegetarian":
        plan = vegetarian_plans.get(calorie_level, vegetarian_plans["medium"])
    else:
        plan = non_vegetarian_plans.get(calorie_level, non_vegetarian_plans["medium"])
    
    # Handle allergies
    if allergy.lower() != "none":
        # This is a simplified approach - in a real app, you would have more sophisticated handling
        plan = [meal for meal in plan if allergy.lower() not in meal.lower()]
        plan.append(f"Note: Please avoid {allergy} and substitute with alternatives.")
    
    # Format the plan as a string
    plan_text = "Here is your personalized diet plan:\n\n"
    plan_text += "\n".join(plan)
    plan_text += f"\n\nFood Preference: {food}\nCalories: {calories} kcal\nAllergy: {allergy}"
    
    return plan_text