from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from dbUtils import createQuery
import sqlite3 as sql

class Sendtosql(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        print(kwargs)
        self.reportDict = kwargs.get('reportDict')
        self.location = kwargs.get('reportDict').get('location')
        self.description = kwargs.get('reportDict').get('description')
        self.tableName = kwargs.get('reportDict').get('tableName')
        self.phoneNum = kwargs.get('reportDict').get('phoneNum')
        self.keyword = 'send-sql'

    def can_process(self, statement):
        if self.keyword in statement.text.split(':'):
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        params = (int(self.phoneNum),str(self.location),"Heloooo")
        with sql.connect('calamitigator.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO hazardly VALUES(CURRENT_TIMESTAMP, ?, ?, ? )",params)

        response = Statement("Data Stored and on it's way!")
        response.confidence = 1
        return response
