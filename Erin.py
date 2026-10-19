from NEA_Main import *
from Scheduler import *
import tflearn 


class Erin():
    def __init__(self, model : tflearn.DNN, schedule):
        self.model = model
        self.schedule = schedule

    def textToScheduler(self,text):
        '''
        This method takes the natural language string from user input, parses the date from it, as well as the
        specified weekday, the name of the event, and the start and endpoints of the event and then finally adds the event into the schedule
        '''

        parsedDate = parseDates(text)
        day = weekdayExtractor(parsedDate.get('dayString'))
        time1 = dtConverter(parsedDate.get('startTime'))
        time2 = dtConverter(parsedDate.get('endTime'))
        eventName = extract_event(text)
        newEvent = Event(eventName[0])
        self.schedule.addEvent(day,startTime=time1,duration=None,endtime=time2,event=newEvent)

        
