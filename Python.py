import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Function to get the Jenkins URL based on microservice name
def get_jenkins_url(microservice_name):
    parts = microservice_name.split("-")
    prefix = parts[0]
    rest = parts[1:]
    jenkins_url = f"{prefix}.api.v2.{'.'.join(rest)}.gc.iut.int"
    return jenkins_url

# Function to get the latest Jenkins build information
def get_latest_jenkins_build(url, username, password):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get('lastSuccessfulBuild')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to process the Excel file and get latest builds
def process_excel(input_filename, output_filename, jenkins_username, jenkins_password):
    try:
        # Read the Excel file
        df = pd.read_excel(input_filename)

        # Ensure that the "Microservice Name" column exists in the Excel file
        if "Microservice Name" not in df.columns:
            raise ValueError("Column 'Microservice Name' not found in the Excel file.")

        # Create an empty list to store build data
        build_data = []

        # Iterate through the microservice names in the Excel file
        for microservice_name in df["Microservice Name"]:
            jenkins_url = get_jenkins_url(microservice_name)
            latest_build_info = get_latest_jenkins_build(jenkins_url, jenkins_username, jenkins_password)

            if latest_build_info:
                build_data.append({
                    "Microservice Name": microservice_name,
                    "Build Number": latest_build_info['number'],
                    "Build URL": latest_build_info['url']
                })

        # Create a DataFrame from the build data and save it to Excel
        if build_data:
            build_df = pd.DataFrame(build_data)
            build_df.to_excel(output_filename, index=False)
            print(f"Build information saved to {output_filename}")
        else:
            print("No valid build information found.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_filename = "microservices.xlsx"  # Replace with your Excel file path
output_filename = "latest_builds.xlsx"
jenkins_username = "ms59214"
jenkins_password = "Sunita@9791"

process_excel(input_filename, output_filename, jenkins_username, jenkins_password)
