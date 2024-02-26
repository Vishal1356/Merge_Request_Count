import requests
import pandas as pd


# Function to fetch user ID from username
def get_user_id(username, private_token):
    headers = {"Private-Token": private_token}
    response = requests.get(f"https://git.automate.com/api/v4/users?username={username}", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        if user_data:
            return user_data[0]["id"]
        else:
            print(f"No user found with username: {username}")
            return None
    else:
        print(f"Error fetching user data: {response.text}")
        return None


# Function to fetch merge requests for a user from the GitLab API
def fetch_merge_requests(username, private_token):
    author_id = get_user_id(username, private_token)
    if author_id is not None:
        api_url = f"https://git.automate.com/api/v4/projects/testing%2Fam-ui-automation/merge_requests?scope=all&state=merged&author_id={author_id}"
        headers = {"Private-Token": private_token}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            merge_requests_data = response.json()
            return merge_requests_data
        else:
            print(f"Error fetching merge requests data: {response.text}")
            return None
    else:
        return None


# Function to fetch merge request changes data from GitLab API
def fetch_merge_request_changes(merge_request_iid, private_token):
    headers = {"PRIVATE-TOKEN": private_token}
    url = f"https://git.automate.com/api/v4/projects/testing%2Fam-ui-automation/merge_requests/{merge_request_iid}/changes"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching merge request changes: {response.text}")
        return None


# Main function to retrieve and save data
def main(username):
    private_token = "fzsqL4ppitPYBEUcF6sH"  # Replace with your Private-Token

    # Fetch merge requests for the specified username
    merge_requests_data = fetch_merge_requests(username, private_token)
    if merge_requests_data:
        # Create DataFrame with merge requests data
        df_merge_requests = pd.DataFrame({"ID": [mr["id"] for mr in merge_requests_data],
                                          "UserName": [mr["author"]["username"] for mr in merge_requests_data],
                                          "IId": [mr["iid"] for mr in merge_requests_data]})

        # Add count of merge requests column
        merge_requests_count = len(df_merge_requests)
        df_merge_requests["MergeRequestCount"] = merge_requests_count

        # Create an empty DataFrame to store merge request changes data
        df_changes = pd.DataFrame(columns=["IId", "LinesAdded", "LinesRemoved"])

        # Fetch and process merge request changes data for each merge request
        for merge_request_iid in df_merge_requests["IId"]:
            changes_data = fetch_merge_request_changes(merge_request_iid, private_token)
            if changes_data:
                # Combine all changes data into one variable
                all_changes = ""
                for change in changes_data["changes"]:
                    all_changes += change["diff"]

                # Calculate the number of lines added (n+) and removed (n-)
                lines_added_count = all_changes.count("\n+")
                lines_removed_count = all_changes.count("\n-")

                # Append data to df_changes
                df_changes = pd.concat([df_changes, pd.DataFrame({"IId": [merge_request_iid],
                                                                   "LinesAdded": [lines_added_count],
                                                                   "LinesRemoved": [lines_removed_count]})])

        # Merge df_merge_requests with df_changes on IId
        df_result = pd.merge(df_merge_requests, df_changes, on="IId", how="outer")

        # Save data to Excel
        file_name = "gitlab_merge_requests.xlsx"
        df_result.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")

    else:
        print(f"No merge requests found for user: {username}")


# Execute main function with input username
if __name__ == "__main__":
    username_input = input("Enter the username: ")
    main(username_input)
