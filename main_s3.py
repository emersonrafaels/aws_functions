from functions_s3.aws_functions_s3 import Functions_S3

local_file = "data_examples/despachantes.csv"
bucket_name = "analyticsitaughp00569"
object_key = "data/uploaded/despachantes.csv"

s3_filepath = "s3://analyticsitaughp00569/data/uploaded/despachantes.csv"
s3_file_prefix = "s3://analyticsitaughp00569/data/uploaded/"

# DELETE FILE
Functions_S3.delete_objects_s3(filepath=s3_filepath)

# UPLOAD A FILE
Functions_S3.upload_file_to_s3(local_file=local_file,
                               bucket_name=bucket_name,
                               object_key=object_key)

# READ A FILE
result_read_s3_file = Functions_S3.read_s3_file(filepath=s3_filepath)