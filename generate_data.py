"""
generate_data.py
Creates a SYNTHETIC (made-up) car wash bookings dataset for practice.
This is NOT real business data. Run it once to create data/car_wash_bookings.csv
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # fixed seed so everyone gets the same data

# Service name -> base price in PKR
services = {
    "Basic Exterior Wash": 800,
    "Interior + Exterior Wash": 1500,
    "Engine Wash": 1000,
    "Wax and Polish": 2500,
    "Full Detailing": 4500,
    "Vacuum Cleaning": 500,
}
service_probs = [0.30, 0.25, 0.08, 0.14, 0.07, 0.16]

# Vehicle type -> price multiplier
vehicles = {"Hatchback": 1.0, "Sedan": 1.15, "SUV": 1.4, "Pickup": 1.5}
vehicle_probs = [0.30, 0.38, 0.22, 0.10]

points = ["Canal Road", "Main Boulevard", "Satyana Road"]
point_probs = [0.40, 0.35, 0.25]

payments = ["Cash", "Mobile Wallet", "Card"]
payment_probs = [0.55, 0.30, 0.15]

# Busier hours: late morning and late afternoon
hours = list(range(9, 20))  # 9am to 7pm
hour_weights = np.array([3, 5, 8, 9, 7, 5, 6, 8, 9, 7, 4], dtype=float)
hour_probs = hour_weights / hour_weights.sum()

# Month factor: more demand in dusty summer months
month_factor = {1: 0.85, 2: 0.9, 3: 1.05, 4: 1.25, 5: 1.3, 6: 1.25,
                7: 1.0, 8: 1.0, 9: 1.05, 10: 1.1, 11: 1.0, 12: 1.15}

rows = []
for day in pd.date_range("2025-01-01", "2025-12-31"):
    base = 4.0
    if day.dayofweek in (5, 6):      # Saturday, Sunday
        base += 3.5
    elif day.dayofweek == 4:         # Friday
        base += 1.5
    n = rng.poisson(base * month_factor[day.month])
    for _ in range(n):
        service = rng.choice(list(services), p=service_probs)
        vehicle = rng.choice(list(vehicles), p=vehicle_probs)
        price = services[service] * vehicles[vehicle]
        price = int(round(price / 50) * 50)  # round to nearest 50 PKR
        premium = service in ("Full Detailing", "Wax and Polish")
        rating = int(np.clip(round(rng.normal(4.5 if premium else 4.1, 0.8)), 1, 5))
        rows.append({
            "date": day.strftime("%Y-%m-%d"),
            "hour": int(rng.choice(hours, p=hour_probs)),
            "service": service,
            "vehicle_type": vehicle,
            "washing_point": rng.choice(points, p=point_probs),
            "payment_method": rng.choice(payments, p=payment_probs),
            "price_pkr": price,
            "rating": rating,
        })

df = pd.DataFrame(rows)
df.insert(0, "booking_id", [f"CW-{i:04d}" for i in range(1, len(df) + 1)])

# Make the data a little messy on purpose, so we can practise cleaning it
df.loc[df.sample(frac=0.04, random_state=1).index, "rating"] = np.nan          # missing ratings
idx = df.sample(frac=0.03, random_state=2).index
df.loc[idx, "payment_method"] = df.loc[idx, "payment_method"].str.upper()      # CASH, CARD...
df = pd.concat([df, df.sample(15, random_state=3)], ignore_index=True)         # 15 duplicate rows
df = df.sample(frac=1, random_state=4).reset_index(drop=True)                  # shuffle

df.to_csv("data/car_wash_bookings.csv", index=False)
print(f"Saved {len(df)} rows to data/car_wash_bookings.csv")
