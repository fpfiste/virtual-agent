import json

import requests

from EnhancedCoreSystem import GraphClient


class SetReminder(GraphClient):
    def __init__(self, config):
        super().__init__(config)

    def set_reminder(self, user_id, subject, date_time_from, date_time_to):
        #url = 'https://graph.microsoft.com/v1.0/users/{}/events'.format(user_id)

        url = self.base_url + '/users/{}/events'.format(user_id)
        time_zone = self.get_time_zone(user_id)
        headers = {'Content-type': 'application/json'}
        event ={
                "subject": subject,
                "start": {
                    "dateTime": date_time_from,
                    "timeZone": time_zone
                },
                "end": {
                    "dateTime": date_time_to,
                    "timeZone": time_zone
                }
            }

        data = json.dumps(event)

        try:
            self.client.post(url, data=data, headers=headers)
        except Exception as e:
            print('ERROR: ', e)

    def get_time_zone(self, user_id):
        url = self.base_url + '/users/{}/mailboxsettings'.format(user_id)
        response = self.client.get(url)
        data = json.loads(response.text)
        return data['timeZone']








