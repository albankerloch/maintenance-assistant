from google.cloud import storage
import streamlit as st
from io import StringIO
import os


def upload_blob(bucket_name, destination_blob_name, file):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"
    # The file to upload
    # file = file-object

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_file(file)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")
    st.write("File:  ", destination_blob_name, "  uploaded.")


#####


st.title('Upload Files to Google Cloud Storage using Streamlit')

bucket_name = "bucket-test-chatbot-edf"
print(bucket_name)

uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    print(uploaded_file.name)
    upload_blob(bucket_name, uploaded_file.name, uploaded_file)