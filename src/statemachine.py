class State:
    def __init__(self, name, connections, initial):
        self.name = name
        self.initial = initial
        self.connections = connections

class StateMachine:
    def __init__(self):
        self.activeState = ''
        self.states = {}

    def __str__(self):
        s = '{Active State: ' + self.activeState + ', States: '
        for state in self.states.items():
            s += state[1].name + ', '
        return s + '}'

    def addState(self, name, connections=[], initial=False):
        self.states[name] = State(name, connections, initial)
        if initial:
            self.activeState = name
    
    def to(self, name):
        for connection in self.states[self.activeState].connections:
            if connection == name:
                self.activeState = name
                return
        raise Exception('Failed to change state. StateMachine: ' + str(self))