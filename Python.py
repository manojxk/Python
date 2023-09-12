import requests
import logging

def create_pull_request(username, password, project, repo_name, base_branch, compare_branch, reviewers):
    # Configure logging
    logging.basicConfig(filename='pull_request_creation.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Authenticate with Bitbucket API
    auth = (username, password)
    headers = {"Content-Type": "application/json"}

    # Define the URL for creating a pull request
    url = f'https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/projects/{project}/repos/{repo_name}/pull-requests'

    # Get the latest commit hashes for the base and compare branches
    base_branch_url = f'https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/projects/{project}/repos/{repo_name}/commits?until={base_branch}'
    compare_branch_url = f'https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/projects/{project}/repos/{repo_name}/commits?until={compare_branch}'

    try:
        base_response = requests.get(base_branch_url, auth=auth)
        compare_response = requests.get(compare_branch_url, auth=auth)

        base_response.raise_for_status()
        compare_response.raise_for_status()

        base_commit_hash = base_response.json()[0]['id']
        compare_commit_hash = compare_response.json()[0]['id']

        if base_commit_hash == compare_commit_hash:
            logging.info("No changes between branches. No pull request created.")
            return

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve commit hashes: {str(e)}", exc_info=True)
        return

    # Create the pull request payload
    pull_request_payload = {
        "title": "My Title",
        "description": "My Description",
        "destination": {
            "branch": {
                "name": base_branch
            }
        },
        "source": {
            "branch": {
                "name": compare_branch
            }
        },
        "reviewers": reviewers  # Add the list of reviewers here
    }

    # Send the POST request to create the pull request
    try:
        response = requests.post(url, json=pull_request_payload, auth=auth, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create pull request: {str(e)}", exc_info=True)
        return

    if response.status_code == 201:
        logging.info("Pull request created successfully.")
    else:
        logging.error(f"Failed to create pull request: {response.status_code} - {response.text}", exc_info=True)

    # Close the log file
    logging.shutdown()

# Example usage:
username = 'your_username'
password = 'your_password'
project = 'your_project'
repo_name = 'your_repository'
base_branch = 'staging'
compare_branch = 'my-feature-branch'
reviewers = ["reviewer1", "reviewer2"]  # Add the list of reviewers here

create_pull_request(username, password, project, repo_name, base_branch, compare_branch, reviewers)
