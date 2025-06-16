import os

import boto3
import streamlit as st
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError


def create_s3_client(region, access_key, secret_key, role_arn=None):
    try:
        if role_arn:
            if not access_key or not secret_key:
                st.error("Access Key and Secret Key are required to assume a role")
                return None

            sts_client = boto3.client(
                "sts",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )

            assumed_role = sts_client.assume_role(
                RoleArn=role_arn, RoleSessionName="AssumeRoleSession"
            )

            creds = assumed_role["Credentials"]

            return boto3.client(
                "s3",
                aws_access_key_id=creds["AccessKeyId"],
                aws_secret_access_key=creds["SecretAccessKey"],
                aws_session_token=creds["SessionToken"],
                region_name=region,
            )

        elif access_key and secret_key:
            return boto3.client(
                "s3",
                region_name=region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        else:
            return boto3.client("s3", region_name=region)

    except (NoCredentialsError, PartialCredentialsError) as e:
        st.error(f"❌ Credential error: {e}")
    except ClientError as e:
        st.error(f"❌ Client error: {e}")
    return None


def list_files(s3_client, bucket, prefix):
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix or "")

        file_list = []
        for page in pages:
            for obj in page.get("Contents", []):
                if not obj["Key"].endswith("/"):
                    file_list.append(obj["Key"])

        return file_list
    except ClientError as e:
        st.error(f"❌ Failed to list files: {e}")
        return []


def download_files(s3_client, bucket, prefix, local_dir):
    try:
        local_dir = local_dir or "downloads"
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            st.write(f"📁 Created local directory: {local_dir}")

        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix or "")

        total_files = 0
        failed_files = 0
        with st.spinner("📥 Downloading files..."):
            for page in pages:
                for obj in page.get("Contents", []):
                    key = obj["Key"]
                    if not key.endswith("/"):
                        total_files += 1
                        relative_path = key[len(prefix) :] if prefix else key
                        local_path = os.path.join(local_dir, relative_path)
                        local_dirname = os.path.dirname(local_path)
                        if not os.path.exists(local_dirname):
                            os.makedirs(local_dirname)
                            st.write(f"📂 Created subdirectory: {local_dirname}")

                        st.write(f"⬇️ Downloading: {key} → {local_path}")
                        try:
                            s3_client.download_file(bucket, key, local_path)
                        except Exception as e:
                            failed_files += 1
                            st.warning(f"⚠️ Failed to download {key}: {e}")

        if total_files == 0:
            st.warning("⚠️ No files found to download.")
        else:
            st.success(
                f"✅ Downloaded {total_files - failed_files} files to {local_dir}"
            )
            if failed_files > 0:
                st.warning(f"⚠️ {failed_files} file(s) failed to download.")
    except Exception as e:
        st.error(f"❌ Unexpected failure during download: {e}")


def upload_files(s3_client, bucket, s3_path_prefix, uploaded_files):
    try:
        successful_uploads = 0
        for uploaded_file in uploaded_files:
            file_path = (
                os.path.join(s3_path_prefix, uploaded_file.name)
                if s3_path_prefix
                else uploaded_file.name
            )
            s3_client.upload_fileobj(uploaded_file, bucket, file_path)
            successful_uploads += 1
            st.write(f"⬆️ Uploaded: {uploaded_file.name} → {file_path}")

        if successful_uploads > 0:
            st.success(
                f"✅ Successfully uploaded {successful_uploads} files to bucket '{bucket}'."
            )
        else:
            st.warning("⚠️ No files were uploaded.")
    except Exception as e:
        st.error(f"❌ Failed to upload files: {str(e)}")


def main():
    st.set_page_config(
        page_title="S3 Bucket Manager",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("📦 S3 Bucket Manager - Upload & Download")

    with st.sidebar:
        st.header("Configuration ⚙️")
        access_key = st.text_input(
            "AWS Access Key ID 🔑", placeholder="AKIAIOSFODNN7EXAMPLE", type="password"
        )
        secret_key = st.text_input(
            "AWS Secret Access Key 🔒",
            placeholder="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            type="password",
        )
        region = st.text_input("AWS Region 🌍", placeholder="us-east-1")
        role_arn = st.text_input(
            "Role ARN 🛡️ (Optional)",
            placeholder="arn:aws:iam::123456789012:role/RoleName",
        )
        bucket = st.text_input("Bucket Name 🪣", placeholder="my-s3-bucket")
        prefix = st.text_input("S3 Path Prefix 📁", placeholder="path/to/folder/")

    if not region:
        st.error("❌ AWS Region is required")
        return

    s3_client = create_s3_client(region, access_key, secret_key, role_arn)
    if not s3_client:
        return

    tab1, tab2, tab3 = st.tabs(["📤 Upload", "📥 Download", "📜 List Files"])

    with tab1:
        st.header("Upload Files to S3")
        uploaded_files = st.file_uploader(
            "Choose files to upload", accept_multiple_files=True
        )
        if st.button("Upload Files 📤"):
            if uploaded_files and bucket:
                upload_files(s3_client, bucket, prefix, uploaded_files)
            else:
                st.warning("⚠️ Please select files and specify a bucket name.")

    with tab2:
        st.header("Download Files from S3")
        local_dir = st.text_input("Local Directory Path 📂", placeholder="./downloads")
        if st.button("Download All Files 📥"):
            if bucket:
                st.info("📥 Starting file download...")
                download_files(s3_client, bucket, prefix, local_dir)
            else:
                st.warning("⚠️ Please specify a bucket name.")

    with tab3:
        st.header("List Files in S3 Bucket")
        if st.button("List Files 📜"):
            if bucket:
                st.info("🔍 Fetching file list...")
                files = list_files(s3_client, bucket, prefix)
                if files:
                    st.subheader(f"Files in {bucket}/{prefix or ''}")
                    st.table({"Files": files})
                else:
                    st.info("No files found.")
            else:
                st.warning("⚠️ Please specify a bucket name.")


if __name__ == "__main__":
    main()
