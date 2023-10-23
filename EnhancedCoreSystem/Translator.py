import requests, uuid


class Translator():
    def __init__(self, config):
        self._headers = {
        'Ocp-Apim-Subscription-Key': config.TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': config.TRANSLATOR_LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())}
        self._translationurl = config.TRANSLATOR_ENDPOINT_URL + '/translate'
        self._detectionurl = config.TRANSLATOR_ENDPOINT_URL + '/detect'

    def detect(self, message):
        params = {'api-version': '3.0'}
        body = [{ 'text': message }]
        request = requests.post(self._detectionurl, params=params, headers=self._headers, json=body)
        response = request.json()
        response = response[0]['language']
        return response

    def translate(self, lang_from, lang_to, text):
        params = {'api-version': '3.0', 'from': lang_from, 'to':lang_to }
        body = [{'text': text}]
        request = requests.post(self._translationurl, params=params, headers=self._headers, json=body)
        response = request.json()
        response = response[0]['translations'][0]['text']
        #response= json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
        return response






