import uuid
from typing import Coroutine
from botbuilder.core import TurnContext
from botbuilder.schema import ActivityTypes
from botbuilder.dialogs.dialog_reason import DialogReason
from botbuilder.dialogs.dialog import Dialog
from botbuilder.dialogs.dialog_turn_result import DialogTurnResult
from botbuilder.dialogs.dialog_context import DialogContext
from botbuilder.dialogs.dialog_instance import DialogInstance


from SystemRequirements.AdaptiveStepContext import AdaptiveStepContext


class AdaptiveDialog(Dialog):
    PersistedOptions = "options"
    CurrentStep = 'currentStep'
    StepIndex = "stepIndex"
    PersistedValues = "values"
    PersistedInstanceId = "instanceId"

    def __init__(self, dialog_id: str, steps: [Coroutine] = None, datamodel = None):
        super(AdaptiveDialog, self).__init__(dialog_id)
        if not steps:
            self._steps = []
        else:
            if not isinstance(steps, list):
                raise TypeError("AdaptiveDialog(): steps must be list of steps")
            self._steps = steps
        self.datamodel = datamodel
        self.slots = [attr for attr in dir(self.datamodel) if not callable(getattr(self.datamodel, attr)) and not attr.startswith("_")]
        self.slots.reverse()
        self.status = None


    def add_step(self, step):
        """Adds a new step to the waterfall.:param step: Step to add:return: Waterfall dialog for fluent calls to `add_step()`."""
        if not step:
            raise TypeError("WaterfallDialog.add_step(): step cannot be None.")
        self._steps.append(step)
        return self

    async def begin_dialog(self, dialog_context: DialogContext, options: object = None) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError("AdaptiveDialog.begin_dialog(): dc cannot be None.")
        # Initialize waterfall state
        self.status = 'Waiting'
        state = dialog_context.active_dialog.state

        instance_id = uuid.uuid1().__str__()
        state[self.PersistedOptions] = options
        state[self.PersistedValues] = {}
        state[self.PersistedInstanceId] = instance_id
        properties = {}
        properties["DialogId"] = self.id
        properties["InstanceId"] = instance_id
        self.telemetry_client.track_event("WaterfallStart", properties)
        # Run first stepkinds


        return await self.run_step(dialog_context, 0, DialogReason.BeginCalled, None)



    async def continue_dialog(self,dialog_context: DialogContext = None,reason: DialogReason = None,result: object = NotImplementedError()) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError("AdaptiveDialog.continue_dialog(): dc cannot be None.")
        if dialog_context.context.activity.type != ActivityTypes.message:
            return Dialog.end_of_turn
        return await self.resume_dialog(dialog_context,DialogReason.ContinueCalled,dialog_context.context.activity.text)

    async def resume_dialog(self, dialog_context: DialogContext, reason: DialogReason, result):
        if dialog_context is None:
            raise TypeError("AdaptiveDialog.resume_dialog(): dc cannot be None.")
        # Increment step index and run step
        state = dialog_context.active_dialog.state
        return await self.run_step(dialog_context, 1, reason, result)

    async def end_dialog(self, context: TurnContext, instance: DialogInstance, reason: DialogReason) -> DialogTurnResult:
        self.status = 'finished'
        if reason is DialogReason.CancelCalled:
            index = instance.state[self.StepIndex]
            step_name = self.get_step_name(index)
            instance_id = str(instance.state[self.PersistedInstanceId])
            properties = {"DialogId": self.id,"StepName": step_name,"InstanceId": instance_id}
            self.telemetry_client.track_event("WaterfallCancel", properties)
        else:
            if reason is DialogReason.EndCalled:
                instance_id = str(instance.state[self.PersistedInstanceId])
                properties = {"DialogId": self.id, "InstanceId": instance_id}
                self.telemetry_client.track_event("WaterfallComplete", properties)
        return reason

    async def run_step(self,dialog_context: DialogContext,index: int,reason: DialogReason,result: object) -> DialogTurnResult:
        if not dialog_context:
            raise TypeError("AdaptiveDialog.run_steps(): dialog_context cannot be None.")
        ### Slot filling with LUIS entities
        # if self.query_performed == True:
        #     return await dialog_context.end_dialog()

        ### Create state object
        state = dialog_context.active_dialog.state
        options = state[self.PersistedOptions]
        values = state[self.PersistedValues]


        ### Find empty slots
        empty_slot = None
        if len(self.slots) != 0:
            for slot in self.slots:
                if not getattr(self.datamodel,slot):
                    empty_slot = slot
                    break



        ### Find next step
        if empty_slot != None:
            state[self.CurrentStep] = slot
            current_step = slot
        else:
            state[self.CurrentStep] = 'query'
            state['slots'] = self.slots
            current_step = 'query'

        if self.datamodel is not None:
            slots = self.datamodel.__dict__
        else:
            slots = None

        step_context = AdaptiveStepContext(self, dialog_context, options, values,current_step, reason, result, slots)
        return await self.on_step(step_context)


    async def on_step(self, step_context: AdaptiveStepContext) -> DialogTurnResult:
        step = step_context.step
        stepindex = self.get_step_name(step)
        instance_id = str(step_context.active_dialog.state[self.PersistedInstanceId])
        properties = {"DialogId": self.id,"StepName": step,"InstanceId": instance_id}
        self.telemetry_client.track_event("WaterfallStep", properties)
        return await self._steps[stepindex](step_context)


    def get_step_name(self, step: str) -> str:
        """Give the waterfall step a unique name"""
        for stepindex in range(len(self._steps)):
            step_name = self._steps[stepindex].__name__
            if step == step_name:
                return stepindex

