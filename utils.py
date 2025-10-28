# utils.py
# (Currently not required by the other files — here for future expansion.)
def safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default
