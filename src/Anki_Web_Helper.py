import json
import urllib.request

class Anki_Web_Helper:

    def __init__(self):
        pass
    def _request(self, action, **params):
        return {'action': action, 'params': params, 'version': 6}

    def _invoke(self, action, **params):
        requestJson = json.dumps(self._request(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])

        return response['result']

    def getDeckNames(self):
        return self._invoke("deckNames")

    def getAllCardsFromDeck(self, deckName):
        return self._invoke(action="findCards", query=f"deck:{deckName}")

    def getInfoForCards(self, cardIdList):
        return self._invoke(action="cardsInfo", cards=cardIdList)

    def addNode(self, noteDic):
        return self._invoke(action="addNote", note=noteDic)

    def deleteNotes(self, cardIdList):
        return self._invoke(action="deleteNotes", notes=cardIdList)

    def updateNote(self, noteDic):
        return self._invoke(action="updateNote", note=noteDic)

    def createDeck(self, deckName):
        return self._invoke(action="createDeck", deck=deckName)
