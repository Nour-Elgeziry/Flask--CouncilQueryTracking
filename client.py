from queryFactory import QueryFactory


class Client:
    def __init__(self):
        self.username = ""
        self.email = ""
        self.query = QueryFactory()
        self.users = []

    def addUsers(self, user):
        self.users.append(user)

    def removeUsers(self, user):
        self.users.remove(user)

    def getUsers(self):
        return self.users

    def getUsersNames(self):
        names = ""
        for person in self.users:
            names = names + " " + person.getName()
        return names

    def setName(self, name):
        self.username = name

    def getName(self):
        return self.username

    def setEmail(self, email):
        self.email = email

    def getEmail(self):
        return self.email

    def setQuery(self):
        query = QueryFactory()
        self.query = query

    def getQuery(self):
        return self.query
