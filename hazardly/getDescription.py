from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class getDesc(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.reportDict = kwargs.get('reportDict')
        self.keyword = 'desc->'

    def can_process(self,statement):
        if self.keyword in statement.text.split(':'):
            print(str(statement.text.split()).strip('[').strip('[').strip(','))
            return True
        else:
            return False

    def process(self,statement, additional_response_selection_parameters=None):
        self.reportDict['description'] = str(statement.text.split()).strip('[').strip('[').strip(',')
        print(self.reportDict)
        response = Statement("Recorded!")
        response.confidence = 1
        return response

