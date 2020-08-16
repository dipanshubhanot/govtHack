from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from dbUtils import createQuery
import sqlite3 as sql


class Sendtosql(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.db_connection = sql.connect('calamitigator.db')
        self.location = kwargs.get('reportDict').get('location')
        self.description = kwargs.get('reportDict').get('description')
        self.tableName = kwargs.get('reportDict').get('tableName')
        self.phoneNum = kwargs.get('reportDict').get('phoneNum')
        self.keyword = 'Send-Report'

    def can_process(self,statement):
        if self.keyword in statement.text.split():
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        createQuery.insert_img(self.db_connection, self.tableName,
                               dateTime="CURRENT_TIMESTAMP", phoneNum=int(self.phoneNum),
                               location=str(self.location), description=str(self.description))

        response = Statement("Recorded!")
        response.confidence = 1
        return response

