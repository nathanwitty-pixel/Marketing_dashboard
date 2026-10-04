# Shop birthdays

**This file is the source of truth for when each shop opened.** A shop's birthday (its opening
anniversary) is a sales hook — the dashboard flags it **30 days ahead** so an offer / posts can be
planned for that shop. Edit the table below and re-run the generators; `lib/shop_birthdays.py`
reads this file at build time. No code change needed.

Rules for editing:
- Keep the pipe format `| Shop | Month | Day | Year | Note |`. **Shop** is the dashboard shop name
  (as in [shop-regions.md](shop-regions.md); matched case-insensitively — `KTDA Shop`, `Tanzania`
  and `Nairobi` resolve to KTDA, Sinza and Starmall).
- **Month** = full name (`October`). A blank or unknown month → the shop gets **no** birthday until
  it's filled in. A blank **Day** → the 1st of that month (flagged "day not set").
- **Year** = the opening year (the age is counted from it). Blank → the birthday shows without an age.

## Shop → opening date

| Shop | Month | Day | Year | Note |
|---|---|---|---|---|
| Starmall | | | | Nairobi — opening date not given yet |
| Mombasa | July | 19 | 2021 | |
| Nakuru | January | 5 | 2019 | |
| Eldoret | September | 11 | 2019 | |
| Kisumu | October | | 2020 | day not given |
| Meru | | 20 | 2022 | month not given (sheet said "MERU") — fill in the month |
| Thika | July | 3 | 2021 | |
| Hazina | June | | 2022 | day not given |
| Kitengela | November | 29 | 2022 | |
| Nanyuki | October | 2 | 2023 | sheet said "OCTOMBER" |
| Kakamega | December | 1 | 2023 | |
| Hilton | April | 5 | 2024 | |
| Sinza | September | 20 | 2024 | Tanzania |
| Uganda | August | 1 | 2025 | |
| Kisii | November | 28 | 2025 | |
| KTDA | January | 30 | 2026 | |
| Busia | March | 27 | 2026 | |
| Rongai | April | 24 | 2026 | |

## Where it shows

- **Window:** from **30 days before** the birthday to **1 day after** (`upcoming(today)`).
  The text reads `🎂 3rd birthday in 12 days` / `🎂 3rd birthday today` / `🎂 3rd birthday was yesterday`.
- **Shops Efficiency** — a 🎂 badge beside the shop name ([shops-efficiency.md](shops-efficiency.md)).
- **Bags on vs off Offer** — a 🎂 badge beside the shop in the shops table ([bags-on-offer.md](bags-on-offer.md)).
- **Push Planner** — an "Upcoming shop birthdays" note: plan a push for that shop's birthday week
  ([push-planner.md](push-planner.md)).
- **Monthly Report** — the shops with a birthday in the report month ([monthly-report.md](monthly-report.md)).
