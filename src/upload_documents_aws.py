import boto3

class DocumentProcessor:
    """
    A class used to upload and download documents from AWS S3
    
    """
    def __init__(self, aws_access_key, aws_secret_key, bucket_name):
        """
        Parameters
        ----------
        aws_access_key : str
            AWS access key ID
        aws_secret_key : str
            AWS secret access key
        bucket_name : str
            AWS S3 bucket name
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

    def upload_documents_to_s3(self, file_paths):
        """
        Upload documents to AWS S3

        Parameters
        ----------
        file_paths : list
            List of file paths to upload to S3
        """

        for file_path in file_paths:
            object_name = file_path.split("/")[-1]
            if object_name.lower().endswith(".pdf"):
                self.s3_client.upload_file(file_path, self.bucket_name, object_name)
                print(
                    f"File '{file_path}' uploaded successfully to S3."
                )
            else:
                print(
                    f"The file '{file_path}' is not a PDF file and will not be uploaded to S3."
                )

    def download_documents_from_s3(self):
        """
        Download documents from AWS S3
        """

        response = self.s3_client.list_objects(Bucket=self.bucket_name)
        objects = response.get("Contents", [])

        for obj in objects:
            object_name = obj["Key"]
            if object_name.lower().endswith(".pdf"):
                file_path = "../data/"+object_name

                self.s3_client.download_file(
                    self.bucket_name, object_name, file_path
                )

                print(f"File '{object_name}' downloaded successfully from S3.")

                
                

if __name__ == "__main__":
    # AWS credentials
    with open("../api/keys.txt", "r") as f:
        # Read the file
        input_string = f.read()

        # Close the file
        f.close()

    aws_access_key = re.search(r'aws_access_key = "(.*)"', input_string).group(1)
    aws_secret_key = re.search(r'aws_secret_key = "(.*)"', input_string).group(1)
    bucket_name = re.search(r'bucket_name = "(.*)"', input_string).group(1)
    
    # Create a DocumentProcessor object
    document_processor = DocumentProcessor(
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
        bucket_name=bucket_name,
    )

    # Upload documents to S3
    file_paths = ["CONS Test File.pdf", "FIDU Test File.pdf"]
    document_processor.upload_documents_to_s3(file_paths)

    # Download documents from S3
    document_processor.download_documents_from_s3()

