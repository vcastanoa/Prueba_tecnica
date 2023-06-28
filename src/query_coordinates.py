import googlemaps
from datetime import datetime
import re

with open("../api/keys.txt", "r") as f:
        # Read the file
        input_string = f.read()

        # Close the file
        f.close()

def get_coordinates(address):
    """
    Get the latitude and longitude of an address

    Parameters
    ----------
    address : str
        The address to be queried.

    Returns
    -------
    latitude : float
    longitude : float
    """
    gmaps_key = re.search(r'gmaps = "(.*)"', input_string).group(1)
    gmaps = googlemaps.Client(key=gmaps_key)

    # Geocoding an address in Medellin, Colombia to improve the accuracy of the results
    geocode_result = gmaps.geocode(address + ', Medellin, Colombia')

    if geocode_result:
        # Extract latitude and longitude
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']

        return latitude, longitude

    else:
        print(f'No coordinates found for the address {address}.')


def get_multiple_coordinates(addresses):
    """
    Get the latitude and longitude of multiple addresses

    Parameters
    ----------
    addresses : list
        A list of addresses to be queried.

    Returns
    -------
    coordinates : dict
        A dictionary with the addresses as keys and the coordinates as values.
    """

    # Query the coordinates of each address
    coordinates = {}
    for address in addresses:
        latitude, longitude = get_coordinates(address)
        coordinates[address] = (latitude, longitude)

    return coordinates


if __name__ == "__main__":
    # Test the get_coordinates function
    print("Test the get_coordinates function")

    address = "Cra. 57a #62 92"
    latitude, longitude = get_coordinates(address)
    print("The coordinates of {} are ({}, {})".format(address, latitude, longitude))
    print("\n")

    # Test the query of multiple addresses
    print("Test the query of multiple addresses")

    addresses = ["Cra. 57a #62 92", "Cl. 43a #1 50", "Cra. 78A #47-15"]
    coordinates = get_multiple_coordinates(addresses)
    print("The coordinates are {}".format(coordinates))
    print("\n")

    new_york_coordinates = (40.75, -74.00)
    

