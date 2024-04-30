import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import os

def main():
    st.set_page_config(
        page_title="S3 Bucket Uploader",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("📦 S3 Bucket Uploader")

    with st.sidebar:
        st.header("Configuration ⚙️")
        aws_access_key_id = st.text_input("AWS Access Key ID 🔑", placeholder="AKIAIOSFODNN7EXAMPLE")
        aws_secret_access_key = st.text_input("AWS Secret Access Key 🔒", type="password", placeholder="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
        aws_region = st.text_input("AWS Region 🌍", placeholder="us-west-2")
        bucket_name = st.text_input("Bucket Name 🪣", placeholder="my-s3-bucket")
        s3_path_prefix = st.text_input("S3 Path Prefix (Optional) 📁", placeholder="path/to/folder/")

        file_uploader = st.file_uploader("Choose a file to upload 📤", accept_multiple_files=True)
        upload_files = st.button("Upload Files 📤")

    s3_client = None
    if aws_access_key_id and aws_secret_access_key and aws_region:
        try:
            s3_client = boto3.client(
                's3',
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
        except (NoCredentialsError, PartialCredentialsError) as e:
            st.error(f"Error with AWS credentials: {str(e)}")
            return

    if s3_client and bucket_name and file_uploader and upload_files:
        try:
            successful_uploads = 0
            for uploaded_file in file_uploader:
                file_path = os.path.join(s3_path_prefix, uploaded_file.name)
                s3_client.upload_fileobj(uploaded_file, bucket_name, file_path)
                successful_uploads += 1

            if successful_uploads > 0:
                st.success(f"Successfully uploaded {successful_uploads} files to bucket '{bucket_name}'.")
            else:
                st.warning("No files were uploaded.")
        except Exception as e:
            st.error(f"Failed to upload files: {str(e)}")

if __name__ == "__main__":
    main()
