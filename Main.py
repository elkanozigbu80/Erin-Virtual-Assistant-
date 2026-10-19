#Main Execution File
from NEA_Main import *   #Import the main code
erinModel = model.load('Erin Alpha')  # Load the most recently trained chatbot model
unpickler = Unpickler(open('schedule.obj','rb'))  # Initialise object deserialiser
erinSchedule = unpickler.load()  # load the most recently saved schedule object
if __name__ == '__main__':
    '''
    Execution Statement
    '''
    erin = Erin.Erin(model=erinModel,schedule=erinSchedule)
    chat()
    
    