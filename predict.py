# predict.py — Final debug version with ML error tracing
from calorie_model import predict_calories
from utils import safe_int
from recommendation import generate_daily_plan

print("\n👤 Please enter your details for a personalized diet plan:\n")

print("1. Male\n2. Female")
gender_choice = input("Select Gender (1-2): ").strip()
gender = "Male" if gender_choice == "1" else "Female"

print("1. Ectomorph\n2. Mesomorph\n3. Endomorph")
body_choice = input("Select Body Type (1-3): ").strip()
body_types = {"1": "Ectomorph", "2": "Mesomorph", "3": "Endomorph"}
body_type = body_types.get(body_choice, "Mesomorph")

print("1. Vegetarian\n2. Non-Vegetarian")
diet_choice = input("Select Diet Type (1-2): ").strip()
diet_type = "Vegetarian" if diet_choice == "1" else "Non-Vegetarian"

print("1. Diabetes\n2. Blood Pressure\n3. Asthma\n4. Thyroid\n5. Fatty Liver\n6. None")
medical_history_input = input("Select Medical History (comma-separated numbers): ").strip()
medical_history = []
if medical_history_input and medical_history_input != "6":
    selected = [x.strip() for x in medical_history_input.split(",")]
    mapping = {"1": "Diabetes", "2": "Blood Pressure", "3": "Asthma", "4": "Thyroid", "5": "Fatty Liver"}
    medical_history = [mapping.get(x, "") for x in selected if x in mapping]

print("1. Bulking\n2. Cutting\n3. Weight Loss\n4. Maintain")
goal_choice = input("Select Fitness Goal (1-4): ").strip()
goals = {"1": "Bulking", "2": "Cutting", "3": "Weight Loss", "4": "Maintain"}
goal = goals.get(goal_choice, "Maintain")

print("1. Gluten\n2. Dairy\n3. None")
allergy_input = input("Select Allergies (comma-separated numbers): ").strip()
allergies = []
if allergy_input and allergy_input != "3":
    selected = [x.strip() for x in allergy_input.split(",")]
    mapping = {"1": "Gluten", "2": "Dairy"}
    allergies = [mapping.get(x, "") for x in selected if x in mapping]

age = safe_int(input("Age: "))
weight = float(input("Weight (kg): "))
height = float(input("Height (cm): "))

# === Machine Learning Calorie Prediction ===
print("\n🤖 Predicting your daily calorie needs using machine learning model...")
user_features = {
    "Age": age,
    "Weight": weight,
    "Height": height,
    "Gender": gender,
    "Body Type": body_type,
    "Diet Type": diet_type,
    "Goal": goal
}

try:
    predicted_calories = predict_calories(user_features)
    print(f"Estimated base calorie requirement: {predicted_calories:.0f} kcal")
except Exception as e:
    print("❌ ML model failed with error:", e)
    predicted_calories = 2000

# Keep same visible input style for consistency
manual_input = input(f"Current Calorie Intake (kcal) [{int(predicted_calories)}]: ").strip()
if manual_input == "":
    current_calories = predicted_calories
else:
    current_calories = safe_int(manual_input)

# === Goal Adjustment (same fixed rule) ===
if goal.lower() in ["bulking", "bulk"]:
    target_calories = current_calories + 300
elif goal.lower() in ["cutting", "weight loss", "lose weight"]:
    target_calories = current_calories - 300
else:
    target_calories = current_calories  # Maintain

# === Summary Output (unchanged format) ===
print(f"\n⚡ Fitness Profile Summary")
print(f"   Gender: {gender}, Age: {age}, Height: {height:.1f} cm, Weight: {weight:.1f} kg")
print(f"   Body Type: {body_type}, Goal: {goal}")
print(f"⚖️ Current Calorie Intake: {current_calories:.2f} kcal")
print(f"🎯 Adjusted Calorie Target: {target_calories:.2f} kcal\n")

# === Prepare user_data dictionary for recommendation ===
user_data = {
    "Gender": gender,
    "Age": age,
    "Height": height,
    "Weight": weight,
    "Body Type": body_type,
    "Diet Type": diet_type,
    "Medical History": medical_history,
    "Allergies": allergies,
    "Fitness Goal": goal
}

# === Generate Daily Plan ===
plan = generate_daily_plan(user_data, target_calories)
# === Generate Daily Plan ===
plan = generate_daily_plan(user_data, target_calories)

# === Display Daily Plan ===
print("\n🍽️ Daily Plan:")
for meal_type, items in plan.items():
    if meal_type in ["Total Calories", "Note"]:
        continue
    print(f"➡️ {meal_type}:")
    for item in items:
        print(f"   - {item['name']} → {item['qty']}, {item['calories']} kcal")

# === Summary totals ===
print(f"➡️ Total Calories: {plan['Total Calories']} kcal (Target: {int(target_calories)} kcal)\n")

if "Note" in plan:
    print(f"{plan['Note']}")

