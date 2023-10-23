
from datetime import datetime, date


from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
import recognizers_suite as Recognizers




class LUISClient():
    def __init__(self, config):
        self.app_id = config.LUIS_APP_ID
        self.version = config.LUIS_VERSION
        self.luis_auth_client = LUISAuthoringClient(config.LUIS_AUTH_ENDPOINT, CognitiveServicesCredentials(config.LUIS_AUTH_KEY))
        self.clientRuntime = LUISRuntimeClient(endpoint=config.LUIS_PRED_ENDPOINT,credentials=CognitiveServicesCredentials(config.LUIS_KEY))


    ######## Model Training Functions ############

    def add_utterance(self, utterance, intent):
        data = {'text': utterance,
                'intentName': intent,
                'entityLabels': []}
        self.luis_auth_client.examples.add(self.app_id, self.version, data)

    def add_new_intent(self, intentName):
        self.luis_auth_client.model.add_intent(self.app_id, self.version, intentName)

    def train_luis(self):
        self.luis_auth_client.train.train_version(self.app_id, self.version)

    ######## Model Prediction Functions ###########

    def get_prediction(self, message, all_intents=True, min_score=0):
        luis_result = self.clientRuntime.prediction.resolve(self.app_id, message, verbose=all_intents)

        if all_intents:
            return luis_result.intents
        if luis_result.top_scoring_intent.score < min_score:
            luis_result.top_scoring_intent.intent = 'None'
        return luis_result

    def resolve_date_time(self, date_time):
        date_time = Recognizers.recognize_datetime(date_time, Recognizers.Culture.English)
        type = date_time[0].__dict__['type_name']
        value = date_time[0].__dict__['resolution']['values'][0]['value']
        result = None
        if type == 'datetimeV2.time':
            time = datetime.strptime(value, '%H:%M:%S').time()
            result = datetime.combine(date.today(), time)
        elif type == 'datetimeV2.date':
            result = datetime.strptime(value, '%Y-%m-%d')
        elif type == 'datetimeV2.datetime':
            result = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return (result, type)






















