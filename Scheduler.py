from Event import *  # Importing the Event class 
from EventParser import *  # Importing EventParser 
from DateParserII import *  # Importing DateParserII 
import pickle  # For saving and loading the schedule object

class Schedule():
    def __init__(self):
        # Initialize the schedule dictionary with keys for each day of the week
        self.schedule = {
            "monday": {},
            "tuesday": {},
            "wednesday": {},
            "thursday": {},
            "friday": {},
            "saturday": {},
            "sunday": {}
        }
        self.saveSchedule()  # Save the initialized schedule to a file

    def addEvent(self, day: str, startTime: list, duration: list, endtime: list, event: Event):
        """
        Add an event to the schedule.
        
        Parameters:
        - day (str): Day of the week to add the event.
        - startTime (list): Start time in [hour, minute].
        - duration (list): Duration in [hour, minute].
        - endtime (list): End time in [hour, minute] (optional if duration is provided).
        - event (Event): The event object to add.
        
        Returns:
        - dict: Updated schedule.
        """
        timeframe = self.getTimeFrame(start=startTime, duration=duration, endtime=endtime)  # Calculate event timeframe
        self.schedule[day][timeframe] = event.getEventName()  # Add the event to the schedule
        return self.schedule

    def saveSchedule(self):
        #Save the current schedule object to a file
        schedule_file = open('schedule.obj', 'wb')  # Open file 
        pickle.dump(self, schedule_file)  # Serialize and save the schedule object

    def clearSchedule(self):
        #Clear all events from the schedule.
        for key in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            self.schedule[key].clear()  # Clear the events for each day
        return self.schedule

    def getTimeFrame(self, start, duration, endtime):
        """
        Calculate the timeframe of an event based on start time, duration, or end time.
        Parameters:
        - start (list): Start time in [hour, minute].
        - duration (list): Duration in [hour, minute].
        - endtime (list): End time in [hour, minute] (optional).
        Returns:
        - str: Timeframe in the format "HH:MM-HH:MM".
        """
        finalTime = [0, 0]  # Initialize the final time

        if endtime is not None:
            # If end time is provided, use it directly
            finalTime[0] = endtime[0]
            finalTime[1] = endtime[1]
        elif duration is not None:
            # If duration is provided, calculate the end time
            finalTime[1] = (start[1] + duration[1]) % 60  # Calculate minutes with overflow
            if finalTime[1] == 0:
                finalTime[1] = "00"  # Format minutes as "00" if zero
            carryover = (start[1] + duration[1]) // 60  # Carry over extra hours from minutes
            finalTime[0] = start[0] + duration[0] + carryover  # Calculate hours
            if start[1] == 0:
                start[1] = "00"  # Format start minutes as "00" if zero

        # Create a string representing the timeframe
        timeFrame = (str(start[0]) + ":" + str(start[1]) + "-" + str(finalTime[0]) + ":" + str(finalTime[1]))
        return timeFrame

    def removeEvent(self, day, timeframe):
        """
        Remove an event from the schedule.

        Parameters:
        - day (str): Day of the week.
        - timeframe (str): Timeframe of the event to remove.

        Returns:
        - dict: Updated schedule.
        """
        self.schedule[day].pop(timeframe)  # Remove the event by its timeframe
        self.saveSchedule()  # Save the updated schedule
        return self.schedule

    def debugPreview(self):
        #Print the current schedule for debugging purposes.
        print(self.schedule)

