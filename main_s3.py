from aws_s3_functions import Functions_S3

local_file = "DATA/BASE_COM_CEP.xlsx"
bucket_name = "analyticsitaughp00569"
object_key = "data/uploaded/footprint.xlsx"

s3_filepath = "s3://analyticsitaughp00569/data/uploaded/footprint.xlsx"
s3_file_prefix = "s3://analyticsitaughp00569/data/uploaded/"


# UPLOAD A FILE
"""
Functions_S3.upload_file_to_s3(local_file=local_file,
                               bucket_name=bucket_name,
                               object_key=object_key)
"""

# READ A FILE
result_read_s3_file = Functions_S3.read_s3_file(filepath=s3_filepath)