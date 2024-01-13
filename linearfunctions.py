import requests
import os
import json


base_url = "https://api.linear.app/graphql"

#TODO Make it so you can pass in the user's API Key
api_key= os.environ.get('LINEAR_KEY')
headers = {
    "Authorization": f"{api_key}",
    "Content-Type": "application/json"
}

def create_issue(issue_type: str, title: str = '', description: str = '') -> str:
    """
    Creates a new Linear issue using GraphQL
    
    :param title: Title of the bug report
    :param title: Title of the new issue
    :param description: Detailed description of the issue
    :return: The issue_id if successful. None if a query failed
    """

    team_id = get_team_id()
    issue_label_id = get_issue_labels(issue_type)
    create_issue_query = f"""
        mutation IssueCreate {{
        issueCreate(
            input: {{
            title: "{title}"
            description: "{description}"
            teamId: "{team_id}"
            labelIds: ["{issue_label_id}"]
            }}
        ) {{
            success
            issue {{
            id
            title
            }}
        }}
        }}"""
    
    response = requests.post(base_url, headers=headers, json={"query": create_issue_query})
    if response.status_code == 200:
        print(issue_type + " report created successfully!")
        print("Issue ID:", response.content)
        content = json.loads(response.content.decode('utf-8')) # gets the query response's body content and converts to json
        issue_id = content['data']['issueCreate']['issue']['id']
        return issue_id
    else:
        print("Error creating issue. Status code:", response.status_code)
        print("Response:", response)
        return None

def get_team_id() -> str:
    """
    Queries for all the teams of the current user.

    :param None
    :return: The first team's id
    """

    # Query team for team we want to create an issue for
    teams_query = '''query Teams {
                teams {
                    nodes {
                    id
                    name
                    }
                 }
                }'''
    response = requests.post(base_url, headers=headers, json={"query": teams_query}) #TODO catch this response
    content = json.loads(response.content.decode('utf-8')) # gets the query response's body content and converts to json

    team_id = content['data']['teams']['nodes'][0]['id'] # may want to save this somewhere if we are doing the above query a lot.
    return team_id

def get_issue_labels(issue_type: str):
    """
    Queries for the label id for the given issue. If the label does not exist, the label is created and then the new label_id is returned

    :param issue_type: String that is either 'Bug' or 'Feature'
    :return: The label_id for the provided issue_type
    """
    # Query team for team we want to create an issue for
    teams_query = '''query Labels {
                issueLabels {
                    nodes {
                    id
                    name
                    }
                 }
                }'''
    response = requests.post(base_url, headers=headers, json={"query": teams_query}) #TODO catch this response
    content = json.loads(response.content.decode('utf-8'))
    labels = content['data']['issueLabels']['nodes']
    for label in labels:
        if label['name'] == issue_type:
            return label['id']
    #TODO Create the label

def create_bug_report(title: str = '', description: str = '') -> str:
    """
    Creates a bug report for a specific team. Creates a new Linear issue
    
    :param title: Title of the bug report
    :param description: Detailed description of the bug
    :return: The bug report's issue id
    """     
    return create_issue(issue_type='Bug', title=title, description=description)


# create_bug_report('fsjdio', 'testBUGGY', 'bug is testing this product')
def create_feature_request(title: str = '', description: str = '') -> str:
    """
    Creates a feature request for a specific team. Creates a new Linear issue
    :param title: Title of the Feature Request
    :param description: Detailed description of the new feature request
    :return: The feature request's issue id
    """
    
    return create_issue(issue_type='Feature', title=title, description=description)