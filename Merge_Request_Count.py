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
def fetch_merge_requests(user_id, private_token, target_month):
    api_url = f"https://git.automate.com/api/v4/projects/testing%2Fam-ui-automation/merge_requests?scope=all&state=merged&author_id={user_id}"
    headers = {"Private-Token": private_token}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        merge_requests_data = response.json()
        # Filter merge requests based on target month
        merge_requests_data = [mr for mr in merge_requests_data if pd.to_datetime(mr["created_at"]).month == target_month.month and pd.to_datetime(mr["created_at"]).year == target_month.year]
        return merge_requests_data
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
    months = pd.date_range(start="2024-01-01", end="2024-03-31", freq="MS")  # Generate a range of months for the year 2023

    for target_month in months:
        # Get user IDs and usernames for all users with pagination
        user_data = get_all_user_data(private_token)
        if not user_data:
            print("No users found.")
            continue

        # Create an empty DataFrame to store merge request data
        df_merge_requests = pd.DataFrame(columns=["Project Name","Name", "MergeRequestCount", "LinesAdded", "LinesRemoved"])

        # Fetch merge requests for each user
        for user_id, username in user_data.items():
            merge_requests_data = fetch_merge_requests(user_id, private_token, target_month)
            if merge_requests_data:
                # Calculate total lines added and removed for this user
                total_lines_added = 0
                total_lines_removed = 0
                for merge_request in merge_requests_data:
                    merge_request_iid = merge_request["iid"]
                    changes_data = fetch_merge_request_changes(merge_request_iid, private_token)
                    if changes_data:
                        # Combine all changes data into one variable
                        all_changes = "".join(change["diff"] for change in changes_data["changes"])
                        # Calculate the number of lines added (n+) and removed (n-)
                        total_lines_added += all_changes.count("\n+")
                        total_lines_removed += all_changes.count("\n-")

                    # Append user's data to df_merge_requests
                user_df = pd.DataFrame({
                    "Project Name":"am-ui-automation",
                    "Name": [username],
                    "MergeRequestCount": len(merge_requests_data),
                    "LinesAdded": total_lines_added,
                    "LinesRemoved": total_lines_removed,
                    "Created_at": None  # You can update this if needed
                })
                df_merge_requests = pd.concat([df_merge_requests, user_df], ignore_index=True)

        # Save data to Excel for the current month
        file_name = f"gitlab_merge_requests_{target_month.strftime('%B_%Y')}.xlsx"
        df_merge_requests.to_excel(file_name, index=False)
        print(f"Data saved to {file_name}")

# Execute main function
if __name__ == "__main__":
    main()
