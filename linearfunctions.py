import requests
import os
import json
base_url = "https://api.linear.app/graphql"
def create_bug_report(teamId: str, title: str = None, description: str = None) -> str:
    """
    Creatse a bug report for a specific team. Creates a new Linear issue
    
    :param teamId: The identifier of the team for which the bug report is created
    :param title: Title of the bug report
    :param description: Detailed description of the bug
    :return: The bug report's issue id
    """ 
    api_key= os.environ.get('LINEAR_KEY')
    headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json"
    }
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
    content = json.loads(response.content.decode('utf-8')) # gets the query response's body content and converts to json
    team_id = content['data']['teams']['nodes'][0]['id'] # may want to save this somewhere if we are doing the above query a lot.
    print(team_id)
    create_issue_query = f"""
        mutation IssueCreate {{
        issueCreate(
            input: {{
            title: "{title}"
            description: "{description}"
            teamId: "{team_id}"
            }}
        ) {{
            success
            issue {{
            id
            title
            }}
        }}
        }}"""
    print(create_issue_query)
    response = requests.post(base_url, headers=headers, json={"query": create_issue_query})
    if response.status_code == 200:
        print("Issue created successfully!")
        print("Issue ID:", response.content)
    else:
        print("Error creating issue. Status code:", response.status_code)
        print("Response:", response)

    print('Bug report created')

create_bug_report('fsjdio', 'test', 'bug is testing this product')
def create_feature_request(teamId: str, title: str = None, description: str = None) -> str:
    """
    Creates a feature request for a specific team. Creates a new Linear issue
    :param teamId: The identifier of the team for which the feature request is created
    :param title: Title of the Feature Request
    :param description: Detailed description of the new feature request
    :return: The feature request's issue id
    """
    print('Feature_request created')

def update_bug_report():
    #TODO later
    pass

def update_feature_request():
    #TODO later
    pass

def neither_bug_report_or_feature_request():
    #TODO later --- probably not necessary.
    pass
