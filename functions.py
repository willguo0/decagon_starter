def create_bug_report(teamId: str, title: str = None, description: str = None) -> str:
    """
    Creatse a bug report for a specific team. Creates a new Linear issue
    
    :param teamId: The identifier of the team for which the bug report is created
    :param title: Title of the bug report
    :param description: Detailed description of the bug
    :return: The bug report's issue id
    """ 
    print(title, description, teamId)


def create_feature_request(teamId: str, title: str = None, description: str = None) -> str:
    """
    Creates a feature request for a specific team. Creates a new Linear issue
    :param teamId: The identifier of the team for which the feature request is created
    :param title: Title of the Feature Request
    :param description: Detailed description of the new feature request
    :return: The feature request's issue id
    """
    pass

def update_bug_report():
    #TODO later
    pass

def update_feature_request():
    #TODO later
    pass

def neither_bug_report_or_feature_request():
    #TODO later --- probably not necessary.
    pass
