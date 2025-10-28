import pandas as pd
import random

# Try to import fuzzy logic (optional but recommended)
try:
    from fuzzy import compute_fuzzy_factors
except Exception:
    compute_fuzzy_factors = None

# =========================================================
# INDIAN MEAL DATABASE (Veg + Non-Veg)
# Clean, low-spice, soy-aware, and dairy-aware meals.
# =========================================================
meal_database = {
    "breakfast": [
        {"name": "Egg White Omelet", "diet": "non-vegetarian",
         "base_qty": "4 egg whites + 5g oil (~120g)", "base_calories": 160,
         "tags": ["protein", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Boiled Eggs", "diet": "non-vegetarian",
         "base_qty": "2 pcs (~100g)", "base_calories": 140,
         "tags": ["protein", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Paneer Paratha + Curd", "diet": "vegetarian",
         "base_qty": "1 paratha (~100g) + 50g curd", "base_calories": 350,
         "tags": ["carb", "protein", "dairy", "low_spice"],
         "allergens": ["gluten", "dairy"], "medical_notes": []},

        {"name": "Tofu Scramble", "diet": "vegetarian",
         "base_qty": "100g tofu + onion + tomato", "base_calories": 230,
         "tags": ["protein", "soy", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Sprout Salad", "diet": "vegetarian",
         "base_qty": "100g moong/chana sprouts", "base_calories": 250,
         "tags": ["protein", "fiber", "low_salt", "low_spice"],
         "allergens": [], "medical_notes": ["diabetes", "bp"]},

        {"name": "Boiled Soybeans", "diet": "vegetarian",
         "base_qty": "100g soybeans", "base_calories": 330,
         "tags": ["protein", "fiber", "soy", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Milk + Almonds", "diet": "vegetarian",
         "base_qty": "200ml milk + 5 almonds", "base_calories": 180,
         "tags": ["dairy", "healthy_fat", "low_spice"], "allergens": ["dairy"], "medical_notes": []},

        {"name": "Oats + Milk + Raisins", "diet": "vegetarian",
         "base_qty": "40g oats + 200ml milk + 20g raisins", "base_calories": 340,
         "tags": ["carb", "dairy", "low_spice"], "allergens": ["dairy", "gluten"], "medical_notes": ["diabetes"]},
    ],

    "lunch": [
        {"name": "Boiled Chicken + Rice + Veggies", "diet": "non-vegetarian",
         "base_qty": "150g chicken + 150g rice + 100g veg", "base_calories": 600,
         "tags": ["protein", "carb", "clean", "low_spice", "low_salt"], "allergens": [], "medical_notes": []},

        {"name": "Paneer Bhurji + Rotis", "diet": "vegetarian",
         "base_qty": "100g paneer + 2 rotis (~120g)", "base_calories": 520,
         "tags": ["protein", "carb", "dairy", "low_spice"], "allergens": ["gluten", "dairy"], "medical_notes": []},

        {"name": "Rajma + Rice", "diet": "vegetarian",
         "base_qty": "150g rajma + 150g rice", "base_calories": 550,
         "tags": ["protein", "carb", "fiber", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Tofu + Rice + Veg Curry", "diet": "vegetarian",
         "base_qty": "100g tofu + 150g rice + 100g veg curry", "base_calories": 450,
         "tags": ["protein", "carb", "soy", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Moong Dal Khichdi + Curd", "diet": "vegetarian",
         "base_qty": "200g khichdi + 50g curd", "base_calories": 420,
         "tags": ["protein", "carb", "dairy", "low_spice"], "allergens": ["dairy"], "medical_notes": ["diabetes"]},

        {"name": "Chana Masala + Salad", "diet": "vegetarian",
         "base_qty": "150g chana + 100g salad", "base_calories": 380,
         "tags": ["protein", "fiber", "low_salt", "low_spice"], "allergens": [], "medical_notes": ["diabetes"]},

        {"name": "Mix Veg Curry + Bajra Roti", "diet": "vegetarian",
         "base_qty": "150g curry + 1 bajra roti (~50g)", "base_calories": 360,
         "tags": ["fiber", "low_salt", "low_spice"], "allergens": [], "medical_notes": ["bp", "asthma"]},

        {"name": "Lauki Chana Dal + Rice", "diet": "vegetarian",
         "base_qty": "150g lauki + 100g chana dal + 150g rice", "base_calories": 400,
         "tags": ["protein", "carb", "low_salt", "low_spice"], "allergens": [], "medical_notes": []},
    ],

    "dinner": [
        {"name": "Boiled Chicken + Veg Soup", "diet": "non-vegetarian",
         "base_qty": "150g chicken + 200ml soup", "base_calories": 420,
         "tags": ["protein", "clean", "low_salt", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Paneer Curry + Rotis", "diet": "vegetarian",
         "base_qty": "100g paneer curry + 2 rotis", "base_calories": 500,
         "tags": ["protein", "carb", "dairy", "low_spice"], "allergens": ["gluten", "dairy"], "medical_notes": []},

        {"name": "Tofu + Veggies", "diet": "vegetarian",
         "base_qty": "100g tofu + 150g veggies", "base_calories": 350,
         "tags": ["protein", "fiber", "soy", "low_salt", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Masoor Dal + Rice + Salad", "diet": "vegetarian",
         "base_qty": "150g dal + 150g rice + 100g salad", "base_calories": 420,
         "tags": ["protein", "carb", "fiber", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Moong Dal + Roti + Salad", "diet": "vegetarian",
         "base_qty": "150g dal + 1 roti + 100g salad", "base_calories": 380,
         "tags": ["protein", "fiber", "low_spice"], "allergens": ["gluten"], "medical_notes": ["diabetes"]},

        {"name": "Curd + Roti + Sabzi", "diet": "vegetarian",
         "base_qty": "100g curd + 1 roti + 150g sabzi", "base_calories": 350,
         "tags": ["dairy", "carb", "low_spice"], "allergens": ["gluten", "dairy"], "medical_notes": []},

        {"name": "Lauki/Tori Sabzi + Roti", "diet": "vegetarian",
         "base_qty": "150g lauki + 1 roti", "base_calories": 300,
         "tags": ["fiber", "low_salt", "low_spice"], "allergens": ["gluten"], "medical_notes": ["bp"]},

        {"name": "Palak Dal + Rotis", "diet": "vegetarian",
         "base_qty": "150g dal + 2 rotis", "base_calories": 480,
         "tags": ["protein", "carb", "fiber", "low_spice"], "allergens": ["gluten"], "medical_notes": []},
    ],

    "snacks": [
        {"name": "Boiled Eggs", "diet": "non-vegetarian",
         "base_qty": "3 pcs (~150g)", "base_calories": 210,
         "tags": ["protein", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Paneer Cubes", "diet": "vegetarian",
         "base_qty": "100g paneer", "base_calories": 280,
         "tags": ["protein", "dairy", "low_spice"], "allergens": ["dairy"], "medical_notes": []},

        {"name": "Sprouts Chaat", "diet": "vegetarian",
         "base_qty": "100g sprouts", "base_calories": 200,
         "tags": ["protein", "fiber", "low_salt", "low_spice"], "allergens": [], "medical_notes": ["diabetes"]},

        {"name": "Greek Yogurt", "diet": "vegetarian",
         "base_qty": "150g unsweetened yogurt", "base_calories": 160,
         "tags": ["protein", "dairy", "low_spice"], "allergens": ["dairy"], "medical_notes": []},

        {"name": "Soybeans (boiled)", "diet": "vegetarian",
         "base_qty": "50g soybeans", "base_calories": 160,
         "tags": ["protein", "fiber", "soy", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Fruit Bowl", "diet": "vegetarian",
         "base_qty": "200g mixed fruit", "base_calories": 200,
         "tags": ["low_salt", "fiber", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Almonds", "diet": "vegetarian",
         "base_qty": "7 pcs (~10g)", "base_calories": 70,
         "tags": ["healthy_fat", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Walnuts", "diet": "vegetarian",
         "base_qty": "3 halves (~15g)", "base_calories": 90,
         "tags": ["healthy_fat", "low_spice"], "allergens": [], "medical_notes": []},

        {"name": "Raisins", "diet": "vegetarian",
         "base_qty": "20g raisins", "base_calories": 60,
         "tags": ["carb", "low_spice"], "allergens": [], "medical_notes": ["diabetes"]},

        {"name": "Roasted Makhana", "diet": "vegetarian",
         "base_qty": "25g makhana", "base_calories": 150,
         "tags": ["low_salt", "fiber", "low_spice"], "allergens": [], "medical_notes": ["bp"]},
    ]
}
# =========================================================
# DataFrame (must come after meal_database)
# =========================================================
all_meals_df = pd.concat(
    {k: pd.DataFrame(v) for k, v in meal_database.items()},
    names=["meal_type"]
).reset_index(level=0)

# =========================================================
# Diabetes-Friendly Replacements
# =========================================================
def _make_diabetes_safe(meals_df):
    """Return a version of meals_df with diabetic-safe swaps."""
    df = meals_df.copy()

    # Replace risky carb sources
    df["name"] = df["name"].replace({
        "Rajma + Rice": "Rajma + Brown Rice",
        "Lauki Chana Dal + Rice": "Lauki Chana Dal + Brown Rice",
        "Tofu + Rice + Veg Curry": "Tofu + Millets + Veg Curry",
        "Boiled Chicken + Rice + Veggies": "Boiled Chicken + Brown Rice + Veggies",
        "Masoor Dal + Rice + Salad": "Masoor Dal + Brown Rice + Salad",
        "Moong Dal Khichdi + Curd": "Moong Dal Khichdi + Unsweetened Curd",
        "Paneer Bhurji + Rotis": "Paneer Bhurji + Multigrain Rotis",
        "Moong Dal + Roti + Salad": "Moong Dal + Multigrain Roti + Salad",
        "Curd + Roti + Sabzi": "Unsweetened Curd + Bajra Roti + Sabzi",
    })

    # Lower-calorie, low-glycemic alternatives
    df.loc[df["name"].str.contains("rice", case=False), "base_calories"] *= 0.9
    df.loc[df["name"].str.contains("roti", case=False), "base_calories"] *= 0.9
    df.loc[df["name"].str.contains("curd", case=False), "base_calories"] *= 0.85

    return df
# =========================================================
# Condition-Safe Replacement Helpers
# =========================================================
def _make_diabetes_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Lower-GI staples: swap white rice->brown/millets; plain rotis->multigrain/bajra; unsweetened dairy."""
    d = df.copy()

    # ✅ Convert to float to avoid FutureWarning for dtype mismatch
    d["base_calories"] = d["base_calories"].astype(float)

    d["name"] = d["name"].replace({
        "Rajma + Rice": "Rajma + Brown Rice",
        "Lauki Chana Dal + Rice": "Lauki Chana Dal + Brown Rice",
        "Tofu + Rice + Veg Curry": "Tofu + Millets + Veg Curry",
        "Boiled Chicken + Rice + Veggies": "Boiled Chicken + Brown Rice + Veggies",
        "Masoor Dal + Rice + Salad": "Masoor Dal + Brown Rice + Salad",
        "Paneer Bhurji + Rotis": "Paneer Bhurji + Multigrain Rotis",
        "Moong Dal + Roti + Salad": "Moong Dal + Multigrain Roti + Salad",
        "Curd + Roti + Sabzi": "Unsweetened Curd + Bajra Roti + Sabzi",
        "Oats + Milk + Raisins": "Oats + Milk + Almonds",  # drop raisins spike
    })

    # Nudge calories slightly down for lower-GI swaps
    d.loc[d["name"].str.contains("brown rice|millet|multigrain|bajra", case=False), "base_calories"] *= 0.93

    # Keep unsweetened dairy leaner
    d.loc[d["name"].str.contains("unsweetened curd|unsweetened yogurt", case=False), "base_calories"] *= 0.95

    return d

def _make_bp_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Low-salt leaning: prefer 'low_salt' items and rebrand saltier items to low-salt variants."""
    d = df.copy()
    d["base_calories"] = d["base_calories"].astype(float)


    d["name"] = d["name"].replace({
        "Paneer Cubes": "Paneer Cubes (Low-Salt, Homemade)",
        "Chana Masala + Salad": "Chana + Salad (No Packaged Masala)",
        "Boiled Chicken + Rice + Veggies": "Boiled Chicken + Brown Rice + Veggies (Low-Salt)",
        "Boiled Chicken + Veg Soup": "Chicken + Veg Soup (Low-Salt Broth)",
        "Greek Yogurt": "Unsweetened Yogurt (Low-Salt)",
        "Curd + Roti + Sabzi": "Unsweetened Curd + Bajra Roti + Sabzi (Low-Salt)"
    })

    # Encourage low_salt choices via a small calorie nudge (doesn't change selection drastically)
    d.loc[d["tags"].apply(lambda t: "low_salt" in [x.lower() for x in t]), "base_calories"] *= 0.98
    return d


def _make_fatty_liver_safe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Make meal list fatty-liver friendly:
    - Reduce high-fat dairy & soy meals
    - Remove fried or creamy items
    - Prefer lean proteins, fiber, and low-oil meals
    """
    d = df.copy()
    d["base_calories"] = d["base_calories"].astype(float)

    # Replace high-fat / heavy items with lighter options
    d["name"] = d["name"].replace({
        "Paneer Paratha + Curd": "Oats Cheela + Mint Yogurt (Low-Fat)",
        "Paneer Bhurji + Rotis": "Moong Dal Bhurji + Multigrain Rotis",
        "Paneer Cubes": "Grilled Chicken Cubes (Lean)",
        "Soybeans (boiled)": "Steamed Moong Sprouts",
        "Boiled Soybeans": "Green Gram (Moong) Boiled",
        "Tofu + Veggies": "Tofu + Veggies (Grilled, Low Oil)",
        "Rajma + Rice": "Rajma + Brown Rice (Low Oil)",
        "Curd + Roti + Sabzi": "Plain Roti + Stir-Fried Veggies (Low Oil)",
    })

    # Drop very high-fat, heavy, or processed items altogether
    d = d[~d["name"].str.contains("fried|deep|butter|cheese|cream", case=False)]

    # Slightly downscale calorie density of dairy/soy foods
    mask = d["name"].str.contains("paneer|curd|yogurt|tofu|soy", case=False)
    d.loc[mask, "base_calories"] *= 0.88  # reduce fat impact

    # Slightly reward fiber-based or low-salt items (encourage inclusion)
    d.loc[d["tags"].apply(lambda t: "fiber" in [x.lower() for x in t]), "base_calories"] *= 1.02
    d.loc[d["tags"].apply(lambda t: "low_salt" in [x.lower() for x in t]), "base_calories"] *= 1.01

    # Add liver-supportive item if not already included
    add = pd.DataFrame([{
        "name": "Lauki-Turmeric Soup + Ginger",
        "diet": "vegetarian",
        "base_qty": "250ml soup",
        "base_calories": 120.0,
        "tags": ["low_spice", "fiber", "antioxidant"],
        "allergens": [],
        "medical_notes": ["fatty liver"]
    }])
    d = pd.concat([d, add], ignore_index=True)

    return d

def _make_asthma_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Removes mucus-trigger foods (dairy, soy) and adds anti-inflammatory alternatives."""
    d = df.copy()
    d["base_calories"] = d["base_calories"].astype(float)

    # Replace known triggers with safer alternatives
    d["name"] = d["name"].replace({
        "Soybeans (boiled)": "Steamed Moong Sprouts + Ginger",
        "Boiled Soybeans": "Green Moong + Carrot Mix",
        "Paneer Paratha + Curd": "Oats Cheela + Mint Chutney",
        "Greek Yogurt": "Almond Yogurt (Unsweetened)",
        "Paneer Cubes": "Roasted Chickpeas",
        "Tofu + Veggies": "Moong Dal + Veggies (Light Curry)",
        "Tofu + Rice + Veg Curry": "Moong Dal + Brown Rice + Veg Curry"
    })

    # 🚫 Drop asthma-triggering foods (soy, dairy)
    d = d[~d["name"].str.contains("tofu|soy|paneer|curd|yogurt", case=False)]

    # ✅ Add anti-inflammatory soup
    add = pd.DataFrame([{
        "name": "Moong Dal Soup + Lemon + Ginger",
        "diet": "vegetarian",
        "base_qty": "250ml soup",
        "base_calories": 150.0,
        "tags": ["low_spice", "fiber", "anti_inflammatory"],
        "allergens": [],
        "medical_notes": ["asthma"]
    }])
    d = pd.concat([d, add], ignore_index=True)

    # Small calorie normalization for low-spice benefit
    d.loc[d["tags"].apply(lambda t: "low_spice" in [x.lower() for x in t]), "base_calories"] *= 0.98

    return d


def _make_thyroid_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Anti-goitrogenic bias: remove soy-heavy items; swap to egg/chicken/lentils; keep iodine/selenium sources."""
    d = df.copy()
    d["base_calories"] = d["base_calories"].astype(float)


    d["name"] = d["name"].replace({
        "Tofu + Veggies": "Egg White Scramble + Veggies",
        "Boiled Soybeans": "Steamed Moong Sprouts + Lemon",
        "Soybeans (boiled)": "Green Moong + Cucumber",
        "Tofu + Rice + Veg Curry": "Boiled Chicken + Rice + Veg Curry",
        "Paneer Bhurji + Rotis": "Egg Bhurji + Multigrain Rotis",
        "Paneer Paratha + Curd": "Oats Cheela + Mint Yogurt (Low-Fat)"
    })

    # Downweight soy-based items further
    d.loc[d["name"].str.contains("tofu|soy", case=False), "base_calories"] *= 0.0  # effectively removes them

    # Small upweight for egg/chicken to preserve protein target
    d.loc[d["name"].str.contains("egg|chicken", case=False), "base_calories"] *= 1.04
    return d

# =========================================================
# Helper Functions
# =========================================================
def _norm_list(v):
    if isinstance(v, str): return [v.lower()]
    if isinstance(v, list): return [str(x).lower() for x in v]
    return ["none"]


def slot_percentages():
    return {"breakfast": 0.25, "lunch": 0.35, "dinner": 0.25, "snacks": 0.15}


def goal_tolerance_and_caps(goal):
    g = (goal or "").lower()
    if g == "bulking":
        return 0.25, {"breakfast": 2, "lunch": 2, "dinner": 2, "snacks": 3}, 1.40
    if g in ["cutting", "weight loss"]:
        return 0.20, {"breakfast": 2, "lunch": 2, "dinner": 2, "snacks": 1}, 1.00
    return 0.15, {"breakfast": 2, "lunch": 2, "dinner": 2, "snacks": 2}, 1.10


def _slot_bounds(cal_target, meal_type, goal, fuzzy=None):
    pct = slot_percentages()[meal_type]
    tol, _, widen = goal_tolerance_and_caps(goal)
    base = cal_target * pct
    lo = base * (1 - tol)
    hi = base * (1 + tol) * (widen if goal == "bulking" else 1)
    if fuzzy:
        lo *= fuzzy.get("scale", 1.0)
        hi *= fuzzy.get("scale", 1.0)
    return lo, hi

## =========================================================
# Master Medical Filter (calls all condition-safe replacements)
# =========================================================
def _apply_medical_filters(df: pd.DataFrame, medical: list, allergies: list) -> pd.DataFrame:
    """Applies condition-safe replacements IN ORDER and re-checks allergies afterwards."""
    m = [str(x).lower() for x in (medical or [])]
    a = [str(x).lower() for x in (allergies or [])]
    out = df.copy()

    # ✅ Apply medical condition-based replacements in proper order
    if "diabetes" in m:
        out = _make_diabetes_safe(out)
    if "bp" in m or "blood pressure" in m:
        out = _make_bp_safe(out)
    if "fatty liver" in m:
        out = _make_fatty_liver_safe(out)
    if "asthma" in m:
        out = _make_asthma_safe(out)
    if "thyroid" in m:
        out = _make_thyroid_safe(out)

    # ✅ Recheck allergies (strict removal of allergens)
    if "dairy" in a or "gluten" in a:
        out = out[~out["allergens"].apply(lambda al:
            any(alg in [x.lower() for x in al] for alg in a if alg != "none")
        )].copy()

    # ✅ Safety fallback: if everything is filtered out, use low-spice, high-fiber meals
    if out.empty:
        out = df[df["tags"].apply(lambda t:
            "low_spice" in [x.lower() for x in t] and "fiber" in [x.lower() for x in t]
        )].copy()

    return out


# =========================================================
# STRICT Medical and Allergy Filtering (main entrypoint)
# =========================================================
def _filter_pool(user_data, meal_type):
    """Filter meal options for each meal type based on user diet, allergies, and medical conditions."""
    diet = (user_data.get("Diet Type", "") or "").lower()
    allergies = _norm_list(user_data.get("Allergies", "none"))
    medical = _norm_list(user_data.get("Medical History", "none"))

    # ✅ Select meals from the correct category
    subset = all_meals_df[all_meals_df["meal_type"] == meal_type].copy()

    # ✅ Apply master medical filter (handles diabetes/BP/asthma/fatty liver/thyroid)
    subset = _apply_medical_filters(subset, medical, allergies)

    # ✅ Apply vegetarian-only filtering after replacements
    if diet == "vegetarian":
        subset = subset[subset["diet"].str.lower() == "vegetarian"]

    # ✅ Fallback to safe high-fiber, low-spice options if nothing remains
    if subset.empty:
        subset = all_meals_df[
            all_meals_df["tags"].apply(lambda x: "low_spice" in x and "fiber" in x)
        ].copy()

    return subset


# =========================================================
# Core Selection + Scaling
# =========================================================
def _scale_row(row, factor):
    return {
        "name": row["name"],
        "calories": int(row["base_calories"] * factor),
        "qty": f"{factor:.2f} × {row['base_qty']}"
    }


def _protein_sort_key(row, protein_bias: float):
    tags = [t.lower() for t in (row.get("tags") or [])]
    return 0 if ("protein" in tags) else (1 - protein_bias)


def _caution_penalty(row, *, salt_caution, carb_caution, fat_caution,
                     inflammation_caution, soy_caution):
    tags = [t.lower() for t in (row.get("tags") or [])]
    penalty = 0.0
    if "low_salt" not in tags:
        penalty += 0.6 * salt_caution
    if "carb" in tags:
        penalty += 0.5 * carb_caution
    if "dairy" in tags or "healthy_fat" in tags:
        penalty += 0.4 * fat_caution
    if "soy" in tags:
        penalty += 0.6 * soy_caution
    if "low_spice" not in tags:
        penalty += 0.5 * inflammation_caution
    return penalty


def pick_meals_for_slot(user_data, meal_type, calorie_target, fuzzy):
    goal = (user_data.get("Fitness Goal", "") or "").lower()
    lo, hi = _slot_bounds(calorie_target, meal_type, goal, fuzzy)
    _, slot_caps, _ = goal_tolerance_and_caps(goal)
    max_items = slot_caps.get(meal_type, 2)

    pool = _filter_pool(user_data, meal_type)
    if pool.empty:
        return [{"name": "⚠️ No suitable meal", "calories": 0, "qty": ""}]

    f = (fuzzy or {})
    protein_bias = f.get("protein_bias", 0.0)
    salt_caution = f.get("salt_caution", 0.0)
    carb_caution = f.get("carb_caution", 0.0)
    fat_caution = f.get("fat_caution", 0.0)
    inflammation_caution = f.get("inflammation_caution", 0.0)
    soy_caution = f.get("soy_caution", 0.0)

    scored = []
    for idx, row in pool.iterrows():
        base = _protein_sort_key(row, protein_bias)
        penalty = _caution_penalty(
            row,
            salt_caution=salt_caution,
            carb_caution=carb_caution,
            fat_caution=fat_caution,
            inflammation_caution=inflammation_caution,
            soy_caution=soy_caution,
        )
        scored.append((base + penalty + random.random() * 0.05, idx))

    scored.sort(key=lambda x: x[0])
    indices = [i for _, i in scored]

    chosen = []
    for idx in indices[:max_items]:
        row = pool.loc[idx]
        chosen.append(_scale_row(row, 1.0))
    return chosen


# =========================================================
# Adjustment + Notes
# =========================================================
def adjust_to_match_target(plan, calorie_target, fuzzy):
    total = sum(x["calories"] for m in plan.values() if isinstance(m, list) for x in m)
    if total == 0:
        return plan

    fuzzy_scale = (fuzzy or {}).get("scale", 1.0)
    total *= fuzzy_scale
    scale_factor = calorie_target / max(total, 1e-6)
    final_scale = fuzzy_scale * scale_factor

    for meal_type, items in plan.items():
        if meal_type in ("Total Calories", "Note"):
            continue
        for item in items:
            item["calories"] = int(item["calories"] * final_scale)
            item["qty"] = f"{final_scale:.2f} × {item['qty']}"
    plan["Total Calories"] = int(calorie_target)

    notes = [
        "🍲 If any food is unavailable, replace with its nearest alternative (e.g., tofu ↔ paneer, chicken ↔ soybeans).",
        "🌶️ Avoid spicy and oily food; use minimal oil, mild spices; onion, tomato, and garlic allowed.",
        "🥗 You may freely add fruits and vegetables to boost fiber, vitamins, and minerals.",
        "💧 Drink sufficient water throughout the day.",
        "📱 If calories still feel insufficient/excessive, check App (Supplement section) for portion guidance.",
        "✅ Stay consistent – stick with the same plan rather than switching frequently."
    ]
    plan["Note"] = "\n".join(notes)
    return plan


# =========================================================
# Public API
# =========================================================
def generate_daily_plan(user_data, calorie_target):
    fuzzy = compute_fuzzy_factors(user_data, calorie_target) if callable(compute_fuzzy_factors) else None
    plan, total = {}, 0
    for meal in ["breakfast", "lunch", "dinner", "snacks"]:
        items = pick_meals_for_slot(user_data, meal, calorie_target, fuzzy)
        plan[meal.title()] = items
        total += sum(x["calories"] for x in items)
    plan["Total Calories"] = total
    return adjust_to_match_target(plan, calorie_target, fuzzy)