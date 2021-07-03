import uuid as uuida 
class arashId:
    """This class generates an incremental deterministic id for tests 
    """
    def __init__(self):
        self.current_number = 3000 
    def uuid4(self):
        self.current_number = self.current_number + 1
        return str(self.current_number)

def id_gen( test, ArashId ):
        """
            This function generates the id based oh the type of test.

            :param <test>: <input>
            :type <string>: <test specified the type of id>

            :param <ArashId>: <input>
            :type <class>: <generates an incremental deterministic id for tests>

        """
        if test == True :
            uuid = ArashId
            return uuid.uuid4()
        else:
            uuid = uuida
            return uuid.uuid4().hex

