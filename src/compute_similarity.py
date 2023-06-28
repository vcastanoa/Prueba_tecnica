import numpy as np
from collections import defaultdict


class DamerauLevenshteinDistance:
    """
    Calculates the Damerau-Levenshtein distance between two addresses.

    The Damerau-Levenshtein distance is a measure of the minimum number of operations
    (insertions, deletions, substitutions, and transpositions) required to transform
    one address into another.

    """

    def __init__(self, first_address, second_address):
        """
        Initializes the DamerauLevenshteinDistance object with the given addresses.

        Args:
            first_address (str): The first address.
            second_address (str): The second address.
        """

        self.first_address = first_address
        self.second_address = second_address

        self.len_first_address = len(first_address)
        self.len_second_address = len(second_address)
        
        self.max_distance = self.len_first_address + self.len_second_address
        self.char_positions = defaultdict(int)
        
        # Create a distance matrix with additional rows and columns for boundary conditions
        self.distance_matrix = [[0] * (self.len_second_address + 2) for _ in range(self.len_first_address + 2)]

    def calculate_distance(self):
        """
        Calculates and returns the Damerau-Levenshtein distance between the two addresses.

        Returns:
            int: The Damerau-Levenshtein distance.

        Notes:
            This method fills in a distance matrix where each entry (i, j) represents the minimum distance
            between the substrings of the first address up to position i and the substrings of the
            second address up to position j.
        """

        self.distance_matrix[0][0] = self.max_distance

        # Initialize the first row and column of the distance matrix
        for i in range(self.len_first_address + 1):
            self.distance_matrix[i + 1][0] = self.max_distance
            self.distance_matrix[i + 1][1] = i

        for i in range(self.len_second_address + 1):
            self.distance_matrix[0][i + 1] = self.max_distance
            self.distance_matrix[1][i + 1] = i

        # Fill in the rest of the distance matrix
        for i in range(1, self.len_first_address + 1):
            previous_matching_j = 0
            for j in range(1, self.len_second_address + 1):
                previous_matching_i = self.char_positions[self.second_address[j - 1]]

                # Calculate the cost of the current operation (insertion, deletion, substitution, or transposition)
                cost = 1
                if self.first_address[i - 1] == self.second_address[j - 1]:
                    cost = 0
                    previous_matching_j = j

                # Calculate the costs of the possible operations
                insertion = self.distance_matrix[i + 1][j] + 1
                deletion = self.distance_matrix[i][j + 1] + 1
                substitution = self.distance_matrix[i][j] + cost
                transposition = self.distance_matrix[previous_matching_i][previous_matching_j] + (
                            i - previous_matching_i - 1) + 1 + (j - previous_matching_j - 1)

                # Choose the minimum cost among all possible operations
                self.distance_matrix[i + 1][j + 1] = min(insertion, deletion, substitution, transposition)

            # Update the last known position of the character in the first address
            self.char_positions[self.first_address[i - 1]] = i

        # The final distance is the value in the bottom-right corner of the distance matrix
        return self.distance_matrix[self.len_first_address + 1][self.len_second_address + 1]


class AddressSimilarity:
    """
    Calculates the similarity between an address and a list of homonyms addresses.
    """
    def __init__(self, original_address, homonyms_address):
        """
        Initializes the AddressSimilarity object with the given addresses.

        Args:
            original_address (str): The original address.
            homonyms_address (list): The list of homonyms addresses.
            
        """
        self.original_address = original_address
        self.homonyms_address = homonyms_address

    def get_similarity_score(self, first_address, second_address):
        """
        Calculates and returns the similarity score between the two addresses.

        Args:
            first_address (str): The first address.
            second_address (str): The second address.

        Returns:
            float: The similarity score.
        """
        distance = DamerauLevenshteinDistance(first_address, second_address).calculate_distance()

        length_first_address = len(first_address)
        length_second_address = len(second_address)
        
        max_length_address = np.max([length_first_address, length_second_address])
        
        score = 1 - distance / max_length_address
        return score

    def get_all_scores(self):
        """
        Calculates and returns the similarity score between the original address and each homonym address.

        Returns:
            dict: A dictionary with the similarity score for each homonym address.
        """
        dict_scores = {}
        for address in self.homonyms_address:
            score = self.get_similarity_score(self.original_address, address)
            dict_scores[address] = score
        return dict_scores

    def filter_best_scores(self, dict_scores, threshold):
        """
        Filters the similarity scores and returns the addresses with a score above the threshold.

        Args:
            dict_scores (dict): A dictionary with the similarity score for each homonym address.
            threshold (float): The threshold for the similarity score.

        Returns:
            list: A list with the addresses with a score above the threshold.
        """
        

        dict_filtered_scores = {}
        for address, score in dict_scores.items():
            if score >= threshold:
                dict_filtered_scores[address] = score
        list_filtered_addresses = list(dict_filtered_scores.keys())
        return list_filtered_addresses

    

if __name__ == "__main__":
    # Test the Damerau-Levenshtein distance function
    print("Test the Damerau-Levenshtein distance function")

    original_address = "Carrera 78A No 47-15"
    homonyms_address = ["Carrera 78A # 47-15", "Kra 78A Num 47-15"]

    distance = DamerauLevenshteinDistance(original_address, homonyms_address[0]).calculate_distance()
    print("Distance between {} and {} is {}".format(original_address, homonyms_address[0], distance))
    print("\n")

    # Test the similarity score function
    print("Test the similarity score function")

    similarity = AddressSimilarity(original_address, homonyms_address)
    score = similarity.get_similarity_score(original_address, homonyms_address[0])
    print("Similarity score between {} and {} is {}".format(original_address, homonyms_address[0], score))
    print("\n")

    # Test the similarity of an address against a list of homonyms addresses
    print("Test the similarity of an address against a list of homonyms addresses")

    scores = similarity.get_all_scores()
    print("Similarity scores between {} and {} are {}".format(original_address, homonyms_address, scores))
    print("\n")

    # Test the filtering of the best scores
    print("Test the filtering of the best scores")

    threshold = 0.9
    filtered_addresses = similarity.filter_best_scores(scores, threshold)
    print("Filtered addresses with more than {}% similarity are {}".format(threshold * 100, filtered_addresses))
