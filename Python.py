import requests
import logging

def get_pull_requests_with_conflicts():
    # Replace with your Bitbucket credentials and repository information
    username = 'ms59214'
    password = 'Sunita@9791'

    # Authenticate with Bitbucket API
    auth = (username, password)
    headers = {"X-Atlassian-Token": "no-check"}
    logging.basicConfig(filename='pull_requests_with_conflicts.log',
                        level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Define the URL for getting pull requests
    url = f'https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/dashboard/pull-requests?state=OPEN'
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(
            f"Failed to retrieve pull requests: {str(e)}", exc_info=True)
        return
    if response.status_code == 200:
        pull_requests = response.json().get('values', [])
        # Filter pull requests with conflicts
        for pr in pull_requests:
            properties = pr.get("properties", {})
            merge = properties.get("mergeResult", {})
            conflict = merge.get("outcome")
            repo = pr["fromRef"]["repository"]["slug"]
            if conflict == "CONFLICTED":
                logging.info(f"{repo}")
                pr_id = pr.get('id', 'Unknown')
                project = "CONSUMERAPI"
                repo_name = pr["fromRef"]["repository"].get("slug", 'Unknown')
                version = pr.get("version", 'Unknown')
                body = {
                    "version": version
                }
                close_url = f'https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/projects/{project}/repos/{repo_name}/pull-requests/{pr_id}?version={version}'
                try:
                    response = requests.delete(
                        close_url, auth=auth, headers=headers, json=body)
                    response.raise_for_status()  # Raise an exception for non-204 responses
                except requests.exceptions.RequestException as e:
                    logging.error(
                        f"Failed to close pull request #{pr_id}: {str(e)}", exc_info=True)
                    continue  # Continue to the next pull request

                if response.status_code == 204:
                    logging.info(
                        f"Deleted")
                else:
                    msg = response.json().get("errors", {}).get("message", "Unknown error")
                    logging.error(
                        f"Failed to close pull request #{pr_id}: {response.status_code} - {msg}", exc_info=True)
    else:
        logging.error(
            f"Failed to retrieve pull requests: {response.status_code}", exc_info=True)

    # Close the log file
    logging.shutdown()
