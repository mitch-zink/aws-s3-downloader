import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import os


def main():
    st.set_page_config(
        page_title="S3 Bucket Downloader",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("📦 S3 Bucket Downloader")

    with st.sidebar:
        st.header("Configuration ⚙️")
        aws_access_key_id = st.text_input(
            "AWS Access Key ID 🔑",
            placeholder="AKIAIOSFODNN7EXAMPLE",
            type="password",
        )
        aws_secret_access_key = st.text_input(
            "AWS Secret Access Key 🔒",
            type="password",
            placeholder="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        )
        aws_region = st.text_input("AWS Region 🌍", placeholder="us-west-2")
        bucket_name = st.text_input("Bucket Name 🪣", placeholder="my-s3-bucket")
        s3_path_prefix = st.text_input(
            "S3 Path Prefix (Optional) 📁", placeholder="path/to/folder/"
        )
        local_directory = st.text_input(
            "Local Directory Path 📂", placeholder="C:/Users/username/Downloads"
        )

        download_files = st.button("Download All Files 📥")

    s3_client = None
    if aws_access_key_id and aws_secret_access_key and aws_region:
        try:
            s3_client = boto3.client(
                "s3",
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
        except (NoCredentialsError, PartialCredentialsError) as e:
            st.error(f"Error with AWS credentials: {str(e)}")
            return

    if s3_client and bucket_name and local_directory and download_files:
        try:
            if not os.path.exists(local_directory):
                os.makedirs(local_directory)

            paginator = s3_client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_path_prefix)

            for page in pages:
                if "Contents" in page:
                    for file in page["Contents"]:
                        file_key = file["Key"]
                        if not file_key.endswith(
                            "/"
                        ):  # Checking that it's not a directory
                            local_file_path = os.path.join(
                                local_directory, os.path.basename(file_key)
                            )
                            s3_client.download_file(
                                bucket_name, file_key, local_file_path
                            )
            st.success(f"Downloaded all files to {local_directory}")
        except Exception as e:
            st.error(f"Failed to download files: {str(e)}")


if __name__ == "__main__":
    main()
