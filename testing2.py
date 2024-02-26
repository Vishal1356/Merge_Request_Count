import requests
import pandas as pd


# Function to fetch user IDs and usernames for all users with pagination
def get_all_user_data(private_token):
    headers = {"Private-Token": private_token}
    users_data = []
    page = 1
    while True:
        response = requests.get(f"https://git.automate.com/api/v4/users?page={page}", headers=headers)
        if response.status_code == 200:
            users_page_data = response.json()
            if users_page_data:
                users_data.extend(users_page_data)
                page += 1
            else:
                break
        else:
            print(f"Error fetching user data: {response.text}")
            return {}
    user_ids = [user["id"] for user in users_data]
    usernames = [user["username"] for user in users_data]
    return dict(zip(user_ids, usernames))


# Function to fetch merge requests for a user from the GitLab API
def fetch_merge_requests(user_id, private_token):
    api_url = f"https://git.automate.com/api/v4/projects/testing%2Fam-ui-automation/merge_requests?scope=all&state=merged&author_id={user_id}"
    headers = {"Private-Token": private_token}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching merge requests data for user {user_id}: {response.text}")
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
def main():
    private_token = "fzsqL4ppitPYBEUcF6sH"  # Replace with your Private-Token

    # Get user IDs and usernames for all users with pagination
    user_data = get_all_user_data(private_token)
    if not user_data:
        print("No users found.")
        return

    # Create an empty DataFrame to store merge request data
    df_merge_requests = pd.DataFrame(columns=["Name", "MergeRequestCount", "LinesAdded", "LinesRemoved"])

    # Fetch merge requests for each user
    for user_id, username in user_data.items():
        merge_requests_data = fetch_merge_requests(user_id, private_token)
        if merge_requests_data:
            # Create DataFrame with merge requests data for this user
            df_user_merge_requests = pd.DataFrame({"Name": [username],
                                                   "MergeRequestCount": len(merge_requests_data),
                                                   "LinesAdded": 0,
                                                   "LinesRemoved": 0})

            # Fetch and process merge request changes data for each merge request
            for merge_request in merge_requests_data:
                merge_request_iid = merge_request["iid"]
                changes_data = fetch_merge_request_changes(merge_request_iid, private_token)
                if changes_data:
                    # Combine all changes data into one variable
                    all_changes = ""
                    for change in changes_data["changes"]:
                        all_changes += change["diff"]

                    # Calculate the number of lines added (n+) and removed (n-)
                    lines_added_count = all_changes.count("\n+")
                    lines_removed_count = all_changes.count("\n-")

                    # Add lines added and removed to user's DataFrame
                    df_user_merge_requests["LinesAdded"] += lines_added_count
                    df_user_merge_requests["LinesRemoved"] += lines_removed_count

            # Append user's data to df_merge_requests
            df_merge_requests = pd.concat([df_merge_requests, df_user_merge_requests], ignore_index=True)

    # Save data to Excel
    file_name = "gitlab_merge_requests.xlsx"
    df_merge_requests.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")

# Execute main function
if __name__ == "__main__":
    main()
#Actual Code