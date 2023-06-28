import folium
import re

with open("../api/keys.txt", "r") as f:
        # Read the file
        input_string = f.read()

        # Close the file
        f.close()

def generate_html_map(coordinates):
    """
    Generate an HTML document with a Google Map.

    Parameters
    ----------
    api_key : str
        The Google Maps API key.
    coordinates : list of tuple
        List of coordinates, where each coordinate is a tuple containing
        latitude and longitude values.

    Returns
    -------
    html : str
        The HTML document with the map.
    """
    api_key = re.search(r'gmaps = "(.*)"', input_string).group(1)

    # Calculate the center coordinates
    center_lat = sum(lat for lat, lng in coordinates) / len(coordinates)
    center_lng = sum(lng for lat, lng in coordinates) / len(coordinates)

    # Create a map object using Folium
    map = folium.Map(location=[center_lat, center_lng], zoom_start=12)

    # Add markers to the map for each coordinate
    for lat, lng in coordinates:
        marker = folium.Marker([lat, lng])
        marker.add_to(map)

    # Generate the HTML string for the map
    map_html = map.get_root().render()

    # Create the HTML document with the map
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Map</title>
        <style>
            #map{{
                height: 100%;
            }}
            html, body{{
                height: 100%;
                margin: 0;
                padding: 0;
            }}
        </style>
        <script src="https://maps.googleapis.com/maps/api/js?key={api_key}"></script>
    </head>
    <body>
        <div id="map">{map_html}</div>
        <script>
            var map = new google.maps.Map(document.getElementById('map'), {{
                center: {{lat: {center_lat}, lng: {center_lng}}},
                zoom: 12
            }});

            {generate_marker_script(coordinates)}
        </script>
    </body>
    </html>
    '''

    return html


def generate_marker_script(coordinates):
    """
    Generate JavaScript code for adding markers to the map.

    Parameters
    ----------
    coordinates : list of tuple
        List of coordinates, where each coordinate is a tuple containing
        latitude and longitude values.

    Returns
    -------
    script : str
        JavaScript code for adding markers to the map.
    """
    script = ""
    for lat, lng in coordinates:
        script += f'''
            var marker = new google.maps.Marker({{
                position: {{lat: {lat}, lng: {lng}}},
                map: map
            }});
        '''
    return script


if __name__ == "__main__":
    

    # Define the coordinates
    coordinates = [
        (4.710989, -74.072092),  # Bogota
        (6.244203, -75.581211),  # Medellin
        (11.004107, -74.806981),  # Cartagena
        (3.42158, -76.5205)  # Cali
    ]

    # Generate the HTML document with the map
    html_map = generate_html_map(coordinates)

    # Save the HTML document to a file
    with open('google_map.html', 'w') as file:
        file.write(html_map)

    print("HTML document with Google Map generated successfully.")
