#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

from Skills.UserGuide import UserGuidanceDialog
from Skills.SetReminderSkill import SetReminderDialog


class DefaultConfig:
    """ Bot Configuration """
    PORT = 3978

    #### App Information
    #APP_ID = os.environ.get("MicrosoftAppId", "f34b74bc-ef02-407d-b618-84f23e72ac04")
    APP_ID = os.environ.get("MicrosoftAppId", "a3d1bd2d-45c8-4e52-ac12-58b5a657643c")
    #APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "aBw_VVHFO.OK5uV4Dw~as4vm7m_4.Ba8uI")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", ".-46~Hv.827-V_eNYTp2V4tzN.53II5fHd")
    EXPIRE_AFTER_SECONDS = os.environ.get("ExpireAfterSeconds", 300)

    #############################################################
    # Config System Requirements
    #############################################################

    #### LUIS API KEYS & Credentials
    LUIS_APP_ID = ''
    LUIS_KEY = ''
    LUIS_URL = ''
    LUIS_AUTH_KEY = ''
    LUIS_AUTH_ENDPOINT = ""
    LUIS_PRED_ENDPOINT = ""
    LUIS_VERSION = '0.1'

    #### MSGraph API KEYS & Credentials    
    MSGRAPH_API_BASE_URL = ''
    MSGRAPH_ACCESS_TOKEN = ''
    #### Translator API KEYS & Credentials
    TRANSLATOR_KEY = ''
    TRANSLATOR_ENDPOINT_URL = ''
    TRANSLATOR_LOCATION = ''

    #### Log Database
    LOG_DB_CONNECTION = ''
    LOG_DB_NAME = '' # 'DigitalAssistantDev'/'DigitalAssistantTest'


    ##################################
    # Skill config
    #################################

    #### SKILLS
    INTENT_SKILL_DICT = {
        'UserGuidance.ListSkills': UserGuidanceDialog,
        'skill.SetReminder': SetReminderDialog
    }


    #### Open Weather Map API
    WEATHER_OPEN_WEATHERMAP_API_KEY = ''
    WEATHER_OPEN_WEATHERMAP_BASE_URL = ""





if __name__ == '__main__':

    config = DefaultConfig()
    intent = 'None'
    dialog = config.INTENT_SKILL_DICT[intent]
    print(dialog)
