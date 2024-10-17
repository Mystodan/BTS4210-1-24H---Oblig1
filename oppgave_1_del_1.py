import pandas as pd
import folium as fol
import dash
from dash import html

READFILE = "havforsk.csv"
ENCODE = "Windows-1252"




# Define the Oslofjord boundaries
OSLOFJORD_LAT_MIN, OSLOFJORD_LAT_MAX  = 58.5, 60.0
OSLOFJORD_LON_MIN, OSLOFJORD_LON_MAX = 10.0, 11.5

# Read the data from the CSV file
df = pd.read_csv(READFILE, delimiter=";", encoding=ENCODE, engine="python")

# Function to check if a point is within the Oslofjord area
is_within_oslofjord = lambda lat, lon: OSLOFJORD_LAT_MIN <= lat <= OSLOFJORD_LAT_MAX and OSLOFJORD_LON_MIN <= lon <= OSLOFJORD_LON_MAX

# Filter the DataFrame to include only points within the Oslofjord area
df_oslofjord = df[df.apply(lambda row: is_within_oslofjord(row["latitude"], row["longitude"]), axis=1)]


# Create the map centered around the Oslofjord area
map = fol.Map(location=[df_oslofjord["latitude"].mean(), df_oslofjord["longitude"].mean()], zoom_start=8)

# Add markers for each fish within the Oslofjord area
for fish in df_oslofjord.iterrows():
    popup = f"Art: {fish[1]['species']}\nLengde: {fish[1]['length']} \nVekt: {fish[1]['weight']} \nDato: {fish[1]['date']}"
    fol.Marker([fish[1]["latitude"], fish[1]["longitude"]], popup=(popup)).add_to(map)
    
# Save the map to an HTML file
map.save("map.html")

# Create the Dash app
app = dash.Dash()
# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("Fisk rundt Oslofjorden"),
        # Add an iframe to display the map
        html.Iframe(srcDoc=open("map.html", "r", encoding="utf-8").read(), width="100%", height="600")
    ]
)



