from state import State


class ClosedState(State):
    def queryState(self, context):
        context.set_State("Query Closed")
