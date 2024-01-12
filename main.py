def transcription_reader(transcript: str) -> str:
    """
    Takes a conversation transcript and creates or updates a feature request, bug report or does nothing
    
    :param transcript:  String that is passed in after a finished conversation
    :return: String which details whether the transcript detailed a feature request, bug report or neither. If it details
    a feature request or bug report, it also returns the issueID that was created or updated, otherwise it returns None
    """ 
    pass


if __name__ == '__main__':
    default_transcript_files = ['bug_transcript.txt', 'feature_transcript.txt', 'payment_transcript.txt']
    ### Maybe add one that contains both a bug report and a transcript feature


    file = open(default_transcript_files[0], "r") # can change according to the transcript you want to use
    transcript = file.read()
    transcription_reader(transcript=transcript)
    print('hi')




