from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance

armDict = {
    'location': 'loremIpsum',
    'phoneNum': 987654332,
    'dbCon': 'dbCon',
    'tableName':'tableName',
}
armBot = ChatBot(
    'Armour',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. If it is an emergency, '
                                'please call 000.',
            'maximum_similarity_threshold': 0.90
        },
        {
            'import_path':'armour.getDescription.getDesc'
         },
        {
            'import_path':'armour.Sendtosql.Sendtosql'
        }
    ],
    database_uri='sqlite:///database.sqlite3',
    reportDict=armDict
)

training_data_quesans = open('training_data/armour/ques_ans.txt').read().splitlines()

training_data = training_data_quesans

trainer = ListTrainer(armBot)
trainer.train(training_data)

# Training with English Corpus Data
trainer_corpus = ChatterBotCorpusTrainer(armBot)
trainer_corpus.train(
    'chatterbot.corpus.english'
)
