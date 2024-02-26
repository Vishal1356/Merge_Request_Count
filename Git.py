import requests
import pandas as pd

access_token = 'fzsqL4ppitPYBEUcF6sH'
# Function to fetch pull requests from GitLab API
def fetch_pull_requests(project_id, token):
    url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests"
    headers = {"PRIVATE-TOKEN": access_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching pull requests: {response.text}")
        return None


# Function to extract relevant information from pull requests
def extract_info(pull_requests):
    data = []
    for pr in pull_requests:
        pr_id = pr['id']
        title = pr['title']
        lines_added = pr['additions']
        lines_removed = pr['deletions']
        data.append([pr_id, title, lines_added, lines_removed])
    return data


# Main function to retrieve and save data
def main():
    project_id = "your_project_id"
    gitlab_token = "your_gitlab_token"

    pull_requests = fetch_pull_requests(project_id, gitlab_token)
    if pull_requests:
        data = extract_info(pull_requests)
        df = pd.DataFrame(data, columns=['PR ID', 'Title', 'Lines Added', 'Lines Removed'])

        # Save to Excel
        file_name = "pull_requests_data.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")


if __name__ == "__main__":
    main()
