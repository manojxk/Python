import requests
import json
import yaml

# Define common headers
headers = {
    "Content-Type": "application/json"
}

# Define your Bitbucket username and password
username = "Your_Bitbucket_Username"
password = "Your_Bitbucket_Password"

# Function to make an authorized HTTP GET request with username and password
def make_authorized_http_request(url):
    try:
        response = requests.get(url, headers=headers, auth=(username, password))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"HTTP Request error: {e}")
        return None

# Function to authenticate with Bitbucket API
def authenticate():
    base_url = "https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/projects/CONSUMERAPI"
    try:
        response = make_authorized_http_request(base_url)
        if response is not None:
            print(response)
    except Exception as e:
        print(f"Authentication error: {e}")

# Function to get inbound URI mappings
def get_inbound_uris(region, service_name):
    print("INBOUND REQUEST")
    bb_url = (
        f"https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/projects/CONSUMERAPI/{region}/{service_name}-config/browse/"
        f"{service_name}-config/UAT2/{service_name.replace('-', '')}/{service_name.replace('-', '')}.yml"
    )

    uri_mapping_list = []

    try:
        response_text = make_authorized_http_request(bb_url)
        if response_text:
            component_config = yaml.safe_load(response_text)

            # You can parse the YAML data and populate uri_mapping_list here

    except Exception as e:
        print(f"Error from BB :: {bb_url}")
        # Handle the error and populate uri_mapping_list accordingly

    return uri_mapping_list

# Function to get outbound APIs
def get_outbound_apis(region, service_name, domain):
    print("OUTBOUND REQUEST")
    bb_url = (
        f"https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/projects/CONSUMERAPI/{region}/{service_name}/browse/"
        f"{service_name}/src/main/resources/application.yml"
    )

    out_bound_list = []

    try:
        response_text = make_authorized_http_request(bb_url)
        if response_text:
            component_config = yaml.safe_load(response_text)

            # You can parse the YAML data and populate out_bound_list here

    except Exception as e:
        print(f"Error from BB :: {bb_url}")
        # Handle the error and populate out_bound_list accordingly

    return out_bound_list

# Function to get Jenkins configuration
def get_jenkins_config(region, service_name):
    print("JENKINS REQUEST")
    bb_url = f"https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/projects/CONSUMERAPI/{region}/{service_name}/browse/"
    jenkins_url = {}

    try:
        response_text = make_authorized_http_request(bb_url)
        if response_text:
            # Process the response_text and populate jenkins_url dictionary

    except Exception as e:
        print(f"ERROR IN JENKIN URL :: {service_name}")
        # Handle the error and populate jenkins_url accordingly

    return jenkins_url

# Function to get active profiles
def get_active_profiles(region, service_name):
    bb_url = (
        f"https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/projects/CONSUMERAPI/{region}/{service_name}/browse/"
        f"{service_name}/src/main/resources/bootstrap.yml"
    )

    active_profiles = service_name
    try:
        response_text = make_authorized_http_request(bb_url)
        if response_text:
            component_config = yaml.safe_load(response_text)
            active_profiles = f"{service_name},{component_config.get('spring', {}).get('profiles', {}).get('active', 'NA')}"
    except Exception as e:
        print(f"Error from BB :: {bb_url}")
        # Handle the error and set active_profiles accordingly

    return active_profiles

# Example usage:
if __name__ == "__main__":
    authenticate()
    inbound_uris = get_inbound_uris("example_region", "example_service")
    print("Inbound URIs:", inbound_uris)
    outbound_apis = get_outbound_apis("example_region", "example_service", "example_domain")
    print("Outbound APIs:", outbound_apis)
    jenkins_config = get_jenkins_config("example_region", "example_service")
    print("Jenkins Config:", jenkins_config)
    active_profiles = get_active_profiles("example_region", "example_service")
    print("Active Profiles:", active_profiles)
