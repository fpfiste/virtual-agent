# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
from pprint import pprint
from botbuilder.core import UserState
from requests_oauthlib import OAuth2Session



class GraphClient:
    def __init__(self, config, user_state = UserState):
        self.user_state = user_state
        self.config = config
        self.client = OAuth2Session(token={"access_token": self.config.MSGRAPH_ACCESS_TOKEN, "token_type": "Bearer"})
        self.base_url = config.MSGRAPH_API_BASE_URL

    def get_user_email_by_identity(self, user_id):
        url = self.base_url + '/users/{}/identities'.format(user_id)
        response = self.client.get(url)
        user_email = json.loads(response.text)['value'][0]['issuerAssignedId']
        return user_email

    def get_user_info(self, user_email) -> {}:
        url = self.base_url + '/users/' +user_email
        response = self.client.get(url)
        return json.loads(response.text)






## /users/d3bba431-e44b-45fc-943d-c0da55c127bd/people?$search="Christian"
