from typing import Callable, Awaitable, List
from botbuilder.core import Middleware, TurnContext, UserState
from botbuilder.schema import ActivityTypes, Activity, ResourceResponse

from EnhancedCoreSystem import Logger
from SystemRequirements import UserProfile
from EnhancedCoreSystem import Translator


class Middleware_Translation(Middleware):
    def __init__(self, config, user_state:UserState):
        self._translator = Translator(config)
        self._user_state = user_state
        self.user_profile_accessor = user_state.create_property("UserState")
        self.logger = Logger(config)

    async def on_turn(self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]):
        if context.activity.type == ActivityTypes.message:

            ###### Log original user input
            context.activity.additional_properties['userinput_original'] = context.activity.text
            user_profile = await self.user_profile_accessor.get(context, UserProfile)
            langDetected = self._translator.detect(context.activity.text)
            if user_profile.language != langDetected:
                user_profile.language = langDetected
            translation = self._translator.translate(lang_from=user_profile.language, lang_to='en', text=context.activity.text)
            context.activity.additional_properties['userinput_translated'] = translation
            context.activity.text = translation

        # Register outgoing handler.
        context.on_send_activities(self._outgoing_handler)

        # Continue processing messages.
        await logic()

    async def _outgoing_handler(self, context: TurnContext, activities: List[Activity],logic: Callable[[TurnContext], Awaitable[List[ResourceResponse]]]):
        user_profile = await self.user_profile_accessor.get(context, UserProfile)
        for activity in activities:
            if activity.type == ActivityTypes.message:
                context.activity.additional_properties['bot_answer'] = activity.text
                langDetected = self._translator.detect(activity.text)
                if langDetected != user_profile.language:
                    answer = self._translator.translate(lang_from='en', lang_to=user_profile.language, text=activity.text)
                    activity.text = answer
                    context.activity.additional_properties['bot_answer_translated'] = activity.text
        self.logger.log_turn(context.activity)
        return await logic()






