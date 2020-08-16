from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import sqlite3 as sql
dbCon = sql.connect('calamitigator.db')
# Creating ChatBot Instance

reportDict = {
    'location': 'loremIpsum',
    'phoneNum': 987654332,
    'dbCon': dbCon,
    'tableName':'hazardly',
}
myChatBot = ChatBot(
    'Hazardly',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
         'chatterbot.logic.MathematicalEvaluation',
         'chatterbot.logic.TimeLogicAdapter',
        # 'chatterbot.logic.BestMatch',
        # {
        #     'import_path': 'chatterbot.logic.BestMatch',
        #     'default_response': 'I am sorry, but I do not understand. If it is an emergency, '
        #                         'please call 000.',
        #     'maximum_similarity_threshold': 0.90
        # },
         {
            'import_path':'hazardly.getDescription.getDesc'
         },
        {
            'import_path':'hazardly.Sendtosql.Sendtosql'
        }
    ],
    database_uri='sqlite:///database.sqlite3',
    reportDict=reportDict
)

training_data_quesans = open('training_data/hazardly/ques_ans.txt').read().splitlines()

training_data = training_data_quesans

trainer = ListTrainer(myChatBot)
trainer.train(training_data)

# # Training with English Corpus Data
# trainer_corpus = ChatterBotCorpusTrainer(myChatBot)
# trainer_corpus.train(
#     'chatterbot.corpus.english'
# )
