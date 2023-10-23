# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from datetime import timedelta, datetime

from botbuilder.dialogs import ComponentDialog, Dialog
from botbuilder.core import MessageFactory, UserState
from SystemRequirements import AdaptiveDialog, AdaptiveStepContext, UserProfile
from CoreSystem import LUISClient, LanguageGenerator
from .SetReminderAnswerTemplates import SetReminderAnswerTemplates
from .SetReminderDatamodel import SetReminderDataModel
from .SetReminder import SetReminder


class SetReminderDialog(ComponentDialog):
    """Set a reminder into the users outlook calendar"""

    def __init__(self, config, user_profile):

        super(SetReminderDialog, self).__init__(SetReminderDialog.__name__)

        #### Get config class ####
        self.config = config

        #### Get reminder setter class ####
        self.reminder_setter = SetReminder(config)



        #### Get Dialog DataModel ####
        self.data_model = SetReminderDataModel(user_profile)
        self.add_dialog(AdaptiveDialog(SetReminderDialog.__name__,
                                       [self.user_email,
                                        self.subject,
                                        self.date_time,
                                        self.query],
                                       self.data_model))
        self.initial_dialog_id = SetReminderDialog.__name__
        self._luis = LUISClient(config)
        self.language_generator = LanguageGenerator(SetReminderAnswerTemplates())




    async def user_email(self, step_context: AdaptiveStepContext):
        answer = self.language_generator.generate_anwer(current_step=step_context.step)
        await step_context.context.send_activity(MessageFactory.text(answer))
        return Dialog.end_of_turn

    async def subject(self, step_context: AdaptiveStepContext):
        answer = self.language_generator.generate_anwer(current_step=step_context.step)
        await step_context.context.send_activity(MessageFactory.text(answer))
        return Dialog.end_of_turn

    async def date_time(self, step_context: AdaptiveStepContext):
        answer = self.language_generator.generate_anwer(current_step=step_context.step)
        await step_context.context.send_activity(MessageFactory.text(answer))
        return Dialog.end_of_turn


    async def query(self, step_context: AdaptiveStepContext):
        print('here')
        answer = 'I set a reminder with the title "{0}" for {1} into your outlook calendar'
        user_email = step_context._slots['user_email']
        remindersubject = step_context._slots['subject']
        date_time = step_context._slots['date_time']
        date_time_from, date_time_type= self._luis.resolve_date_time(date_time)
        if date_time_type == 'datetimeV2.time' or date_time_type == 'datetimeV2.datetime':
            date_time_to = date_time_from + timedelta(minutes=15)
        elif date_time_type == 'datetimeV2.date':
            date_time_to = date_time_from + timedelta(days=1)


        try:
            self.reminder_setter.set_reminder(user_email, remindersubject, date_time_from.isoformat(), date_time_to.isoformat())
        except Exception as e:
            print(e)
        slots = (remindersubject, date_time_from)
        answer = self.language_generator.generate_anwer(current_step=step_context.step, slots = slots)

        await step_context.context.send_activity(MessageFactory.text(answer))
        return await step_context.end_dialog()

