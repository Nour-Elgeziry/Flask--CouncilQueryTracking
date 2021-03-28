from query import Query


class RoadWork(Query):
    def __init__(self):
        self.username = ""
        self.type = ""
        self.state = None
        self.address = ""
        self.question = ""
        self.answer = ""

    def get_username(self):  # get method
        return self.username

    def set_username(self, name):  # set method
        self.username = name

    def get_type(self):  # get method
        return self.type

    def set_type(self, the_type):  # set method
        self.type = the_type

    def get_state(self):  # get method
        return self.state

    def set_state(self, status):  # set method
        self.state = status

    def addQuestion(self):
        pass

    def getAddress(self):
        return self.address

    def setAddress(self, theaddress):
        self.address = theaddress

    def getQuestion(self):
        return self.question

    def setQuestion(self, ques):
        self.question = ques

    def getAnswer(self):
        return self.answer

    def setAnswer(self, ans):
        self.answer = ans
