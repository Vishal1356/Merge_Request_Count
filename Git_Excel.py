import requests
from openpyxl import Workbook
from datetime import datetime

# GitLab API endpoint and personal access token
gitlab_url = 'https://git.automate.com/api/v4/users'
access_token = 'fzsqL4ppitPYBEUcF6sH'

#m1XGzsLPvFzaTXqBQhQZ
# Function to get PRs by person and date
def get_prs_by_person_and_date(username, start_date, end_date):
    headers = {'PRIVATE-TOKEN': access_token}
    # Get user ID by username
     #  user_response = requests.get(f'{gitlab_url}/users', headers=headers)
    user_response = requests.get(f'{gitlab_url}', headers=headers)
    user_id = user_response.json()[0]['id'] if user_response.status_code == 200 else None

    if not user_id:
        print(f"User '{username}' not found.")
        return []

    # Get merge requests by user ID and date range
    merge_requests_url = f'{gitlab_url}merge_requests?source_user_id={user_id}&created_after={start_date}&created_before={end_date}'
    merge_requests_response = requests.get(merge_requests_url, headers=headers)

    if merge_requests_response.status_code != 200:
        print(f"Error fetching merge requests: {merge_requests_response.text}")
        return []

    return merge_requests_response.json()


# Function to create Excel file
def create_excel_file(filename):
    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'Title', 'Author', 'Created At', 'Web URL'])

    # for pr in data:
    #     ws.append([pr['id'], pr['title'], pr['author']['username'], pr['created_at'], pr['web_url']])

    wb.save(filename)


if __name__ == "__main__":
    # Input parameters

    #
    #
    # username ='vishal.ganji'
    # start_date = '2023-01-01T00:00:00Z'  # Replace with your desired start date
    # end_date = '2024-01-10T23:59:59Z'  # Replace with your desired end date
    #
    # # Get PRs
    # prs_data = get_prs_by_person_and_date(username, start_date, end_date)

    # Create Excel file
    excel_filename = 'gitlab_prs.xlsx'
    create_excel_file(excel_filename)

    print(f"Excel file '{excel_filename}' created successfully.")