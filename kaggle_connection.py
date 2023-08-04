from streamlit.connections import ExperimentalBaseConnection
import os
import pandas as pd
import zipfile
import streamlit as st


class KaggleDatasetConnection(ExperimentalBaseConnection):

    def _connect(self):
        # Set Kaggle credentials
        os.environ['KAGGLE_USERNAME'] = self._secrets.KAGGLE_USERNAME
        os.environ['KAGGLE_KEY'] = self._secrets.KAGGLE_KEY

        # importing here because it requires the credentials to be set
        from kaggle.api.kaggle_api_extended import KaggleApi

        # Initialize Kaggle API connection
        self.conn = KaggleApi()

    def get(self, path, filename, ttl):
        @st.cache_data(ttl=ttl)
        def _get(path=path):
            # Authenticate to Kaggle
            self.conn.authenticate()
            # Download zip file
            self.conn.dataset_download_files(path)
            # get filename from path
            file_name = path.split('/')[-1] + ".zip"
            # Dataset is downloaded as a zip, so we need to extract it
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall('.')
            # Read csv file to df
            df = pd.read_csv(filename)
            return df
        return _get(path)

    def get(self, dataset_reference, ttl):
        @st.cache_data(ttl=ttl)
        def _get(dataset_reference):
            # Authenticate to Kaggle
            self.conn.authenticate()

            # Download dataset files
            self.conn.dataset_download_files(dataset_reference)

            # Get filename from dataset reference
            file_name = dataset_reference.split('/')[-1] + ".zip"

            # Dataset is downloaded as a zip, so we need to extract it
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall('.')

            # Find the CSV file in the extracted contents
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            if len(csv_files) == 0:
                raise ValueError("No CSV file found in the dataset.")
            else :
                latest_csv_file_path = max(csv_files, key=os.path.getmtime)
                latest_csv_file_name = os.path.basename(latest_csv_file_path)

            # Read the CSV file to a DataFrame
            df = pd.read_csv(latest_csv_file_name)

            return df

        return _get(dataset_reference)

