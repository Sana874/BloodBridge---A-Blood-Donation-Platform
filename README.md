# BloodBridge — A Blood Donation Platform

An AI-powered platform that connects blood recipients with compatible donors using medical compatibility rules, real-world geolocation filtering, and heuristic-based ranking — built with Python and Streamlit.

---

## The Problem

Despite the presence of numerous donors, the challenge in emergencies is quickly identifying the *right* donor — one who is medically compatible, geographically reachable, and available. BloodBridge solves this by decomposing the donor-matching task into three computational components.

---

## How It Works

**Step 1 — Medical Matching (Constraint Satisfaction Problem)**

Blood type compatibility is modeled as a CSP where the recipient's blood group is the variable and compatible donor types form the domain. A dictionary-based lookup enforces medically accepted transfusion rules — for example, an A+ recipient can receive from A+, A−, O+, and O− donors only.

**Step 2 — Geographic Filtering (Haversine Formula)**

Donors outside a user-defined radius are excluded using the Haversine formula, which computes real-world curved distance between two lat/lon coordinates. This ensures only logistically feasible donors are considered in emergencies.

**Step 3 — Heuristic Donor Ranking**

Filtered donors are ranked by a custom heuristic score combining two factors:
- **Proximity** — donors closer to the recipient score higher for faster response
- **Blood group rarity** — rarer blood types (e.g. AB−, O−) are weighted higher to encourage rare donations

---

## Features

- Blood type compatibility filtering based on medically accepted transfusion rules
- Location-based donor search using the Haversine formula with configurable radius
- Heuristic scoring that balances proximity and blood group rarity
- Interactive map view of donor locations using PyDeck
- Ranked donor table showing name, blood group, hospital, contact, and distance
- Top 3 donor cards for immediate contact at a glance
- Streamlit sidebar for entering recipient details (name, age, blood group, city, state, radius)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Python, Streamlit |
| Geolocation | Haversine Formula, PyDeck |
| Matching Logic | Constraint Satisfaction Problem (CSP) |
| Ranking | Custom Heuristic Scoring |
| Data | CSV (donor dataset with lat/lon, city coordinates dataset) |

---

## Project Structure

```
BloodBridge---A-Blood-Donation-Platform/
│
├── app2.py                                      # Main Streamlit application
├── final_updated_donor_data_with_coords.csv     # Donor dataset with geolocation
├── BloodBridge.pdf                              # Project report
├── README.md
```

---

## Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/Sana874/BloodBridge---A-Blood-Donation-Platform.git
cd BloodBridge
```

**2. Install dependencies**
```bash
pip install streamlit pandas pydeck
```

**3. Run the app**
```bash
streamlit run app2.py
```

---

## Usage

1. Enter your name, age, required blood group, city, state, and maximum search radius in the sidebar
2. The system filters donors by blood type compatibility and geographic proximity
3. View matching donors on the interactive map
4. Review the ranked donor table sorted by heuristic score
5. Contact one of the top 3 highlighted donor cards directly

---

## Future Scope

- Live donor availability — integrate last donation date and response status
- Real-time SMS/app alerts to notify nearby donors automatically
- Urgency-based scoring to prioritize donors for critical cases

---

## Team

| Name | ID |
|------|----|
| Sana Firdous | 2022A7PS0193U |
| Tarunikka Suresh | 2022A7PS0199U |
| Mohammed Raashid | 2022A7PS0259U |

BITS Pilani Dubai Campus

---

## Tech Used
`Python` · `Streamlit` · `PyDeck` · `Pandas` · `Haversine Formula` · `CSP` · `Geolocation`
