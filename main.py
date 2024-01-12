default_transcript_feature = """User: Hi! I've been using your app and absolutely love it, but I have a suggestion for a feature that I think could make it even better.
Chatbot: That's wonderful to hear! We're always open to user suggestions. What feature do you have in mind?
User: I was thinking it would be great to have a virtual workout buddy feature. The idea is to connect with friends who also use the app, share workout progress, and maybe even challenge each other.
Chatbot: That's an interesting suggestion! A virtual workout buddy feature could add a social and motivational aspect to the app. How do you envision this feature working?
User: Ideally, users could connect with their friends on the app, see each other's workout activities, and maybe set friendly challenges or goals. It could be a fun way to stay motivated and engaged in fitness routines.
Chatbot: I see! That sounds like a great idea for fostering a sense of community and motivation among users. We'll definitely consider it for future updates. Thank you for sharing your thoughts! If you have any more details or other suggestions, feel free to let us know.
User: Sure thing! I'm glad you like the idea. If you need more details or have any questions, I'm here to help. Keep up the good work with the app!
Chatbot: Thank you for your support! We appreciate your feedback and look forward to making the app even better. If you have any more ideas in the future, don't hesitate to reach out. Happy exercising!."""

default_transcript_bug_report = """User: Hi there! I've been using your app and overall love the experience, but I've come across a bug that's been bothering me.
Chatbot: I'm sorry to hear that you're facing an issue. We appreciate you bringing it to our attention. Could you please provide more details about the bug so we can better understand and address it?
User: Certainly. It seems that whenever I try to log my workout using the app, the calorie tracking feature isn't calculating accurately. The numbers seem a bit off, and I've double-checked the data I input.
Chatbot: I apologize for the inconvenience you're experiencing with the calorie tracking. We take this seriously, and we want to resolve it for you. Can you share more specifics about the workouts you've logged and any patterns you've noticed with the inaccuracies?
User: It happens consistently, regardless of the type of workout – whether it's cardio or strength training. The calories burned just don't align with what I would expect based on the intensity and duration of the exercises.
Chatbot: Thank you for providing those details. We'll investigate this issue further to identify and fix the bug causing the inaccuracies in calorie tracking. In the meantime, is there anything else about the bug that you've observed or any other aspects of the app you'd like to discuss?
User: No, that's the main issue I've encountered. I appreciate your prompt response and willingness to look into it.
Chatbot: It's our pleasure. We value your feedback, and our team will work diligently to address this bug and ensure a more accurate calorie tracking experience. If you think of anything else or have additional details to share, please feel free to reach out. We're here to help!
User: Thanks for your assistance. I look forward to the resolution. If there's anything I can do to assist with troubleshooting, let me know.
Chatbot: Absolutely! We may reach out for more information if needed. Thank you for your understanding and patience. We'll keep you updated on the progress. If you have any more concerns or questions, don't hesitate to contact us. Happy exercising!"""

default_transcript_neither= """User: Hi! I've been using your app for a while, and I need to switch my payment method. How can I do that?
Chatbot: Of course! I'm happy to help you with that. To switch your payment method, you can go to the "Account" or "Settings" section in the app. Look for the "Payment" or "Billing" option, and there should be an option to update or change your payment method.
User: Thanks for the guidance. I'll give it a try. Do I need to enter the new payment information, or is there a specific process I should follow?
Chatbot: When you navigate to the payment section, you'll likely find an option to "Add" or "Update" payment details. Click on that, and you'll be prompted to enter the new payment information, including credit card details or any other preferred payment method."""

### Maybe add one that contains both a bug report and a transcript feature

###make above be in random file.....
print(default_transcript_feature)

def transcription_reader(transcript: str) -> str:
    """
    Takes a conversation transcript and creates or updates a feature request, bug report or does nothing
    
    :param transcript:  String that is passed in after a finished conversation
    :return: String which details whether the transcript detailed a feature request, bug report or neither. If it details
    a feature request or bug report, it also returns the issueID that was created or updated, otherwise it returns None
    """ 
    pass