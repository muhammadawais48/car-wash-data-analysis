"""
analysis.py
Car Wash Business Analysis (sample data)

Steps:
1. Load the CSV
2. Clean the data
3. Calculate key numbers (KPIs)
4. Make charts
5. Run SQL queries from queries.sql using SQLite
"""
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # lets us save charts without opening a window
import matplotlib.pyplot as plt

# ---------- 1. Load ----------
df = pd.read_csv("data/car_wash_bookings.csv")
print("Rows before cleaning:", len(df))

# ---------- 2. Clean ----------
# a) remove duplicate bookings (same booking_id)
df = df.drop_duplicates(subset="booking_id")

# b) make payment_method consistent: "CASH" -> "Cash"
df["payment_method"] = df["payment_method"].str.strip().str.title()

# c) turn the date text into a real date and add helpful columns
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)
df["weekday"] = df["date"].dt.day_name()

# d) missing ratings: we keep them as empty (NaN) instead of guessing
print("Rows after cleaning:", len(df))
print("Missing ratings:", df["rating"].isna().sum())

# ---------- 3. Key numbers ----------
total_revenue = df["price_pkr"].sum()
total_bookings = len(df)
print(f"\nTotal bookings: {total_bookings}")
print(f"Total revenue: PKR {total_revenue:,.0f}")
print(f"Average booking value: PKR {df['price_pkr'].mean():,.0f}")
print(f"Average rating: {df['rating'].mean():.2f}")

by_service = df.groupby("service")["price_pkr"].agg(["count", "sum"]).sort_values("sum", ascending=False)
by_month = df.groupby("month")["price_pkr"].sum()
by_weekday = df["weekday"].value_counts().reindex(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
by_hour = df["hour"].value_counts().sort_index()
by_point = df.groupby("washing_point")["price_pkr"].sum().sort_values(ascending=False)
by_payment = df["payment_method"].value_counts()

print("\nTop service by revenue:", by_service.index[0],
      f"({by_service['sum'].iloc[0] / total_revenue:.0%} of revenue)")
print("Best month:", by_month.idxmax(), f"(PKR {by_month.max():,.0f})")
print("Weakest month:", by_month.idxmin(), f"(PKR {by_month.min():,.0f})")
print("Busiest weekday:", by_weekday.idxmax(), f"({by_weekday.max()} bookings)")
print("Peak hour:", f"{by_hour.idxmax()}:00", f"({by_hour.max()} bookings)")
print("Top washing point:", by_point.index[0])
print("Most used payment method:", by_payment.index[0], f"({by_payment.iloc[0] / total_bookings:.0%})")

# ---------- 4. Charts ----------
plt.rcParams.update({"figure.figsize": (9, 5), "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 11})
BLUE = "#1f6feb"

# Chart 1: revenue by service
fig, ax = plt.subplots()
by_service["sum"].sort_values().plot(kind="barh", color=BLUE, ax=ax)
ax.set_title("Revenue by Service (PKR)")
ax.set_xlabel("Revenue (PKR)")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("charts/1_revenue_by_service.png", dpi=150)
plt.close()

# Chart 2: monthly revenue
fig, ax = plt.subplots()
ax.plot(by_month.index, by_month.values, marker="o", color=BLUE)
ax.set_title("Monthly Revenue, 2025 (PKR)")
ax.set_ylabel("Revenue (PKR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/2_monthly_revenue.png", dpi=150)
plt.close()

# Chart 3: bookings by weekday
fig, ax = plt.subplots()
by_weekday.plot(kind="bar", color=BLUE, ax=ax)
ax.set_title("Bookings by Day of the Week")
ax.set_ylabel("Number of bookings")
ax.set_xlabel("")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("charts/3_bookings_by_weekday.png", dpi=150)
plt.close()

# Chart 4: bookings by hour
fig, ax = plt.subplots()
ax.bar(by_hour.index, by_hour.values, color=BLUE)
ax.set_title("Bookings by Hour of the Day")
ax.set_xlabel("Hour (24h clock)")
ax.set_ylabel("Number of bookings")
ax.set_xticks(by_hour.index)
plt.tight_layout()
plt.savefig("charts/4_bookings_by_hour.png", dpi=150)
plt.close()

# Chart 5: payment methods
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(by_payment.values, labels=by_payment.index, autopct="%1.0f%%",
       colors=["#1f6feb", "#58a6ff", "#a5d6ff"], startangle=90)
ax.set_title("Payment Methods")
plt.tight_layout()
plt.savefig("charts/5_payment_methods.png", dpi=150)
plt.close()
print("\nSaved 5 charts in the charts/ folder")

# ---------- 5. SQL queries ----------
conn = sqlite3.connect(":memory:")
df_sql = df.copy()
df_sql["date"] = df_sql["date"].dt.strftime("%Y-%m-%d")
df_sql.drop(columns=["month", "weekday"]).to_sql("bookings", conn, index=False)

with open("queries.sql") as f:
    blocks = [b.strip() for b in f.read().split(";") if "SELECT" in b]

for block in blocks:
    title = [l for l in block.splitlines() if l.startswith("-- Query")][0][3:]
    sql = "\n".join(l for l in block.splitlines() if not l.startswith("--"))
    print(f"\n{title}")
    print(pd.read_sql_query(sql, conn).to_string(index=False))
conn.close()
