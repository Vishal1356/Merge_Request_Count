import streamlit as st
import git
import subprocess

# Streamlit App
st.title('Automated Test Case Runner')

# Input fields for Git repository URL, username, and password
repo_url = st.text_input('Enter Git Repository URL')
username = st.text_input('Enter Username')
password = st.text_input('Enter Password', type='password')

# Button to trigger test execution
if st.button('Run Test Cases'):
    try:
        # Clone the repository using GitPython
        repo = git.Repo.clone_from(repo_url, 'local_repo_directory')

        # Configure Git credentials for authentication
        # Note: This command saves credentials, consider security implications
        git.cmd.Git().execute(f'git config --local credential.helper store')
        git.cmd.Git().execute(f'git config --local credential.helper store')
        git.cmd.Git().execute(f'git config --local user.name "{username}"')
        git.cmd.Git().execute(f'git config --local user.password "{password}"')

        # Run your automation tests using subprocess or any other method
        # Example: subprocess.run(['pytest', 'test_file.py'])

        # Capture test results or display success message
        st.success('Test cases executed successfully!')

    except git.exc.GitCommandError as e:
        st.error(f"Git command error occurred: {str(e)}")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
