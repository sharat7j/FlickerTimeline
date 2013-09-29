from json import JSONEncoder

class myEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

