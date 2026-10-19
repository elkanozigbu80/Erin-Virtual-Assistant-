class Event():
    def __init__(self,EventName : str):
        self.Name = EventName


    def updateEventName(self,NewName):
        '''
        Updates the name of the event if needed
        '''
        self.Name = NewName
    
    def getEventName(self):
        '''
        Accesses the name of the event
        '''
        return self.Name
