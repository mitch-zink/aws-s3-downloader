import os

import boto3
import streamlit as st
from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError


def main():
    st.set_page_config(
        page_title="S3 Bucket Downloader",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("📦 S3 Bucket File Lister & Downloader")

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
        role_arn = st.text_input(
            "Role ARN 🛡️ (Optional)",
            placeholder="arn:aws:iam::123456789012:role/RoleName",
        )
        bucket_name = st.text_input("Bucket Name 🪣", placeholder="my-s3-bucket")
        s3_path_prefix = st.text_input(
            "S3 Path Prefix (Optional) 📁", placeholder="path/to/folder/"
        )
        local_directory = st.text_input(
            "Local Directory Path 📂", placeholder="C:/Users/username/Downloads"
        )

        list_files_button = st.button("List Files 📜")
        download_files = st.button("Download All Files 📥")

    s3_client = None
    if aws_region:
        try:
            if role_arn:
                # Assume role
                if not aws_access_key_id or not aws_secret_access_key:
                    st.error(
                        "AWS Access Key ID and Secret Access Key are required to assume a role"
                    )
                    return

                sts_client = boto3.client(
                    "sts",
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=aws_region,
                )

                assumed_role = sts_client.assume_role(
                    RoleArn=role_arn, RoleSessionName="AssumeRoleSession"
                )

                credentials = assumed_role["Credentials"]

                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=credentials["AccessKeyId"],
                    aws_secret_access_key=credentials["SecretAccessKey"],
                    aws_session_token=credentials["SessionToken"],
                    region_name=aws_region,
                )

            elif aws_access_key_id and aws_secret_access_key:
                # Use provided credentials
                s3_client = boto3.client(
                    "s3",
                    region_name=aws_region,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                )
            else:
                # Use default credentials
                s3_client = boto3.client(
                    "s3",
                    region_name=aws_region,
                )
        except (NoCredentialsError, PartialCredentialsError) as e:
            st.error(f"Error with AWS credentials: {str(e)}")
            return
        except ClientError as e:
            st.error(f"Client error: {str(e)}")
            return
    else:
        st.error("Please provide the AWS Region")
        return

    if s3_client and bucket_name and list_files_button:
        try:
            paginator = s3_client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_path_prefix)

            file_list = []
            for page in pages:
                if "Contents" in page:
                    for file in page["Contents"]:
                        file_key = file["Key"]
                        if not file_key.endswith("/"):
                            file_list.append(file_key)

            if file_list:
                st.subheader("Files in Bucket")
                st.table({"Files": file_list})
            else:
                st.info("No files found in the specified bucket/path.")
        except ClientError as e:
            if e.response["Error"]["Code"] == "403":
                st.error("Access denied to the bucket or object")
            elif e.response["Error"]["Code"] == "404":
                st.error("The bucket does not exist")
            else:
                st.error(f"Failed to list files: {str(e)}")
        except Exception as e:
            st.error(f"Failed to list files: {str(e)}")

    if s3_client and bucket_name and local_directory and download_files:
        try:
            if not os.path.exists(local_directory):
                os.makedirs(local_directory)

            paginator = s3_client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_path_prefix)

            with st.spinner("Downloading files..."):
                for page in pages:
                    if "Contents" in page:
                        for file in page["Contents"]:
                            file_key = file["Key"]
                            if not file_key.endswith("/"):
                                relative_path = (
                                    file_key[len(s3_path_prefix) :]
                                    if s3_path_prefix
                                    else file_key
                                )
                                local_file_path = os.path.join(
                                    local_directory, relative_path
                                )
                                local_file_dir = os.path.dirname(local_file_path)
                                if not os.path.exists(local_file_dir):
                                    os.makedirs(local_file_dir)
                                s3_client.download_file(
                                    bucket_name, file_key, local_file_path
                                )
            st.success(f"Downloaded all files to {local_directory}")
        except ClientError as e:
            if e.response["Error"]["Code"] == "403":
                st.error("Access denied to the bucket or object")
            elif e.response["Error"]["Code"] == "404":
                st.error("The bucket or object does not exist")
            else:
                st.error(f"Failed to download files: {str(e)}")
        except Exception as e:
            st.error(f"Failed to download files: {str(e)}")


if __name__ == "__main__":
    main()
