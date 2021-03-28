from taxes import Taxes
from roadwork import RoadWork


class QueryFactory:
    def __init__(self):
        self.query = None

    def getQuery(self, the_type):
        if the_type is not None:
            if the_type.lower() == "taxes":
                self.query = Taxes()
            elif the_type.lower() == "road_work":
                self.query = RoadWork()
            else:
                self.query = None

        return self.query
