# Technical Assessment
The following are the instructions and recommendations for running the technical assessment, as well as the suppositions made for the development of the code.

The program  requires boto3, googlemaps, Folium, and pypdf2  libraries to upload the documents to AWS S3 console, to access the Google Maps API, generate the map, and working with PDF documents in Python respectively. To install run the following command:
    pip install boto3
    pip install googlemaps
    pip install folium
    pip install pypdf2
    
First, we need to have one or more documents uploaded to AWS to download and extract addresses from them.

