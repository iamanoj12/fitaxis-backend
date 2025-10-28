# fuzzy.py
# ---------------------------------------------------------
# Adaptive fuzzy-logic engine for personalized diet plans.
# Fully dependency-free (no skfuzzy etc.).
# Handles:
#   → Fitness Goals: Bulking, Cutting, Weight Loss, Maintain
#   → Medical History: BP, Diabetes, Fatty Liver, Asthma, Thyroid
#   → Allergies: Dairy, Gluten
# Produces gentle scaling & nutrient biases for recommendation.py
# ---------------------------------------------------------

def _clamp(x, lo, hi):
    """Keep a value within [lo, hi] range."""
    return max(lo, min(hi, x))


# -------------------------
# Goal Scoring Functions
# -------------------------
def _score_cutting(goal: str) -> float:
    """Cutting / Weight loss goals → negative scale, high protein bias."""
    return 1.0 if (goal or "").lower() in ("cutting", "weight loss") else 0.0

def _score_bulking(goal: str) -> float:
    """Bulking goal → positive calorie scale."""
    return 1.0 if (goal or "").lower() == "bulking" else 0.0

def _score_maintain(goal: str) -> float:
    """Maintain goal → neutral scale."""
    return 1.0 if (goal or "").lower() == "maintain" else 0.0


# -------------------------
# Medical Condition Scoring
# -------------------------
def _score_bp(med_hist) -> float:
    """Blood Pressure → needs low salt meals."""
    tags = [str(m).lower() for m in (med_hist or [])]
    return 1.0 if ("bp" in tags or "blood pressure" in tags) else 0.0

def _score_diabetes(med_hist) -> float:
    """Diabetes → reduce simple carbs."""
    tags = [str(m).lower() for m in (med_hist or [])]
    return 1.0 if "diabetes" in tags else 0.0

def _score_fatty_liver(med_hist) -> float:
    """Fatty Liver → avoid fatty/oily meals."""
    tags = [str(m).lower() for m in (med_hist or [])]
    return 1.0 if "fatty liver" in tags else 0.0

def _score_asthma(med_hist) -> float:
    """Asthma → avoid inflammation-triggering foods (spicy/fried)."""
    tags = [str(m).lower() for m in (med_hist or [])]
    return 1.0 if "asthma" in tags else 0.0

def _score_thyroid(med_hist) -> float:
    """Thyroid → avoid excess soy & high-fat foods."""
    tags = [str(m).lower() for m in (med_hist or [])]
    return 1.0 if "thyroid" in tags else 0.0


# -------------------------
# Allergy Scoring
# -------------------------
def _score_dairy_allergy(allergies) -> float:
    """Avoid dairy if allergic."""
    tags = [str(a).lower() for a in (allergies or [])]
    return 1.0 if "dairy" in tags else 0.0

def _score_gluten_allergy(allergies) -> float:
    """Avoid gluten if allergic."""
    tags = [str(a).lower() for a in (allergies or [])]
    return 1.0 if "gluten" in tags else 0.0


# -------------------------
# Main Fuzzy Calculator
# -------------------------
def compute_fuzzy_factors(user_data: dict, calorie_target: float) -> dict:
    """
    Compute adaptive fuzzy scaling values.
    These are used by recommendation.py to filter and scale meals.
    Returns a dictionary of bias & caution factors.
    """

    goal = (user_data.get("Fitness Goal", "") or "").lower()
    med  = user_data.get("Medical History", []) or []
    allergies = user_data.get("Allergies", []) or []

    # Goal scores
    s_cut = _score_cutting(goal)
    s_bulk = _score_bulking(goal)
    s_maintain = _score_maintain(goal)

    # Health condition scores
    s_bp  = _score_bp(med)
    s_dm  = _score_diabetes(med)
    s_fl  = _score_fatty_liver(med)
    s_as  = _score_asthma(med)
    s_th  = _score_thyroid(med)

    # Allergy scores
    s_dairy = _score_dairy_allergy(allergies)
    s_gluten = _score_gluten_allergy(allergies)

    # -------------------------
    # Global Calorie Scaling
    # -------------------------
    # Cutting → -5%; Bulking → +5%; Maintain → neutral
    scale = 1.0 + 0.05 * (s_bulk - s_cut)
    scale = _clamp(scale, 0.93, 1.07)

    # -------------------------
    # Nutrient / Food Biases
    # -------------------------
    protein_bias = _clamp(0.30 * s_cut + 0.15 * s_bulk, 0.0, 0.6)  # High for cutting
    salt_caution = _clamp(0.60 * s_bp, 0.0, 0.8)                   # Low-salt for BP
    carb_caution = _clamp(0.50 * s_dm, 0.0, 0.7)                   # Less carbs for diabetes
    fat_caution  = _clamp(0.45 * s_fl + 0.20 * s_th, 0.0, 0.7)     # Less fat for liver/thyroid
    inflammation_caution = _clamp(0.60 * s_as, 0.0, 0.8)           # Anti-inflammatory foods
    soy_caution  = _clamp(0.60 * s_th, 0.0, 0.9)                   # Less soy for thyroid

    # Allergies gently modify choices (soft penalties)
    dairy_caution = _clamp(0.80 * s_dairy, 0.0, 1.0)
    gluten_caution = _clamp(0.80 * s_gluten, 0.0, 1.0)

    # -------------------------
    # Final Output
    # -------------------------
    return {
        "scale": scale,
        "protein_bias": protein_bias,
        "salt_caution": salt_caution,
        "carb_caution": carb_caution,
        "fat_caution": fat_caution,
        "inflammation_caution": inflammation_caution,
        "soy_caution": soy_caution,
        "dairy_caution": dairy_caution,
        "gluten_caution": gluten_caution,
    }
