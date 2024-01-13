##### Main file that contains transcription_reader which is the main function for this project
##### Also contaisn other helper functions that 



from openai import OpenAI
import os
import json
from linearfunctions import create_bug_report, create_feature_request
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


def determine_existing_task_exists(existing: dict, description: str, title: str):
    client = OpenAI(api_key=os.environ.get('OPENAI_KEY'),)
    
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
    response_message = response.choices[0].message
    print(response_message)
determine_existing_task_exists(existing={'Inaccurate Calorie Tracking': 'eb01b728-5e78-4fad-9302-b9c4d1323de5'}, 
                               description='Users are reporting inaccuracies in the calorie tracking feature when logging workouts. The numbers seem to be inconsistent and not aligning with expected results based on workout intensity and duration.', title='Calorie Tracking Bug')


# main function to call
def transcription_reader(transcript: str) -> str:
    """
    Takes a conversation transcript and creates or updates a feature request, bug report or does nothing
    
    :param transcript:  String that is passed in after a finished conversation
    :return: String which details whether the transcript detailed a feature request, bug report or neither. If it details
    a feature request or bug report, it also returns the issueID that was created or updated, otherwise it returns None
    """ 
    client = OpenAI(api_key=os.environ.get('OPENAI_KEY'),)
    messages = [{"role": "system", "content": 'You are a helpful assistant with access to several tools.'}, {"role": "user", "content": transcript}]
    
    # available functions the api can call and access
    tools = get_function_descriptions()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )  # TODO add a limit to the token to prevent overusage of tokens?
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls: # Not none if the model wants to call a function
        available_functions = {
            "create_bug_report": create_bug_report,
            "create_feature_request": create_feature_request,
        }
        messages.append(response_message) # extend conversation with assistant's reply

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args) #TODO add check to make sure this doesn't error while it's unpacking (model can hallucinate extra params)
            # print(function_to_call)
            # print(function_args)
            # print(function_response)
            #TODO once the function returns stuff -- might need 
    else:
        print('no functions called')


# if __name__ == '__main__':
#     """testing code on pre-generated transcripts"""


#     default_transcript_files = ['bug_transcript.txt', 'feature_transcript.txt', 'payment_transcript.txt']
#     ### Maybe add one that contains both a bug report and a transcript feature

#     filepath = 'transcripts/'
#     file = open(filepath+default_transcript_files[0], "r") # can change according to the transcript you want to use
#     transcript = file.read()
#     result = transcription_reader(transcript=transcript)
    




