import requests
import logging

def close_open_pull_requests():
    # Configure logging
    logging.basicConfig(filename='pull_request_closure.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Replace with your Bitbucket credentials and repository information
    username = 'ss21454'
    password = 'HanaHamdan@786'

    # Authenticate with Bitbucket API
    auth = (username, password)
    headers = {"X-Atlassian-Token": "no-check"}

    # Get a list of your open pull requests
    url = 'https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/dashboard/pull-requests?state=OPEN'
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Raise an exception for non-200 responses
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve pull requests: {str(e)}", exc_info=True)
        exit(1)

    if response.status_code == 200:
        pull_requests = response.json().get('values', [])

        # Iterate through pull requests and close or reject them
        for pr in pull_requests:
            pr_id = pr['id']
            project = "CONSUMERAPI"
            repo_name = pr["fromRef"]["repository"]["slug"]
            version = pr["version"]
            close_url = f'https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/projects/{project}/repos/{repo_name}/pull-requests/{pr_id}/decline?version={version}&pullRequestId={pr_id}'
            try:
                response = requests.post(close_url, auth=auth, headers=headers)
                response.raise_for_status()  # Raise an exception for non-204 responses
            except requests.exceptions.RequestException as e:
                logging.error(
                    f"Failed to close pull request #{pr_id}: {str(e)}", exc_info=True)
                continue  # Continue to the next pull request

            if response.status_code == 200:
                logging.info(
                    f"Closed pull request #{pr_id}")
            else:
                msg = response.json().get("errors", {}).get("message", "Unknown error")
                logging.error(
                    f"Failed to close pull request #{pr_id}: {response.status_code} - {msg}", exc_info=True)
    else:
        logging.error(
            f"Failed to retrieve pull requests: {response.status_code}", exc_info=True)

    # Close the log file
    logging.shutdown()

# Call the function to execute the code
close_open_pull_requests()
