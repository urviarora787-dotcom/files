import json
import math

def load_partners(path="partners.json"):
    with open(path) as f:
        return json.load(f)


def distance_km(lat1, lng1, lat2, lng2):
    """
    Haversine formula: calculates distance between two lat/long points
    on Earth's surface, in kilometers.
    """
    R = 6371  # Earth's radius in km

    lat1_rad, lng1_rad = math.radians(lat1), math.radians(lng1)
    lat2_rad, lng2_rad = math.radians(lat2), math.radians(lng2)

    d_lat = lat2_rad - lat1_rad
    d_lng = lng2_rad - lng1_rad

    a = (math.sin(d_lat / 2) ** 2
         + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lng / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def find_nearest_eligible(user_lat, user_lng, loan_category, partners, top_n=3):
    """
    Step 1 (filter): keep only partners that
        - are marked Eligible_For_Routing == "Yes"
          (per the real data, this is the actual field to trust, NOT NPA
          status directly - a partner can have decent NPA but still be
          flagged ineligible for other reasons, so always check this field)
        - have the requested loan category in their schemes_handled list
          (a partner can now handle MULTIPLE categories, e.g.
          ["Micro Finance", "Term Loan"])
    Step 2 (sort): order what's left by distance from the user, closest first.
    Step 3: return the top N results.

    NOTE: This partner data is a MOCK/SYNTHETIC dataset for demo purposes.
    Real NPA/eligibility data for channel partners is not publicly
    available, so these entries were fabricated to demonstrate the logic.
    """
    eligible = [
        p for p in partners
        if p["eligible_for_routing"] == "Yes" and loan_category in p["schemes_handled"]
    ]

    for p in eligible:
        p["distance_km"] = round(distance_km(user_lat, user_lng, p["lat"], p["lng"]), 2)

    eligible.sort(key=lambda p: p["distance_km"])

    return eligible[:top_n]


if __name__ == "__main__":
    # quick manual test: pretend the user is near Delhi, wants a Term Loan
    partners = load_partners()
    results = find_nearest_eligible(
        user_lat=28.6139,
        user_lng=77.2090,
        loan_category="Term Loan",
        partners=partners,
    )
    for r in results:
        print(f"{r['name']} ({r['city']}) - {r['distance_km']} km away - handles {r['schemes_handled']}")
