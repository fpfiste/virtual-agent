# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#
# from botbuilder.dialogs import ComponentDialog,WaterfallDialog,WaterfallStepContext,DialogTurnResult
# from botbuilder.dialogs.prompts import TextPrompt,PromptOptions
# from botbuilder.core import MessageFactory, UserState
# from data_models import UserProfile
# from SystemRequirements import Logger
#
#
#
# class SkillRecommendation(ComponentDialog):
#     def __init__(self, config, user_state: UserState):
#         super(SkillRecommendation, self).__init__(SkillRecommendation.__name__)
#         self.config = config
#         self.user_profile_accessor = user_state.create_property("UserState")
#         self.add_dialog(WaterfallDialog(SkillRecommendation.__name__, [self.first_step, self.second_step, self.third_step]))
#         self.add_dialog(TextPrompt(TextPrompt.__name__))
#         self.initial_dialog_id = SkillRecommendation.__name__
#
#     async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
#         user_profile = await self.user_profile_accessor.get(step_context.context, UserProfile)
#         print(user_profile.email)
#         if user_profile.email == None:
#             return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text("Please insert your email address.")))
#         else:
#             return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text("Please describe the skill you'd like me to learn.")))
#
#
#
#     async def second_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
#         user_profile = await self.user_profile_accessor.get(step_context.context, UserProfile)
#         if user_profile.email == None:
#             user_profile.email = step_context.result
#             return await step_context.prompt(TextPrompt.__name__,PromptOptions(prompt=MessageFactory.text("Please describe the skill you'd like me to learn.")))
#
#         else:
#             logger = Logger(self.config)
#             logger.log_skill_recommendations(user_profile.email,'', step_context.result)
#             await step_context.context.send_activity(MessageFactory.text('Thank you for your input! We will work on this.'))
#             return await step_context.end_dialog()
#
#     async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
#         user_profile = await self.user_profile_accessor.get(step_context.context, UserProfile)
#         logger = Logger(self.config)
#         logger.log_skill_recommendations(user_profile.email, '', step_context.result)
#         await step_context.context.send_activity(MessageFactory.text('Thank you for your input! We will work on this.'))
#         return await step_context.end_dialog()
#
