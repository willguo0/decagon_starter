##### Main file that contains transcription_reader which is the main function for this project
from openai import OpenAI
import os
import json
from linear_functions import create_bug_report, create_feature_request
from openai_helper import get_function_descriptions


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
            print(function_response)
            return function_response
            #TODO once the function returns stuff -- might need 
    else:
        print('no functions called')
        return None


if __name__ == '__main__':
    """testing code on pre-generated transcripts"""


    default_transcript_files = ['bug_transcript.txt', 'feature_transcript.txt', 'payment_transcript.txt']
    ### Maybe add one that contains both a bug report and a transcript feature

    filepath = 'transcripts/'
    file = open(filepath+default_transcript_files[0], "r") # can change according to the transcript you want to use
    transcript = file.read()
    result = transcription_reader(transcript=transcript)
    # determine_existing_task_exists(existing={'Inaccurate Calorie Tracking': 'eb01b728-5e78-4fad-9302-b9c4d1323de5'}, 
    #                         description='Users are reporting inaccuracies in the calorie tracking feature when logging workouts. The numbers seem to be inconsistent and not aligning with expected results based on workout intensity and duration.', title='Calorie Tracking Bug')

    




