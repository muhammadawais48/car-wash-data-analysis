"""
generate_data.py
Creates a SYNTHETIC (made-up) car wash bookings dataset for practice.
This is NOT real business data. Run it once to create car_wash_bookings.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)  # fixed seed so everyone gets the same data

# Service name -> base price in PKR -> probability of being chosen
services = {
    "Basic Exterior Wash": {"price": 800, "prob": 0.30},
    "Interior + Exterior Wash": {"price": 1500, "prob": 0.25},
    "Engine Wash": {"price": 1000, "prob": 0.08},
    "Wax and Polish": {"price": 2500, "prob": 0.14},
    "Full Detailing": {"price": 4500, "prob": 0.07},
    "Vacuum Cleaning": {"price": 500, "prob": 0.16}

}

# Vehicle type -> price multiplier -> probability of being chosen
vehicles = {"Hatchback": {"multiplier": 1.0, "prob": 0.30},
            "Sedan": {"multiplier": 1.15, "prob": 0.38},
            "SUV": {"multiplier": 1.4, "prob": 0.22},
            "Pickup": {"multiplier": 1.5, "prob": 0.10}
            }

points = {"Canal Road" : {"prob": 0.40},
          "Main Boulevard" : {"prob": 0.35},
          "Satyana Road" : {"prob": 0.25}}

payments = {"Cash" : { "prob": 0.55 },
            "Mobile Wallet" : { "prob": 0.30 },
            "Card" : { "prob": 0.15 }}

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
        service = rng.choice(list(services.keys()), p=[service_prob["prob"] for service_prob in services.values()])
        vehicle = rng.choice(list(vehicles.keys()), p=[vehicle_prob["prob"] for vehicle_prob in vehicles.values()])
        price = services[service]["price"] * vehicles[vehicle]["multiplier"]
        price = int(round(price / 50) * 50)  # round to nearest 50 PKR
        premium = service in ("Full Detailing", "Wax and Polish")
        rating = int(np.clip(round(rng.normal(4.5 if premium else 4.1, 0.8)), 1, 5))
        rows.append({
            "date": day.strftime("%Y-%m-%d"),
            "hour": int(rng.choice(hours, p=hour_probs)),
            "service": service,
            "vehicle_type": vehicle,
            "washing_point": rng.choice(list(points.keys()), p=[points[point]["prob"] for point in points]),
            "payment_method": rng.choice(list(payments.keys()), p=[payments[payment]["prob"] for payment in payments]),
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

df.to_csv(Path(__file__).resolve().parent / "car_wash_bookings.csv", index=False)
print(f"Saved {len(df)} rows to car_wash_bookings.csv")
