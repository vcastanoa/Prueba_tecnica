"""
Run this file to start the program.

author: Valentina Castaño Aguirre
"""

# Import the modules
from upload_documents_aws import DocumentProcessor
from extract_address import AddressExtractor
from generate_homonyms import HomonymsGenerator
from compute_similarity import AddressSimilarity
import query_coordinates as qc
import draw_map as dm

# Import necessary libraries
import glob
import numpy as np
import os
import re

def export_array_to_csv(array, filename):
        """
        Exports a numpy array to a csv file.

        Args:
            array (numpy array): The numpy array to be exported.
            filename (str): The name of the csv file.
        """
        # Each row of the array is a line in the csv file
        np.savetxt(filename, array, delimiter=",", fmt="%s")

# Read the API keys
with open("../api/keys.txt", "r") as f:
        # Read the file
        input_string = f.read()

        # Close the file
        f.close()

def main():
    '''
    1) First step.
    Upload n documents to AWS S3 bucket.
    We can upload the documents directly using the AWS S3 console, but as we
    are downloading the documents we can also code and test the upload process.

    Notes:
        - Is supposed that the documents are in PDF format.
        
        - We use the library boto3 to upload the documents to AWS S3 console. 
          If you don't have boto3 installed, run the following command:
            pip install boto3

    '''
    print("PHASE 1: DOWNLOAD THE DOCUMENTS FROM AWS S3 BUCKET")
    print(" -- Downloading the documents from AWS S3 bucket -- \n")

    # Read the AWS credentials from the API keys file
    aws_access_key = re.search(r'aws_access_key = "(.*)"', input_string).group(1)
    aws_secret_key = re.search(r'aws_secret_key = "(.*)"', input_string).group(1)
    bucket_name = re.search(r'bucket_name = "(.*)"', input_string).group(1)

    # Create a DocumentProcessor object
    document_processor = DocumentProcessor(
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
        bucket_name=bucket_name,
    )

    # If we want to upload documents to S3, uncomment the following lines
    # file_paths = ["Doc 1.pdf", "Doc 2.pdf"]
    # document_processor.upload_documents_to_s3(file_paths)

    # Download documents from S3
    document_processor.download_documents_from_s3()

    '''
    2) Second step.
    Extract the address from the documents.

    Notes:
        - Is supposed that the documents have a defined and known structure.

        - This algorithm allows to extract the address from different types of documents (
        different structures), e.g.: fiduciary documents, saving accounts documents, etc.
        But is necessary to explicitly define the structure of each type of document.

        - In this case, we have two types of documents: fiduciary and consolidated based on the
        format used by Bancolombia. This format is easy to extract as the address is in a single line
        but in other cases we can use a regular expression (regex) to extract it.

        - If a new type of document is added which has a (very) different structure, the only thing
        to do is to add a new method to the AddressExtractor class with the corresponding logic.

        - We use the PyPDF2 library to extract the text from the documents. If you don't have PyPDF2
        installed, run the following command:
            pip install PyPDF2

    '''
    print("\n")
    print("PHASE 2: EXTRACT THE ADDRESS FROM THE DOCUMENTS")
    print(" -- Extracting the address from the documents -- \n")

    # Get all the documents in the data folder using the glob module
    document_names = glob.glob("../data/*.pdf")

    # If the name of the document contains the word "fidu", it is a fiduciary document,
    # if contains the word "cons", it is a consolidated document. Otherwise, the default
    # type of document is consolidated.
    documents = {}

    for document_name in document_names:
        if "fidu" in document_name.lower():
            documents[document_name] = "fiduciary"
        elif "cons" in document_name.lower():
            documents[document_name] = "consolidated"
        else:
            documents[document_name] = "consolidated"

    # Create an AddressExtractor object
    extractor = AddressExtractor(documents)

    # Extract the addresses from the documents
    dict_addresses = extractor.locate_addresses()

    for file, address in dict_addresses.items():
        print(f"Document: {file}")
        print(f"Address: {address}")
        print("\n")

    addresses = dict_addresses.values()

    '''
    3) Third step.
    Generate the homonyms.

    Notes:
        - The homonyms are generated using a dictionary of words. In this case, inside the
        corresponding module there is a dictionary of words synonyms of "calle" and "carrera", 
        as well as "#" and the " - " character.
        This approach allows to add / remove / merge words in the dictionary as easy as modifying 
        one single list in the code.

        - Is supposed that the "Carreras" and "Calles" are not homonyms between them, but if this
        is the case it can be easily modified adding the corresponding words to the dictionary.
    
    '''
    print("\n")
    print("PHASE 3: GENERATE THE HOMONYMS")
    print(" -- Generating the homonyms -- \n")

    # Create a HomonymsGenerator object
    generator = HomonymsGenerator()

    # Generate the homonyms
    homonyms = {}

    for address in addresses:
        homonyms[address] = generator.generate_homonyms(address)

    print("Homonyms generated: \n")
    print(homonyms)

    # Export the homonyms to a csv file
    file_path = os.path.join('../data/', 'homonyms.csv')  # Construct the absolute file path

    generator.export_csv(homonyms, file_path)  # Export the CSV file

    '''
    4) Fourth step.
    Compute the similarity between the addresses.

    Notes:
        - The similarity between the addresses is computed using the Damerau-Levenshtein distance.

        - The Damerau-Levenshtein distance is the minimum number of operations (insertions, deletions,
        substitutions and transpositions) required to transform one string into another.

        - This choice is motivated by the fact that this distance takes into account if the characters
        are adjacent or not (transpositions), as well as how many characters are different (insertions,
        deletions and substitutions). This penalizes less small differences of position between the
        characters and allows to obtain a more accurate similarity measure.

        - We need a percentage of similarity and not a distance, so we normalize the distance dividing
        it by the length of the longest string. (0 distance = 100% similarity, 1 distance = 0% similarity)

        - Is interpreted that if the similarity between two addresses is greater than 0.9, the addresses
        to be stored are the original, otherwise we would have several addresses that refer to the same
        place and does not make sense to plot them all in the map.
    '''
    print("\n")
    print("PHASE 4: COMPUTE THE SIMILARITY BETWEEN THE ADDRESSES")
    print(" -- Computing the similarity between the addresses -- \n")

    # Read the homonyms from the csv file
    folder_path = os.path.expanduser('../data/')  # Get the absolute path of the folder
    file_path = os.path.join(folder_path, 'homonyms.csv')  # Construct the absolute file path

    homonyms_list = generator.read_csv(file_path)
    # Create a dictionary with the addresses and their homonyms to associate them
    homonyms = {}
    
    i = 0
    for address in addresses:
        homonyms[address] = homonyms_list[i]
        i = i + 1


    # Compute the similarity between the addresses and their homonyms for each document
    scores = {}

    for address in addresses:
        similarity = AddressSimilarity(address, homonyms[address])
        score = similarity.get_all_scores()

        scores[address] = score


     # Scores is a dictionary of dictionaries with the similarity scores for each original address
     # scores -> { original_address_1: { original_address_1: 1, homonym_1: 0.8, homonym_2: 0.6, ... },
     #             original_address_2: { original_address_2: 1, homonym_1: 0.8, homonym_2: 0.6, ... }}

    # Filter the scores to only keep > 0.9 similarity
    threshold = 0.9
    for address, score in scores.items():
        scores[address] = {k: v for k, v in score.items() if v > threshold}

    # Filter the addresses that do not have any homonym with > 0.9 similarity
    addresses = [k for k, v in scores.items() if v]

    print("Similarity scores after filter: \n")
    print(scores)

    print("Addresses after filter: \n")
    print(addresses)

    folder_path = os.path.expanduser('../data')  # Get the absolute path of the folder
    file_path = os.path.join(folder_path, 'filtered addresses.csv')  # Construct the absolute file path
    export_array_to_csv(["Original Address",*addresses], file_path)

    '''
    5) Fifth step.
    Access the Google Maps API to get the coordinates of the addresses.

    Notes:
        - We are supposing that the addresses are in Medellin, so we add the city and the country
        to the addresses. If is not the case we simply can delete this step inside the module.

        - We use the library googlemaps to access the Google Maps API. This library is installed
        using the pip command.
            pip install googlemaps

    '''
    print("\n")
    print("PHASE 5: GET THE COORDINATES OF THE ADDRESSES")
    print(" -- Getting the coordinates of the addresses -- \n")

    # Get the coordinates of the addresses
    coordinates = qc.get_multiple_coordinates(addresses)

    print("Coordinates: \n")
    print(coordinates)

    # Make an array with the addresses and their coordinates
    addresses_coordinates = []

    for address, coordinate in coordinates.items():
        addresses_coordinates.append([address, coordinate[0], coordinate[1]])

    # Export the addresses and their coordinates to a csv file
    addresses_coordinates = [["Address", "Latitude", "Longitude"],*addresses_coordinates]
    
    folder_path = os.path.expanduser('../data')  # Get the absolute path of the folder
    file_path = os.path.join(folder_path, 'addresses_coordinates.csv')  # Construct the absolute file path
    export_array_to_csv(addresses_coordinates, file_path)

    '''
    6) Sixth step.
    Generate the map with the addresses.

    Notes:
        - The map is generated using the Folium library.

        - The map is generated in a html file which is downloaded to the current directory.
        You can open the file with any browser.
        
    '''
    print("\n")
    print("PHASE 6: GENERATE THE MAP WITH THE ADDRESSES")
    print(" -- Generating the map with the addresses -- \n")

    # Get list of coordinates
    coordinates_list = list(coordinates.values())

    html_map = dm.generate_html_map(coordinates_list)

    # Save the HTML document to a file
    with open('../map/google_map.html', 'w') as file:
        file.write(html_map)

    print("HTML document with Google Map generated successfully.")

if __name__ == "__main__":
    main()