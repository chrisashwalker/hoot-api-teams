class Team:

    def __init__(self, id, name, parent = None):
        self.id = id
        self.name = name
        self.parent = parent

    def rebuild(self, dict):
        self.id = dict["id"]
        self.name = dict["name"]
        self.parent = dict["parent"]