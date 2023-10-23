# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import time
from typing import List

from botbuilder.core import ActivityHandler, TurnContext, UserState, ConversationState
from CoreSystem import LUISClient, DialogStateTracker, DialogPolicyMaker
from SystemRequirements import UserProfile


class Orchestrator(ActivityHandler):
    def __init__(self, config, conversation_state:ConversationState, user_state:UserState):
        #### Load Conversation & User State classes
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.user_profile_accessor = user_state.create_property("UserState")
        self.conversation_property_accessor = self.conversation_state.create_property("DialogState")

        #### Load Core System
        self._luis = LUISClient(config)
        self.dst = DialogStateTracker(config, self.conversation_property_accessor)
        self.policy_maker = DialogPolicyMaker(config)

        #### Get user_profile class ####
        self._user_state = user_state
        self.user_profile_accessor = user_state.create_property("UserState")


    async def on_turn(self, turn_context: TurnContext):
        '''Rules to be executed at the end of every turn'''
        await super().on_turn(turn_context)
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        '''Rules to be executed on every incoming message'''

        #### Get User Profile ####
        user_profile = await self.user_profile_accessor.get(turn_context, UserProfile)
        print(user_profile)
        #### Extract intent & entities from user input ####
        luis_result = self._luis.get_prediction(turn_context.activity.text, all_intents=False, min_score = 0.8)
        intent = luis_result.top_scoring_intent.intent
        turn_context.activity.__dict__['intent'] = intent
        turn_context.activity.entities = luis_result.entities

        #### Track Dialog State ####
        dialog_context = await self.dst.track_dialog_state(turn_context, user_profile)


        if dialog_context != None:
            #### Define next step ####
            result, active_dialog = await self.policy_maker.define_next_step(dialog_context)

            print(result, active_dialog)

            # #### end complete dialogs
            if result != None and result.status == 'finished':
                await self.dst.end_active_dialog(active_dialog)








        # dialog_set = DialogSet(self.conversation_state.create_property("DialogState"))
        #
        # for dialog in self._active_dialogs:
        #     dialog_set.add(dialog)
        # dialog_context = await dialog_set.create_context(turn_context)
        #
        # if dialog_context.context.activity.intent != 'None':
        #
        #     await self.dst.initiate_new_dialog(dialog_context,dialog_set)
        # else:
        #     result = await self.dst.continue_active_dialog(dialog_context)
        #     print(result.status)
        #     if result.status == DialogTurnStatus.Complete:
        #        await self.dst.end_active_dialog(dialog_context)
        #     #     print(self.dst.active_dialogs)












        #### If there is no intent and no running dialog, generate Answer with the ChitChat Skill

        #### If an intent was detected, map the intent to the corresponding dialog and set self.dialog accordingly.
        # if intent != 'None' and self.dialog == None:
        #     skill = self._config.INTENT_SKILL_DICT[intent]
        #     self.dialog = skill(self._config, self.user_state)
        #
        # if intent != 'None':
        #     skill = self._config.INTENT_SKILL_DICT[intent]
        #     dialog = skill(self._config, self.user_state)
        #     self._active_dialogs.append(dialog)
        #     dialog_set.add(dialog)
        #     await dialog_context.begin_dialog(dialog.id)










            # for i in self._active_dialogs:
            #     print(i.__dict__['data_model'].__dict__)
            #await dialog_context.begin_dialog(dialog.id)



        # #### If self.dialog is not None, start/continue running dialog.
        # if self.dialog != None:
        #     dialog_set = DialogSet(self.conversation_state.create_property("DialogState"))
        #     dialog_set.add(self.dialog)
        #     dialog_context = await dialog_set.create_context(turn_context)
        #     if dialog_context.active_dialog is not None:
        #         print(self._active_dialogs)
        #         await dialog_context.continue_dialog()
        #         if dialog_context.active_dialog is None:
        #             self.dialog = None
        #     else:
        #         print('Start Dialog')
        #         await dialog_context.begin_dialog(self.dialog.id)
        #         if dialog_context.active_dialog is None:
        #             self.dialog = None
        #
        # elif intent == 'None' and self.dialog == None:
            # answer = self._chatterbot.chitchat_answer()
            # self._chatterbot.add_to_history(answer)
            # turn_context.activity.additional_properties['intent'] = intent
            # turn_context.activity.additional_properties['dialog'] = self.dialog
            #answer = 'I did not get that. Please check the functionalities'
    #         return await turn_context.send_activity(MessageFactory.text(answer))
    #
    #
    # def start_dialog(self, dialog):




