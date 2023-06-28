import csv
import numpy as np

class HomonymsGenerator:
    """
    A class used to generate homonyms for a given address.
    The strategy is:
        1. Identify the words that can be replaced by other words.
        2. Generate all the possible combinations of the words that can be replaced.
        3. Return the combinations.
    """

    def __init__(self):
        """
        Initialize the class. 
        """
        self.word_replacements = {
            'vertical street': ['Cra', 'Carrera', 'Kra', 'K','CRA'],
            'horizontal street': ['Cl', 'Calle', 'C','Cl.'],
            '#': ['Nro', 'Numero', 'Num', '#'],
            '-': [' ', '-']}


    def generate_homonyms(self, address):
        """
        Generate homonyms for the given address.

        :param address: The address to generate homonyms for.
        :type address: str
        :return: A list of possible homonyms for the address.
        :rtype: list[str]
        """
        # Split the address into individual words
        words = address.split()

        # Initialize a list to store homonyms, starting with an empty list
        homonyms = [[]]

        # Iterate through each word in the address
        for word in words:
            found_replacements = False

            # Iterate through each category and its associated replacements
            for category, replacements in self.word_replacements.items():

                # Check if the word has any replacements in the current category
                if word in replacements:
                    found_replacements = True

                    # Create a new list to store updated homonyms
                    new_homonyms = []

                    # Iterate through each replacement for the word
                    for replacement in replacements:

                        # Iterate through each existing homonym
                        for homonym in homonyms:
                            # Append the replacement to each homonym and add it to the new list
                            new_homonyms.append(homonym + [replacement])

                    # Update the list of homonyms with the new list
                    homonyms = new_homonyms

            # If no replacements were found for the word, append it to each existing homonym
            if not found_replacements:
                for homonym in homonyms:
                    homonym.append(word)
                    
        # Drop the original address from the list of homonyms
        homonyms = [homonym for homonym in homonyms if homonym != words]

        return [' '.join(homonym) for homonym in homonyms]

    def export_csv(self, homonyms, output_file_path):
        """
        Export the homonyms to a CSV file.

        :param homonyms: The homonyms to export.
        :type homonyms: list[str]
        :param output_file_path: The path to the output file.
        :type output_file_path: str
        """
        # Export in CSV with the following format:
        # Original Address, Homonym 1, Homonym 2, Homonym 3, ...

        with open(output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            addresses = []

            for address , homonyms in homonyms.items():
                addresses.append(homonyms)
            
            # Transpose the list of addresses to get the desired format

            writer.writerows(addresses)

        print("File exported successfully with the name: " + output_file_path)

    def read_csv(self, input_file_path):
        """
        Read the homonyms from a CSV file.

        :param input_file_path: The path to the input file.
        :type input_file_path: str
        :return: The homonyms read from the file.
        :rtype: list[str]
        """
        # Read in CSV with the following format:
        # Original Address, Homonym 1, Homonym 2, Homonym 3, ...

        with open(input_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            addresses = []

            for row in reader:
                addresses.append(row)

        return addresses
    
if __name__ == '__main__':
    # Test for generate multiple homonyms with different words and symbols
    print("Test for generate multiple homonyms with different words and symbols")
    
    generator = HomonymsGenerator()
    addresses = ['Cra. 70 # 30-25', 'Calle 30 # 40 - 50']
    for address in addresses:
        homonyms = generator.generate_homonyms(address)
        print(f'Original Address: {address}')
        print(f'Homonyms: {homonyms}')
        print('------------------------')

    # Test for generate multiple homonyms to a single address
    print("Test for generate multiple homonyms to a single address")

    address = 'Cra. 70 # 30-25'
    homonyms = {}
    homonyms[address] = generator.generate_homonyms(address)
    print(f'Original Address: {address}')
    print(f'Homonyms: {homonyms}')
    print('------------------------')

    # Export the homonyms to a CSV file
    print("Export the homonyms to a CSV file")

    generator.export_csv(homonyms, 'homonyms.csv')

    # Read the homonyms from a CSV file
    print("Read the homonyms from a CSV file")

    addresses = generator.read_csv('homonyms.csv')
    print(f'Addresses: {addresses}')


    
