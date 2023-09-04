import requests
import pandas as pd
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

# Function to fetch and save the latest builds to Excel
def get_latest_builds_to_excel(region, component_names, output_filename, username, password):
    jenkins_base_url = f"https://ebjenkins02.nam.nsroot.net/job/{region}/job/169068/job/consumer_api_uat/job"

    build_data = []
    for component_name in component_names:
        component_url = f"{jenkins_base_url}/{component_name}/api/json"
        latest_build_info = get_latest_jenkins_build(component_url, username, password)

        if latest_build_info:
            build_data.append({
                "Component": component_name,
                "Build Number": latest_build_info['number'],
                "Build URL": latest_build_info['url']
            })

    if build_data:
        df = pd.DataFrame(build_data)
        df.to_excel(output_filename, index=False)
        print(f"Build information saved to {output_filename}")
    else:
        print("No valid build information found.")

# Example usage
jenkins_username = "ms59214"
jenkins_password = "Sunita@9791"
region = "APAC"
component_names = [get_jenkins_url("169068-aim-d-publicrefdatamgt-ob-ea")]
output_filename = "latest_builds.xlsx"

get_latest_builds_to_excel(region, component_names, output_filename, jenkins_username, jenkins_password)
