# IMPORTING LIBRARIES
import os
from pathlib import Path
from inspect import stack

import awswrangler as wr
import boto3
import botocore
import pandas as pd

import execute_log

# INICIALIZANDO O LOGGER
execute_log.startLog()

dict_file_format = {
    ".xlsx": "excel",
    ".csv": "csv",
    ".json": "json",
    ".parquet": "parquet",
}


class Functions_S3:
    def __init__(self):
        pass

    @staticmethod
    def create_s3_bucket(bucket_name, region=None):
        """

        CREATE AN S3 BUCKET IN A SPECIFIED VERSION

        IF A REGION IS NOT SPECIFIED,
        THE BUCKET IS CREATED IN THE S3 DEFAULT
        REGION (us-east-1)

        # Arguments
            :param bucket_name: Bucket to create (String)
            :param region: String region to create
                           bucket in, e.g., 'us-west-2' (String)

        # Returns
            :return validator: True if bucket created,
                               else False (Boolean)

        """

        # INIT FUNCTION VALIDATOR
        validator = False

        try:
            if region is None:
                s3_client = boto3.client("s3")
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client("s3", region_name=region)
                location = {"LocationConstraint": region}
                s3_client.create_bucket(
                    Bucket=bucket_name, CreateBucketConfiguration=location
                )

            execute_log.info("BUCKET CREATED SUCCESSFULLY")
            execute_log.info("BUCKET NAME: {}".format(bucket_name))
            execute_log.info("-" * 50)

            validator = True

        except Exception as ex:
            execute_log.error(ex)

        return validator

    @staticmethod
    def list_s3_existing_buckets():
        """

        GET ALL BUCKETS IN ACCOUNT.

        # Returns
            :return list_buckets: List of buckets (List)
        """

        # INIT VARIABLE THAT TO STORE THE LIST OF BUCKETS
        list_buckets = []

        try:
            # CONNECTING TO S3
            s3 = boto3.client("s3")

            # GETTING LIST OF BUCKETS
            response = s3.list_buckets()
            list_buckets = [bucket for bucket in response["Buckets"]]

            execute_log.info("LIST - BUCKETS")

            for bucket in list_buckets:
                execute_log.info("BUCKET: {}".format(bucket["Name"]))

                execute_log.info("-" * 50)

        except Exception as ex:
            execute_log.error(ex)

        return list_buckets

    @staticmethod
    def list_s3_objects(bucket_name, prefix=None, specified_format=None):
        """

        GET ALL OBJECTS IN S3 BUCKET.

        # Arguments
            :param bucket_name: S3 Bucket name (String)
            :param prefix: Dir in bucket (String)
            :param specified_format: Desired data extension (List)

        # Returns
            :return list_objects: List of buckets (List)
        """

        # INIT VARIABLE THAT TO STORE THE OBJECTS IN BUCKET
        list_all_objects = list_specified_format_objects = []

        try:
            # CONNECTING TO S3
            s3 = boto3.client("s3")

            if prefix:
                # GETTING LIST OF BUCKETS WITH DEFINED PREFIX
                response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            else:
                # GETTING LIST OF BUCKETS WITHOUT DEFINED PREFIX
                response = s3.list_objects_v2(Bucket=bucket_name)

            list_all_objects = [content for content in response.get("Contents", [])]

            execute_log.info("LIST - OBJECT")
            execute_log.info("BUCKET: {}".format(bucket_name))

            # ITER OVER ALL OBJECTS
            for idx, object in enumerate(list_all_objects):
                # VERIFYING DESIRED FORMATS
                if specified_format:
                    execute_log.info("SPECIFIED FORMATS: {}".format(specified_format))
                    if object["Key"].endswith(tuple(specified_format)):
                        execute_log.info("OBJECT: {}".format(object["Key"]))
                        list_specified_format_objects.append(object)
                else:
                    execute_log.info("OBJECT: {}".format(object["Key"]))
                    list_specified_format_objects.append(object)

                    execute_log.info("-" * 50)

        except Exception as ex:
            execute_log.error(ex)

        return list_all_objects, list_specified_format_objects

    @staticmethod
    def upload_file_to_s3(local_file, bucket_name, object_key):
        """

        UPLOAD A LOCAL FILE TO S3 BUCKET.

        # Arguments
            :param local_file: Path where is the file (Path)
            :param bucket_name: Bucket to upload the file (String)
            :param object_key: Filename to save in S3.
                               Here it's possible to define the
                               subfolder + filename to save
                               in the bucket. (String)

        # Returns
            :return validator: True if file uploaded,
                               else False (Boolean)

        """

        # INIT FUNCTION VALIDATOR
        validator = False

        try:
            # CONNECTING TO S3
            s3_client = boto3.client("s3")

            # UPLOAD OBJECT
            execute_log.info("Uploading object ...")

            if os.path.exists(local_file):
                s3_client.upload_file(local_file, bucket_name, object_key)
                execute_log.info("Uploaded")

                validator = True

            else:
                execute_log.info("Local file not found")

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucket":
                execute_log.error("Error: Bucket does not exist!!")
            elif e.response["Error"]["Code"] == "InvalidBucketName":
                execute_log.error("Error: Invalid Bucket name!!")
            elif e.response["Error"]["Code"] == "AllAccessDisabled":
                execute_log.error("Error: You do not have access to the Bucket!!")
            else:
                raise

        return validator

    @staticmethod
    def delete_objects_s3(filepath):
        """

        DELETE OBJECTS IN S3 BUCKET.

        # Arguments
            :param filepath: Bucket + Filename to delete (String)

        # Returns
            :return validator: True if file uploaded,
                               else False (Boolean)

        """

        # INIT FUNCTION VALIDATOR
        validator = False

        try:
            execute_log.info("Deleting: {}".format(filepath))

            # DELETE OBJECT
            wr.s3.delete_objects(filepath)

            execute_log.info("Successfully deleted")

            validator = True

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucket":
                execute_log.error("Error: Bucket does not exist!!")
            elif e.response["Error"]["Code"] == "InvalidBucketName":
                execute_log.error("Error: Invalid Bucket name!!")
            elif e.response["Error"]["Code"] == "AllAccessDisabled":
                execute_log.error("Error: You do not have access to the Bucket!!")
            else:
                raise

        return validator

    @staticmethod
    def read_s3_file(filepath=None, file_format=None, prefix=None):
        """

        READ A FILE FROM S3 BUCKET.

        # Arguments
            :param filepath: Bucket + Filename to read (String)
            :param file_format: Format file to read (String)
            :param prefix: Subfolder to read files in the bucket (String)

        # Returns
            :return validator: True if file(s) readed,
                               else False (Boolean)

        """

        # INIT FUNCTION VALIDATOR
        validator = False

        # INIT RESULT DATAFRAME
        df = pd.DataFrame()

        try:
            # VERIFYING IF THE FILEPATH IS UNIQUE FILE OR MULTIPLE FILES
            if prefix:
                if file_format:
                    # THE METHOD ALL FILES IN A FOLDER
                    file_to_read = prefix

                    execute_log.info(
                        "Reading dataframe using Prefix Path: {} - Format: {}".format(
                            file_to_read, file_format
                        )
                    )

                else:
                    execute_log.error(
                        "To read a folder (using prefix) is necessary to specify a files format"
                    )
                    return False, df

            if isinstance(filepath, str):
                # GET THE EXTENSION
                if not file_format:
                    file_format = dict_file_format.get(Path(filepath).suffix)

                # THE METHOD WILL READ A UNIQUE FILE
                file_to_read = filepath

                execute_log.info(
                    "Reading dataframe using Path: {} - Format: {}".format(
                        file_to_read, file_format
                    )
                )

            if isinstance(file_to_read, (str, tuple, list)) and file_format:
                if file_format == "csv":
                    df = wr.s3.read_csv(file_to_read)

                elif file_format == "excel":
                    df = wr.s3.read_excel(file_to_read)

                elif file_format == "parquet":
                    df = wr.s3.read_parquet(file_to_read)

                elif file_format == "json":
                    df = wr.s3.read_json(file_to_read)

                if not df.empty:
                    validator = True

            else:
                execute_log.info("filepath must be a string or a (tuple, list)")

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucket":
                execute_log.error("Error: Bucket does not exist!!")
            elif e.response["Error"]["Code"] == "InvalidBucketName":
                execute_log.error("Error: Invalid Bucket name!!")
            elif e.response["Error"]["Code"] == "AllAccessDisabled":
                execute_log.error("Error: You do not have access to the Bucket!!")
            else:
                raise

        return validator, df
