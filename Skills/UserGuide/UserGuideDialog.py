# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import ComponentDialog
from botbuilder.core import MessageFactory, UserState
from .UserGuide import UserGuide
from SystemRequirements import AdaptiveDialog, AdaptiveStepContext



class UserGuidanceDialog(ComponentDialog):
    """Get a list of all functinoalities of the digital assistant"""

    def __init__(self, config, user_state: UserState):
        super(UserGuidanceDialog, self).__init__(UserGuidanceDialog.__name__)
        self.config = config
        self.user_guide = UserGuide(config)
        self.add_dialog(AdaptiveDialog(UserGuidanceDialog.__name__,[self.query]))
        self.initial_dialog_id = UserGuidanceDialog.__name__



    async def query(self, step_context: AdaptiveStepContext):
        docstrings = self.user_guide.get_skill_doc_strings()
        answer = 'I can do the following tasks: \n'
        for string in docstrings:
            answer += '-\t' + string + '\n'
        await step_context.context.send_activity(MessageFactory.text(answer))
        return await step_context.end_dialog()
