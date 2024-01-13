import requests
import os
import json
from openai_helper import determine_existing_task_exists

base_url = "https://api.linear.app/graphql"

#TODO Make it so you can pass in the user's API Key
api_key= os.environ.get('LINEAR_KEY')
headers = {
    "Authorization": f"{api_key}",
    "Content-Type": "application/json"
}




def create_issue(issue_type: str, title: str = '', description: str = '') -> str:
    """
    Creates a new Linear issue using GraphQL. If there is determined to be an existing issue with a similar title or description, 
    the existing issue is updated with a comment 
    
    :param title: Title of the bug report
    :param title: Title of the new issue
    :param description: Detailed description of the issue
    :return: The issue_id if successful. None if a query failed
    """

    team_id = get_team_id()
    if team_id == None:
        return None
    
    issue_label_id = get_issue_labels(issue_type) # maybe add generated by AI Label
    if issue_label_id == None:
        return None

    ###### check to see if there is an existing issue with a similar description or title
    
    existing_title_to_id = query_existing_tasks(issue_type=issue_type)
    existing_id = determine_existing_task_exists(existing=existing_title_to_id, description=description, title=title)
    update = False

    if existing_id != None:
        update = True
        query = f"""
        mutation commentCreate{{
        commentCreate(
            input:{{
                issueId: "{existing_id}"
                body: "{title + " " + description}"
            
            }}
        ){{success
                comment {{
                    issue{{
                        id
                        title
                    }}
                }}
            }}
        }}


        """
    else:
        query = f"""
        mutation issueCreate {{
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
    
    response = requests.post(base_url, headers=headers, json={"query": query})
    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8')) # gets the query response's body content and converts to json
        if update:
            print('Updated successfully')
            issue_id = content['data']['commentCreate']['comment']['issue']['id']
        else:
            print(issue_type + " report created successfully!")
            issue_id = content['data']['issueCreate']['issue']['id']
        print("Issue ID:", response.content)
        
        return issue_id
    else:
        print(query)
        print("Error creating issue. Status code:", response.status_code)
        print("Response:", response)
        return None

def query_existing_tasks(issue_type: str) -> str:

    # we don't want the description as that would use too many tokens
    issue_query = f"""query Issues {{
                        issues(filter: {{ 
                            labels: {{ name: {{ eq: "{issue_type}" }} }}
                        }}) {{
                            nodes {{
                            id, title
                            }}
                        }}
                        }}"""
    response = requests.post(base_url, headers=headers, json={"query": issue_query})
    if response.status_code != 200:
        print("Error fetching labels. Status code:", response.status_code)
        print("Response:", response)
        return None
    content = json.loads(response.content.decode('utf-8'))
    issues = content['data']['issues']['nodes'] # list of ids and titles of all issues with the given label
    title_to_id = {}
    for issue in issues: # maybe is too slow if we have a lot of issues
        id = issue['id']
        title = issue['title']
        title_to_id[title] = id
    return title_to_id

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
    response = requests.post(base_url, headers=headers, json={"query": teams_query})
    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8')) # gets the query response's body content and converts to json

        team_id = content['data']['teams']['nodes'][0]['id'] # may want to save this somewhere if we are doing the above query a lot.
        return team_id
    else:
        print("Error getting teams. Status code:", response.status_code)
        print("Response:", response)
        return None

def get_issue_labels(issue_type: str):
    """
    Queries for the label id for the given issue. If the label does not exist, the label is created and then the new label_id is returned

    :param issue_type: String that is either 'Bug' or 'Feature'
    :return: The label_id for the provided issue_type
    """
    # Query team for team we want to create an issue for
    labels_query = '''query Labels {
                issueLabels {
                    nodes {
                        id
                        name
                    }
                 }
                }'''
    response = requests.post(base_url, headers=headers, json={"query": labels_query})
    if response.status_code != 200:
        print("Error fetching labels. Status code:", response.status_code)
        print("Response:", response)
        return None
    content = json.loads(response.content.decode('utf-8'))
    labels = content['data']['issueLabels']['nodes']
    for label in labels:
        if label['name'] == issue_type:
            return label['id'] # maybe want to store this result as there are only 2 possible ones
    
    # Create the label --- probably not neccessary as bug and feature are default labels
    # TODO add a generated by AI label

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