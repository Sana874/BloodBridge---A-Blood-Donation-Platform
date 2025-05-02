import streamlit as st
import pandas as pd
import pydeck as pdk
from math import radians, cos, sin, asin, sqrt

# Set up the Streamlit page
st.set_page_config(page_title="Bloodbridge - India Donor Finder", layout="wide")

# Load donor dataset
@st.cache_data
def load_donor_data():
    df = pd.read_csv(r"C:\Users\abkal\Desktop\ai project\final_updated_donor_data_with_coords.csv")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    return df

# Load cities dataset
@st.cache_data
def load_city_data():
    df = pd.read_csv("cities.csv")
    df = df[['city', 'state', 'latitude', 'longitude']]
    df.columns = ['City', 'State', 'Latitude', 'Longitude']
    return df

donor_df = load_donor_data()
cities_df = load_city_data()

# Blood compatibility
def get_compatible_blood_groups(blood_group):
    compatibility = {
        "O-": ["O-"],
        "O+": ["O-", "O+"],
        "A-": ["O-", "A-"],
        "A+": ["O-", "O+", "A-", "A+"],
        "B-": ["O-", "B-"],
        "B+": ["O-", "O+", "B-", "B+"],
        "AB-": ["O-", "A-", "B-", "AB-"],
        "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
    }
    return compatibility.get(blood_group.upper(), [])

# Haversine formula for distance # CSP PART
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return R * c

# Heuristic score with distance filter #HEURISTICS 
def compute_scores(df, user_lat, user_lon, required_blood, max_distance_km=150):
    rare_weight = {
        "AB-": 1.5, "B-": 1.3, "A-": 1.3, "O-": 1.4,
        "AB+": 1.0, "A+": 0.8, "B+": 0.8, "O+": 0.7
    }
    
    scores = []
    distances = []
    for _, row in df.iterrows():
        d = haversine(user_lat, user_lon, row['Latitude'], row['Longitude'])
        distances.append(d)
        rarity_score = rare_weight.get(row['Blood Group'], 1.0)
        score = (1 / (d + 0.1)) + rarity_score
        scores.append(score)
    
    df = df.copy()
    df['Distance (km)'] = distances
    df['Heuristic Score'] = scores
    df = df[df['Distance (km)'] <= max_distance_km]
    df.sort_values(by='Heuristic Score', ascending=False, inplace=True)
    return df

# ------------------------- UI --------------------------

st.markdown("<h1 style='text-align: center; color: red;'>Bloodbridge - Find a Donor</h1>", unsafe_allow_html=True)
st.sidebar.header("Search for a Blood Donor")

user_name = st.sidebar.text_input("Your Name")
user_age = st.sidebar.number_input("Your Age", min_value=1, max_value=100)
required_blood = st.sidebar.selectbox("Required Blood Group", sorted(donor_df['Blood Group'].unique()))
selected_state = st.sidebar.selectbox("Your State", sorted(cities_df['State'].unique()))

selected_state_cities = cities_df[cities_df['State'] == selected_state]
filtered_cities = selected_state_cities['City'].unique()
selected_city = st.sidebar.selectbox("Your City", sorted(filtered_cities))

max_distance = st.sidebar.slider("Maximum Search Distance (km)", 10, 1000, 150)

search = st.sidebar.button("Search")

if search:
    user_city_row = cities_df[(cities_df['City'] == selected_city) & (cities_df['State'] == selected_state)]
    
    if user_city_row.empty:
        st.warning("City coordinates not found.")
    else:
        user_lat = user_city_row['Latitude'].values[0]
        user_lon = user_city_row['Longitude'].values[0]

        compatible_bloods = get_compatible_blood_groups(required_blood)
        matching_donors = donor_df[donor_df['Blood Group'].isin(compatible_bloods)]

        if matching_donors.empty:
            st.warning("No matching donors found.")
        else:
            ranked_donors = compute_scores(matching_donors, user_lat, user_lon, required_blood, max_distance)

            if ranked_donors.empty:
                st.warning(f"No donors found within {max_distance} km.")
            else:
                st.success(f"Found {len(ranked_donors)} matching donors within {max_distance} km.")
                
                st.subheader("📍 Donor Locations on Map")
                st.pydeck_chart(pdk.Deck(
                    initial_view_state=pdk.ViewState(
                        latitude=user_lat,
                        longitude=user_lon,
                        zoom=5,
                    ),
                    layers=[ 
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=ranked_donors,
                            get_position='[Longitude, Latitude]',
                            get_color='[255, 0, 0, 160]',
                            get_radius=8000,
                            pickable=True
                        )
                    ],
                    tooltip={"text": "Name: {Name}\nBlood: {Blood Group}\nDistance: {Distance (km)} km"}
                ))

                st.subheader("🧾 Ranked Donor List")
                st.dataframe(ranked_donors[[ 
                    'Name', 'Blood Group', 'State', 'City', 'Contact No.',
                    'Email', 'Distance (km)', 'Hospital Name'
                ]].reset_index(drop=True))

                # ---------------- Top 3 Donors Summary ----------------
                st.subheader("Top 3 Donors")
                top_3 = ranked_donors.head(3)[[ 
                    'Name', 'Blood Group', 'City', 'State', 'Hospital Name', 'Contact No.', 'Distance (km)'
                ]].reset_index(drop=True)

                for idx, row in top_3.iterrows():
                    st.markdown(f"""
                    <div style="background-color:#000000; color:#ffffff; padding:15px; border-radius:10px; margin-bottom:10px;">
                        <b>Donor #{idx+1}</b><br>
                        <b>Name:</b> {row['Name']}<br>
                        <b>Blood Group:</b> {row['Blood Group']}<br>
                        <b>Hospital:</b> {row['Hospital Name']}<br>
                        <b>Location:</b> {row['City']}, {row['State']}<br>
                        <b>Contact:</b> {row['Contact No.']}<br>
                        <b>Distance:</b> {row['Distance (km)']:.2f} km
                    </div>
                    """, unsafe_allow_html=True)
