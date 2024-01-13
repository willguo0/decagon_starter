from openai import OpenAI
import os

def get_function_descriptions():
    """
    Returns a list that contains the function descriptions the chatbot can access.
    TODO Make it so it's not hardcoded -- i.e it reads the linearfunctions.py and scrapes and formats the below information.

    :param None
    :return: List of Function objects. Each object contains the function name, a description of the function's 
             purpose and the properites needed to be passed in.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "create_bug_report",
                "description": "Create a bug report for a specific team",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the bug report",
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the bug",
                        },
                    },
                    "required": ["teamId"]
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_feature_request",
                "description": "Create a feature request for a specific team",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the feature request",
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the requested feature",
                        },
                    },
                },
            },
        },
    ]

def determine_existing_task_exists(existing: dict,  title: str, description: str):
    """
    Takes a dictionary of existing issues in a Linear Workspace and see if a given description and title match any of them
    
    :param existing:  Dictionary that contains the titles of existing issues in a Linear Workspace. The title of the issue is the key and the issue_id is the value
    :param description:  Description of the current issue being evaluated for a match
    :param title:  Title of the curernt issue being evaluated for a match
    :return: If a match is found, the id of the existing issue is returned. Otherwise the string 'no matches' is returned.
    """
    client = OpenAI(api_key=os.environ.get('OPENAI_KEY'),)
    # client = OpenAI(api_key='',)
    
    # prompt assumes that there is only one match
    system_content = \
        'You trying to determine whether a given description matches and title matches any of the provided titles. \
        If there is a match return the exact title of the match. If there is no match, say "None"'
    content = 'The given title is ' + title +'. The given description is ' + description + '\n'
    content += 'The provided titles are as follows: '
    for existing_title in existing.keys():
        content+= existing_title + ', '
    content = content[:-2] # shave off last comma
    messages = [{"role": "system", "content": system_content}, {
        "role": "user", "content": content}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_message = response.choices[0].message # maybe do fuzzy string matching if this fails too often.
    title_match = response_message.content # Provided title if there is a match. Otherwise 'None'
    if title_match in existing:
        return existing[title_match]
    else:
        return None