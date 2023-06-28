from PyPDF2 import PdfReader

class AddressExtractor:
    """
    A class used to extract addresses from client documents based on the client document type.
    
    This class suppose that the structure of the documents is the same for all
    the documents of the same type. (e.g. all the fiduciary documents have the address
    in the same place).

    """

    def __init__(self, documents):
        """
        Initialize the class with a dictionary of documents and their kinds.

        :param documents: dict, a dictionary where the keys are document file paths and the values are document kinds.
        """
        self.documents = documents
    
    def locate_addresses(self):
        """
        Locate the addresses for all the documents.

        :return: dict, a dictionary where the keys are document file paths and the values are the corresponding addresses.
        """
        addresses = {}
        for file, kind in self.documents.items():
            address = self.locate_address(file, kind)
            addresses[file] = address
        return addresses
    
    def locate_address(self, file, kind):
        """
        Locate the address in a given client document.

        :param file: str, the path to the PDF file to be processed.
        :param kind: str, the type of document. Supported types are 'fiduciary' and 'consolidated'.
        :return: str, the address of the client.
        :raises ValueError: if the document type is not supported or not specified.
        """
        supported_types = {
        'fiduciary': self.get_address_fiduciary,
        'consolidated': self.get_address_consolidated
        }

        if kind not in supported_types:
            raise ValueError(f'The type ({kind}) of the document {file} is not supported or not specified.')

        address_function = supported_types[kind]
        address = address_function(file)
        
        return address
    
    def get_address_fiduciary(self, file):
        """
        Locate the address in a fiduciary document.

        :param file: str, the path to the PDF file to be processed.
        :return: str, the address of the client.
        """
        pdf = PdfReader(file)
        page_number = 0  # In fiduciary documents, the address is always on the first page.
        text = pdf.pages[page_number].extract_text() 
        lines = text.split('\n')
        address = lines[-1]  # The address is on the last line parsed.
        return address
    
    def get_address_consolidated(self, file):
        """
        Locate the address in a consolidated document.

        :param file: str, the path to the PDF file to be processed.
        :return: str, the address of the client.
        """
        pdf = PdfReader(file)
        page_number = 0  # In consolidated documents, the address is always on the first page.
        text = pdf.pages[page_number].extract_text()
        lines = text.split('\n')
        address = lines[-1]  # The address is on the last line parsed.
        return address


if __name__ == '__main__':
    # Test for extract addresses from multiple documents with associated types.
    print("Test for extract addresses from multiple documents with associated types.\n")

    documents = {
        "Doc 1.pdf": "consolidated",
        "Doc 2.pdf": "fiduciary"
    }
    
    extractor = AddressExtractor(documents)
    addresses = extractor.locate_addresses()
    
    for file, address in addresses.items():
        print(f"Document: {file}")
        print(f"Address: {address}")
        print("\n")



    # Test for extract address from a single document.
    print("Test for extract address from a single document.\n")

    file = "Doc 1.pdf"
    kind = "consolidated"
    extractor = AddressExtractor({file: kind})
    address = extractor.locate_address(file, kind)
    print(f"Document: {file}")
    print(f"Address: {address}")
    print("\n")



    # Test for extract address from a single document with an unsupported type.
    print("Test for extract address from a single document with an unsupported type.\n")

    file = "Doc 1.pdf"
    kind = "savings account"
    extractor = AddressExtractor({file: kind})
    address = extractor.locate_address(file, kind)
    print(f"Document: {file}")
    print(f"Address: {address}")
    print("\n")

