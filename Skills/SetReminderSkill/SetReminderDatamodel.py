from datetime import datetime

from botbuilder.core import user_state

from SystemRequirements import UserProfile


class SetReminderDataModel():
    def __init__(self, user_profile):
        try:
            self.user_email = user_profile.email
        except:
            self.user_email = None
        self.subject = None
        self.date_time = None



        self._entity_slot_dict = {'builtin.email': 'user_email',
                                  'reminderSubject': 'subject',
                                  'builtin.datetimeV2.datetime': 'date_time',
                                  'builtin.datetimeV2.time': 'date_time',
                                  'builtin.datetimeV2.date': 'date_time'}




if __name__ == '__main__':
    dm = SetReminderDataModel()

    # required_slots =   [value for value in dm._entity_slot_dict.values() if dm.__dict__[value]['required']]
    # slot_count = len(required_slots)
    # filled_count = 0
    # for value in required_slots:
    #     if isinstance(dm.__dict__[value]['values'], list) and len(dm.__dict__[value]['values']):
    #         filled_count += 1
    #     if dm.__dict__[value]['values'] :
    #         filled_count += 1


    print(dm.__dict__)








