from typing import Callable, Awaitable
from botbuilder.core import Middleware, TurnContext, UserState
from botbuilder.schema import ActivityTypes
from EnhancedCoreSystem import Logger
from SystemRequirements import UserProfile
from EnhancedCoreSystem import GraphClient


class Middleware_UserInfo(Middleware):
    def __init__(self, config, user_state:UserState):
        self._graphclient = GraphClient(config)
        self._user_state = user_state
        self.user_profile_accessor = user_state.create_property("UserState")
        self.logger = Logger(config)

    async def on_turn(self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]):
        if context.activity.type == ActivityTypes.message:
            user_profile = await self.user_profile_accessor.get(context, UserProfile)
            if not user_profile.email:
                try:
                    user_email = self._graphclient.get_user_email_by_identity(context.activity.from_property.aad_object_id)
                    user = self._graphclient.get_user_info(user_email)
                    user_profile.givenname = user['givenName']
                    user_profile.surname = user['surname']
                    user_profile.email = user['mail']
                    #user_profile.location = user['officeLocation']
                    user_profile.language = user['preferredLanguage'][0:2]
                except Exception as e:
                    pass

        context.activity.additional_properties['user_language'] = user_profile.language
        context.activity.additional_properties['user_email'] = user_profile.email

        # Continue processing messages.
        await logic()





