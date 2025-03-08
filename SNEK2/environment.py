from .common import ErrorType, Error


class Environment:
    def __init__(self, parent=None):
        self.values = dict()
        self.parent = parent

    def get(self, name):
        if name.src not in self.values:
            if self.parent is not None:
                return self.parent.get(name)
            raise Error(ErrorType.UNBOUND_VARIABLE_ERROR, name, f"Variable \"{name.src}\" not defined")
        return self.values[name.src]
    
    def assign(self, name, value):
        if name not in self.values:
            if self.parent is not None:
                return self.parent.assign(name, value)
        self.values[name] = value
    
    def delete(self, name):
        if name.src not in self.values:
            raise Error(ErrorType.UNBOUND_VARIABLE_ERROR, name, f"Variable \"{name.src}\" not defined")
        del self.values[name.src]

    
    
