from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class getDesc(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.reportDict = kwargs.get('reportDict')
        self.keyword = 'desc'

    def can_process(self,statement):
        if self.keyword in statement.text.split(':'):
            return True
        else:
            return False

    def process(self,statement, additional_response_selection_parameters=None):
        dict(self.reportDict)["description"] = str(statement.text.split().remove(
            self.keyword)).strip('[]').strip(',')
        response = Statement("Recorded!")
        response.confidence = 1
        return response

