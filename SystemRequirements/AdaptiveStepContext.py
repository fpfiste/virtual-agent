# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict

from botbuilder.dialogs.dialog_context import DialogContext
from botbuilder.dialogs.dialog_reason import DialogReason
from botbuilder.dialogs.dialog_turn_result import DialogTurnResult
from botbuilder.dialogs.dialog_state import DialogState

class AdaptiveStepContext(DialogContext):
    def __init__(self, parent, dc: DialogContext, options: object, values: Dict[str, object], currentstep: int, reason: DialogReason, result: object = None, slots: list = None):
        super(AdaptiveStepContext, self).__init__(dc.dialogs, dc.context, DialogState(dc.stack))
        self._wf_parent = parent
        self._next_called = False
        self._step = currentstep
        self._options = options
        self._reason = reason
        self._result = result
        self._values = values
        self.parent = dc.parent
        self._slots = slots


    @property
    def step(self) -> int:
        return self._step

    @property
    def options(self) -> object:
        return self._options

    @property
    def reason(self) -> DialogReason:
        return self._reason

    @property
    def result(self) -> object:
        return self._result

    @property
    def values(self) -> Dict[str, object]:
        return self._values

    @property
    def slots(self):
        return self._slots

    async def next(self, result: object) -> DialogTurnResult:
        if self._next_called is True:
            raise Exception("WaterfallStepContext.next(): method already called for dialog and step '%s'[%s]."% (self._wf_parent.id, self._index))
        # Trigger next step
        self._next_called = True
        return await self._wf_parent.resume_dialog(self, DialogReason.NextCalled, result)