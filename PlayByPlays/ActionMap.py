from common import DB

class ActionMap:
       
    
    def __init__(self, actions):
        self.actions = actions

    def getByCode(self, code):
        pass
    
    @staticmethod
    def save_new(code=None, description=None):
        if code is None:
            raise ValueError('code is required')
    
        if description is None:
            description = 'NULL'
        
        DB._engine.execute(
            f"INSERT INTO ActionMap (code, description) VALUES ('{code}', '{description}')"
        )