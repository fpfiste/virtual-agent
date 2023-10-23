from botbuilder.core import MessageFactory



class DialogPolicyMaker():
    def __init__(self, config):
        self.config = config



    async def define_next_step(self, dialog_context):
        #### if a dialog was added in this turn, pursue
        dialog_added = getattr(dialog_context.dialogs, 'dialog_added')
        if dialog_added:
            active_dialog = dialog_added
            await dialog_context.begin_dialog(dialog_added.id)
            result = list(active_dialog._dialogs._dialogs.values())[0]
        else:
            #### if now dialog was added, choose one
            active_dialog = self.choose_active_dialog(dialog_context)
            if active_dialog == None:
                answer ="I'm not sure what you want me to do. Please rephrase or check my functionalities by asking what i can do for you."
                await dialog_context.context.send_activity(MessageFactory.text(answer))
                result = None
            else:
                await active_dialog.continue_dialog(dialog_context)
                result = list(active_dialog._dialogs._dialogs.values())[0]
        return result, active_dialog




    def choose_active_dialog(self, dialog_context):
        dialog_stack = getattr(dialog_context.dialogs, '_dialogs')
        if len(dialog_stack)==0:
            return None
        active_dialog = getattr(dialog_context.dialogs, 'active_dialog')

        if active_dialog is not None:
            return active_dialog

        #### Pursue most relevant dialog from latest turn (active dialog with most entities mapped)
        entities_mapped = getattr(dialog_context.dialogs, 'entities_mapped')
        if entities_mapped != {}:
            max_entities_mapped = max(entities_mapped.values())
            print(max_entities_mapped)
            next_step_candidates = [key for key,value in entities_mapped.items() if value == max_entities_mapped]
            if len(next_step_candidates) == 1:
                active_dialog = dialog_stack[next_step_candidates[0]]
                return active_dialog


        #### Last in First out
        initialization_times  = {key:getattr(value, 'initialization_time') for key, value in dialog_stack.items()}

        active_dialog = dialog_stack[max(initialization_times, key=initialization_times.get)]
        return active_dialog


    # async def continue_active_dialog(self, dialog_context):
    #     self.entity_slot_mapping(dialog_context.context)
    #     return await self.active_dialogs[0].continue_dialog(dialog_context)






