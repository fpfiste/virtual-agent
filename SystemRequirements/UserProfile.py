# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Attachment


class UserProfile:
    """
      This is our application state. Just a regular serializable Python class.
    """

    def __init__(self, userid:str=None, givenname: str=None, surname: str=None, email: str = None, location: str = None, language: str=None):
        self.userid = userid
        self.givenname = givenname
        self.surname = surname
        self.email = email
        self.location = location
        self.language = language


