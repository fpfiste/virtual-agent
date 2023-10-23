
import datetime as dt

from botbuilder.core import MessageFactory
from botbuilder.dialogs import DialogSet



class DialogStateTracker():
    def __init__(self, config, conversation_property_accessor):
        self.config = config
        self.dialog_set = DialogSet(conversation_property_accessor)
        self.active_dialog = None

    async def track_dialog_state(self, turn_context, user_profile):
        try:
            ### Check if user started a new dialog and add to dialog set if so
            intent = turn_context.activity.intent
            dialog_added = None
            # if intent == 'UserGuidance.RestartConversation':
            #     await self.start_over(turn_context)
            #     return None
            if intent != 'None':
                skill = self.config.INTENT_SKILL_DICT[intent]
                dialog = skill(self.config, user_profile)
                setattr(dialog, 'initialization_time', dt.datetime.utcnow())
                if dialog.id not in self.dialog_set._dialogs:
                    self.dialog_set.add(dialog)
                    self.active_dialog = dialog
                    dialog_added = dialog
            dialog_context = await self.dialog_set.create_context(turn_context)

            #### Map extracted entities to corresponding slots in dialogs
            entities_mapped = self.entity_slot_mapping(dialog_context.context)
            print(entities_mapped)
            #### add active dialog and mapped entities dict to dialog context
            setattr(dialog_context.dialogs, 'active_dialog', self.active_dialog)
            setattr(dialog_context.dialogs, 'entities_mapped', entities_mapped)
            setattr(dialog_context.dialogs, 'dialog_added', dialog_added)
        except Exception as e:
            print(e)

        return dialog_context


    def entity_slot_mapping(self, turn_context):
        entities = turn_context.activity.entities
        entities_mapped = {}
        if entities != []:
            for key, value in self.dialog_set._dialogs.items():
                entities_mapped[key] = 0
                for entity in entities:
                    entity_type = entity.type
                    if not hasattr(value, 'data_model'):
                        continue
                    data_model = value.data_model
                    entity_slot_dict = data_model._entity_slot_dict
                    if entity_type in entity_slot_dict:
                        slot = entity_slot_dict[entity_type]
                        setattr(data_model, slot, entity.entity)
                        entities_mapped[key] += 1
        entities_mapped = {x:y for x,y in entities_mapped.items() if y!=0}
        return entities_mapped


    async def end_active_dialog(self,active_dialog):
        self.dialog_set._dialogs.pop(active_dialog.id)
        self.active_dialog = None
        return

    # async def start_over(self, turn_context):
    #     await self.conversation_state.clear_state(turn_context)
    #     await self.conversation_state.save_changes(turn_context, True)
    #     answer ="The current conversation history has been cleared. Please restart."
    #     await turn_context.send_activity(MessageFactory.text(answer))








