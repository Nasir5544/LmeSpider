import boto3
from dotenv import load_dotenv
import time
import os

def uploadS3(download_directory):

    # Load environment variables from .env file
    load_dotenv()

    # AWS S3
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    bucket_name = os.getenv('AWS_BUCKET')

    # Wait for the download to complete (you can adjust the wait time as needed)
    max_wait_time = 60  # Maximum wait time in seconds
    interval = 1  # Check every 1 second
    elapsed_time = 0

    while elapsed_time < max_wait_time:
        # List files in the custom download directory
        downloaded_files = os.listdir(download_directory)

        # List files in the custom download directory, excluding both .crdownload and hidden files
        downloaded_files = [file for file in os.listdir(download_directory) if not (file.endswith(".crdownload") or file.startswith("."))]

        # Check if any files have been downloaded
        if downloaded_files:
            # Sort the files by modification time in descending order
            downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_directory, x)), reverse=True)
            
            time.sleep(3)
            downloaded_file_name = downloaded_files[0]
            break
        # else:
        #     downloaded_file_name = ''

        time.sleep(interval)
        elapsed_time += interval

    if elapsed_time >= max_wait_time:
        print("Download did not complete within the specified time.")
    else:
        print("Download completed!")


    # if(downloaded_file_name != ''):
    # Full path to the downloaded file
    downloaded_file_path = os.path.join(download_directory, downloaded_file_name)

    # Read the downloaded file's content
    with open(downloaded_file_path, "rb") as pdf_file:
        pdf_content = pdf_file.read()

        print('Uploading to S3 ...')
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)


        # Upload the file directly to S3 without saving it locally
        object_key = 'lme_files/' + downloaded_file_name
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=pdf_content,
            ContentType="application/pdf"
        )

        # set uploaded file to private
        #s3.put_object_acl(Bucket=bucket_name, Key=downloaded_file_name, ACL="private")
        
        print('Upload to S3 Done')
        os.remove(downloaded_file_path)
        
        return object_key