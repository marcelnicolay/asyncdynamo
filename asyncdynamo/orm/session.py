from asyncdynamo import asyncdynamo

class Session(object):
    
    _session = None
    
    def __new__(cls):

        if not cls._session:
            raise(ValueError("Session is not created"))

        return cls._session
        
    @classmethod
    def create(cls, *args, **kwargs):
        if not cls._session:
            cls._session = asyncdynamo.AsyncDynamoDB(*args, **kwargs)
    
    @classmethod
    def destroy(cls):
        cls._session = None

