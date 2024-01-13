from openai import OpenAI
import os
import json
import linearfunctions

def transcription_reader(transcript: str) -> str:
    """
    Takes a conversation transcript and creates or updates a feature request, bug report or does nothing
    
    :param transcript:  String that is passed in after a finished conversation
    :return: String which details whether the transcript detailed a feature request, bug report or neither. If it details
    a feature request or bug report, it also returns the issueID that was created or updated, otherwise it returns None
    """ 
    client = OpenAI(api_key=os.environ.get('OPENAI_KEY'),)
    messages = [{"role": "system", "content": 'You are a helpful assistant with access to several tools.'}, {"role": "user", "content": transcript}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "create_bug_report",
                "description": "Create a bug report for a specific team",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "teamId": {
                            "type": "string",
                            "description": "The identifier of the team for which the bug report is created",
                        },
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
                        "teamId": {
                            "type": "string",
                            "description": "The identifier of the team for which the feature request is created",
                        },
                        "title": {
                            "type": "string",
                            "description": "Title of the feature request",
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description of the requested feature",
                        },
                    },
                    "required": ["teamId"]
                },
            },
        },
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "create_bug_report": linearfunctions.create_bug_report,
            "create_feature_request": linearfunctions.create_feature_request,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print(function_to_call)
            print(function_args)


if __name__ == '__main__':
    default_transcript_files = ['bug_transcript.txt', 'feature_transcript.txt', 'payment_transcript.txt']
    ### Maybe add one that contains both a bug report and a transcript feature

    filepath = 'transcripts/'
    file = open(filepath+default_transcript_files[0], "r") # can change according to the transcript you want to use
    transcript = file.read()
    result = transcription_reader(transcript=transcript)
    




