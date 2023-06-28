# Technical Assessment

This program extracts addresses from documents, generates homonyms, computes similarity between addresses, retrieves coordinates using the Google Maps API, and generates a map with the addresses. The following are the instructions and recommendations for running the technical assessment, as well as the suppositions made for the development of the code.

# Prerequisites
The program  requires the following libraries to upload the documents to AWS S3 console, to access the Google Maps API, generate the map, and working with PDF documents:
- Python 3.x
- folium
- PyPDF2
- googlemaps
- boto3

All the libraries are easily installables with pip, you can use this command in order to install all of them:

            pip install folium PyPDF2 googlemaps boto3

# Usage
# Technical Assessment

This program extracts addresses from documents, generates homonyms, computes similarity between addresses, retrieves coordinates using the Google Maps API, and generates a map with the addresses. The following are the instructions and recommendations for running the technical assessment, as well as the suppositions made for the development of the code.

# Prerequisites
The program  requires the following libraries to upload the documents to AWS S3 console, to access the Google Maps API, generate the map, and working with PDF documents:
- Python 3.x
- folium
- PyPDF2
- googlemaps
- boto3

All the libraries are easily installables with pip, you can use this command in order to install all of them:

            pip install folium PyPDF2 googlemaps boto3

# Usage
All the scripts in the src subdirectory are functionals independtly, each one has independt tests and examples of use. To compile all the project (from the download of the AWS files to the generation of the map) all you have to do is replace the 'key.txt' file in the subdirectory /api/ with your own API keys and compile the main.py script. Feel free to explore and run the individual scripts within the subdirectory.

The input files with the address are already uploaded to AWS, however, in the main code there is also code to upload local files to AWS S3.
