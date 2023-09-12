import requests
import logging

# Configure logging
logging.basicConfig(filename='pull_request_closure.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

                    # Replace with your Bitbucket credentials and repository information
                    username = 'your_username'
                    password = 'your_password'
                    repo_slug = 'your_repository_slug'

                    # Authenticate with Bitbucket API
                    auth = (username, password)

                    # Get a list of your open pull requests
                    url = f'https://api.bitbucket.org/2.0/repositories/{username}/{repo_slug}/pullrequests'
                    try:
                        response = requests.get(url, auth=auth)
                            response.raise_for_status()  # Raise an exception for non-200 responses
                            except requests.exceptions.RequestException as e:
                                logging.error(f"Failed to retrieve pull requests: {str(e)}")
                                    exit(1)

                                    if response.status_code == 200:
                                        pull_requests = response.json()['values']

                                            # Iterate through pull requests and close or reject them
                                                for pr in pull_requests:
                                                        pr_id = pr['id']
                                                                close_url = f'https://api.bitbucket.org/2.0/repositories/{username}/{repo_slug}/pullrequests/{pr_id}'
                                                                        try:
                                                                                    response = requests.delete(close_url, auth=auth)
                                                                                                response.raise_for_status()  # Raise an exception for non-204 responses
                                                                                                        except requests.exceptions.RequestException as e:
                                                                                                                    logging.error(f"Failed to close pull request #{pr_id}: {str(e)}")
                                                                                                                                continue  # Continue to the next pull request

                                                                                                                                        if response.status_code == 204:
                                                                                                                                                    logging.info(f"Closed pull request #{pr_id}")
                                                                                                                                                            else:
                                                                                                                                                                        logging.error(f"Failed to close pull request #{pr_id}: {response.status_code}")
                                                                                                                                                                        else:
                                                                                                                                                                            logging.error(f"Failed to retrieve pull requests: {response.status_code}")

                                                                                                                                                                            # Close the log file
                                                                                                                                                                            logging.shutdown()
                                                                                                                                                                            )