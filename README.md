# AWS S3 Helper

[![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![AWS S3](https://img.shields.io/badge/-AWS_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)](https://aws.amazon.com/s3/)

## Overview

A powerful and user-friendly Streamlit application for managing AWS S3 buckets. This tool provides a clean interface for listing, downloading, and uploading files to S3 buckets with support for IAM role assumption.

## Features

- 📜 **List Files** - Browse and view files in your S3 buckets
- 📥 **Download Files** - Download all files from a bucket or specific path prefix
- 📤 **Upload Files** - Upload multiple files to S3 with custom path prefixes
- 🛡️ **IAM Role Support** - Assume IAM roles for enhanced security
- 📁 **Path Prefix Support** - Work with specific folders within buckets
- 🔄 **Progress Tracking** - Real-time progress updates for uploads and downloads

## Setup Instructions

### Prerequisites

- Python 3.7+
- AWS credentials with appropriate S3 permissions

### For Mac/Linux

1. **Creating a Virtual Environment, Installing Dependencies, and Running the App**

   ```bash
   python3 -m venv .venv && source .venv/bin/activate && pip3 install --upgrade pip && pip3 install -r requirements.txt && streamlit run app.py
   ```

### For Windows

1. **Allow Script Execution (if necessary)**

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```

2. **Creating a Virtual Environment and Installing Dependencies**

   ```powershell
   py -m venv venv; .\venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt
   ```

3. **Running the Streamlit App**

   ```powershell
   streamlit run app.py
   ```

## Usage

1. **Configure AWS Credentials**

   - Enter your AWS Access Key ID and Secret Access Key
   - Specify the AWS Region (e.g., us-east-1)
   - (Optional) Provide an IAM Role ARN to assume

2. **Specify S3 Bucket**

   - Enter the bucket name you want to work with
   - (Optional) Add a path prefix to work with specific folders

3. **Choose an Operation**
   - **Upload Tab**: Select files and upload them to S3
   - **Download Tab**: Download all files from the specified bucket/prefix
   - **List Files Tab**: View all files in the bucket/prefix

## Security Notes

- Never commit AWS credentials to version control
- Consider using IAM roles for production environments
- Use the principle of least privilege when configuring AWS permissions

## Requirements

See `requirements.txt` for the full list of dependencies. Main requirements:

- streamlit
- boto3
- botocore

## License

This project is open source and available under the MIT License.
