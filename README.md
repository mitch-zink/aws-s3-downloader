# S3 Uploader
 
[![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

## Overview

Easily upload to S3 with a nice streamlit UI 

## Setup Instructions

### For Mac/Linux

1. **Creating a Virtual Environment, Installing Dependencies, and Running the App**

    ```bash
    python3 -m venv venv && source venv/bin/activate && pip3 install --upgrade pip && pip3 install -r requirements.txt &&  streamlit run app.py
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