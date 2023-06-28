import re

with open("../api/keys.txt", "r") as f:
        # Read the file
        input_string = f.read()

aws_access_key = re.search(r'aws_access_key = "(.*)"', input_string).group(1)
aws_secret_key = re.search(r'aws_secret_key = "(.*)"', input_string).group(1)
bucket_name = re.search(r'bucket_name = "(.*)"', input_string).group(1)
gmaps_key = re.search(r'gmaps = "(.*)"', input_string).group(1)

print(aws_access_key)