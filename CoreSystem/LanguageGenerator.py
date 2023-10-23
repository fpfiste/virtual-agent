import random


class LanguageGenerator():
    def __init__(self, answer_template_class):
        self.answer_templates = answer_template_class

    def generate_anwer(self, current_step, slots=None):
        templates = getattr(self.answer_templates,current_step)
        template = random.choice(templates)
        try:
            answer = template.format(*slots)
        except TypeError:
            answer = template
        return answer



if __name__ == '__main__':
    class SetReminderAnswerTemplates():
        user_email = ["In order to schedule a meeting for you, i need your email.",
                      "I need your email adress to set the reminder.",
                      "Can you please give me your email so that i can set the reminder?"]

        subject = ["What should i remind you of?",
                   "What is the subject of the reminder?",
                   "What is the reminder about?"]

        date_time = ["When should I set the reminder?",
                     "When would you like to be reminded?",
                     "When should i remind you?"]

        query = ['I set a reminder with the title "{0}" for {1} into your outlook calendar',
                 'The reminder {0} is set into your outlook calendar for {1}',
                 'I will remind you of {0} on {1}']

    test = SetReminderAnswerTemplates()

    generator = LanguageGenerator(SetReminderAnswerTemplates())
    slots = ('Test', 'Tomorrow 9 am')
    current_step = 'query'
    print(generator.generate_anwer(current_step, slots))







