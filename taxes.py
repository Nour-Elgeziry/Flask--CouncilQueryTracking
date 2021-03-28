from query import Query


class Taxes(Query):
    def __init__(self):
        self.username = ""
        self.type = ""
        self.state = None
        self.socialNumber = ""
        self.question = ""
        self.answer = ""
        self.totalTaxes = 1000
        self.governmentPercentage = 20

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

    def getSocialNumber(self):
        return self.socialNumber

    def setSocialNumber(self, number):
        self.socialNumber = number

    def getQuestion(self):
        return self.question

    def setQuestion(self, ques):
        self.question = ques

    def getAnswer(self):
        return self.answer

    def setAnswer(self, ans):
        self.answer = ans

    def getTotalTax(self):
        tax = self.totalTaxes # tax on resident
        total_pay = (tax * self.governmentPercentage)/100  # amount to be paid by government
        return total_pay
