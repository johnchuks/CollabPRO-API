
def check_auth_user_credentials(current_user, request_user):
    """ Utility function to check if the information requested for belongs
    to the current logged in user """
    if current_user != request_user:
        return False
    return True
