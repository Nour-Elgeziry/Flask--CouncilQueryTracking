from state import State


class OpenState(State):
    def querState(self, context):
        context.set_state("Query Open")
