from models.question import Question
import json 
import pymysql 
import random

def connect_to_db():
    connection = pymysql.connect(
        host = 'localhost',
        user = 'qanysh@localhost',
        password = 'password',
        db = 'test_system',
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )

    print("Conected to  connection")
    return connection

class Storage:
    inst = None
    questions = None
    test_questions_number = None
    max_id = None


    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.inst is None:
            cls.inst = object.__new__(cls)
            cls.questions = []
            cls.test_questions_number = 0
            cls.max_id = 0
        return cls.inst


    def fill_storage(self):
        connection = connect_to_db()

        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM question;"
                cursor.execute(query)
                data = cursor.fetchall()   
                self.questions = [
                    Question.from_dict(i)
                    for i in data            
                ]
        except KeyError:
            print("not such key in  connection")
        finally:
            cursor.close()

        try: 

            with open('questions.json', 'r') as datafile:
                data = json.load(datafile)

            self.test_questions_number = data["test_questions_number"]   
            self.max_id = data["max_id"]
        except FileNotFoundError:
            print("No requested file 'questions.json'!")
        except KeyError:
            print('Invalid json. Requested format: { "questions": [], "test_questions_number" : <val>, "max_id" : <val> }')
        
                
        
    def save_question_statistics(self, question):
        connection = connect_to_db()

        try:
            with connection.cursor() as cursor:
                query = "UPDATE question SET stat_cor = {stat_cor}, stat_wrg = {stat_wrg} where id = {id};" 
                query = query.format(
                    stat_cor = question.stat_cor, 
                    stat_wrg = question.stat_wrg,
                    id = question.id
                )
                cursor.execute(query)
                connection.commit()
        except Exception as ex:
            print(ex)
        finally:
            cursor.close()


    def save_questions(self, question):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO question (text, answers, stat_cor, stat_wrg) VALUES ('{text}', '{answers}', {stat_cor}, {stat_wrg});"
                query = query.format(
                    text = question.text,
                    answers = json.dumps(question.answers),
                    stat_cor = question.stat_cor,
                    stat_wrg = question.stat_wrg                
                )
                
                cursor.execute(query)
                connection.commit()
        except Exception as ex:
            print(ex)
        finally:
            cursor.close()


    def update_question(self, question):
        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                query = "UPDATE question SET  text = '{text}', answers = '{answers}', stat_cor = {stat_cor}, stat_wrg = {stat_wrg} where id = {id};"
                query = query.format(
                    text = question.text,
                    answers = json.dumps(question.answers),
                    stat_cor = question.stat_cor,
                    stat_wrg = question.stat_wrg,
                    id = question.id
                )
                cursor.execute(query)
                connection.commit()
        except Exception as ex:
            print(ex)
        finally:
            cursor.close()


    def delete_question(self, id):
        connection = connect_to_db()
        
        try:
            with connection.cursor() as cursor:
                query = "DELETE FROM question where id = {id};"
                query = query.format(id = id) 
                cursor.execute(query)
                connection.commit()
        except Exception as ex:
            print(ex)

    def fill_json(self):
        try: 
            data = {
                "test_questions_number": self.test_questions_number,
                "max_id": self.max_id
            }

            with open('questions.json', 'w') as datafile:
                json.dump(
                    data, 
                    datafile, 
                    indent=4, 
                    sort_keys=False, 
                    ensure_ascii=False
                )

        except FileNotFoundError:
            print("No requested file 'questions.json'!")

