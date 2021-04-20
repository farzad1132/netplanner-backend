import uuid as uuida 
class arashId:
    def __init__(self):
        self.current_number = 3000 
    def uuid4(self):
        self.current_number = self.current_number + 1
        return str(self.current_number)

def id_gen( test, ArashId ):

        if test == True :
            uuid = ArashId
            return uuid.uuid4()
        else:
            uuid = uuida
            return uuid.uuid4().hex

