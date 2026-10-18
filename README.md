# Car Wash Booking Analysis | Python & SQL

A reproducible exploratory data analysis project using a **synthetic car-wash bookings dataset** for 2025. The project explores service revenue, booking patterns, customer ratings, payment preferences and location performance. It is a learning portfolio project, **not an analysis of real customers or an operating business**.

The topic is related to my [Car Wash Management System final-year project](https://github.com/muhammadawais48/car-wash-management-system). This analysis is a separate practice exercise.

## Questions explored

- Which services contribute the most revenue?
- How do bookings and revenue vary by month, weekday and hour?
- How do washing points compare in revenue?
- What do available ratings and payment methods suggest?

## Stack

Python, pandas, NumPy (data generation), Matplotlib, and SQLite (via Python's standard library).

## Repository contents

```text
.
├── README.md
├── analysis.py                    # cleaning, analysis, charts and SQL execution
├── generate_data.py              # reproducible synthetic-data generator
├── queries.sql                   # six SQLite queries
├── car_wash_bookings.csv         # original synthetic data, including deliberate quality issues
├── cleaned_car_wash_bookings.csv # output from analysis.py
├── charts/                       # five generated charts
└── requirements.txt
```

## Reproduce the analysis

Run from the repository root with Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python analysis.py
```

The input CSV is already included. `analysis.py` prints summary statistics and SQL results, saves a cleaned CSV and refreshes the charts in `charts/`. To regenerate the **synthetic input dataset** using the fixed random seed, run `python generate_data.py` before running the analysis. Regenerating overwrites `car_wash_bookings.csv`.

## Cleaning approach

- Remove duplicate records by `booking_id` (15 duplicate rows in the supplied sample).
- Standardize capitalization and surrounding whitespace in `payment_method`.
- Parse booking dates and derive month and weekday for analysis.
- Leave missing ratings missing, rather than inventing values; exclude them from rating averages.

The included input has 2,061 rows; 2,046 bookings remain after duplicate removal. There are 82 missing ratings in the cleaned sample.

## Results from the included synthetic sample

| Metric | Result |
|---|---|
| Bookings after cleaning | 2,046 |
| Total revenue | PKR 3,533,250 |
| Average booking value | Approximately PKR 1,727 |
| Highest-revenue service | Wax and Polish |
| Busiest weekday | Saturday (438 bookings) |
| Peak booking hour | 12:00 |
| Highest-revenue month | December 2025 |
| Highest-revenue washing point | Main Boulevard |
| Most common payment method | Cash (approximately 54%) |

These figures describe the **generated sample only**. Patterns can reflect the generator's assumptions and random variation, rather than genuine customer behavior.

## Visualizations

![Revenue by service](charts/1_revenue_by_service.png)

![Monthly revenue](charts/2_monthly_revenue.png)

![Bookings by weekday](charts/3_bookings_by_weekday.png)

![Bookings by hour](charts/4_bookings_by_hour.png)

![Payment methods](charts/5_payment_methods.png)

## Interpretation and limitations

Premium services generate substantial revenue in this sample, while weekend and midday bookings are comparatively frequent. These observations could motivate staffing or promotional hypotheses **if** validated using real business records. No causal effect, forecast, or real-world demand conclusion is established here.

The data is intentionally simulated, with predefined service prices, selection probabilities, seasonal weights, and deliberate duplicates and missing values. The analysis therefore demonstrates a workflow—generation, cleaning, aggregation, SQL querying and visualization—rather than evidence of actual market conditions. Revenue is calculated as the sum of listed booking prices; expenses and profitability are not modeled.

## Learning focus and tool use

This project practices data cleaning with pandas, exploratory aggregation, SQLite queries and communicating results through charts. Online learning resources and AI tools were used as aids during project development. Any description of individual contributions in a scholarship application should reflect the work actually performed and the program's disclosure requirements.

## Author

Muhammad Awais | BS Computer Science
