import spacy
import parsedatetime as pdt
from datetime import datetime

# Loads the small English model from spaCy for natural language processing
eng = spacy.load("en_core_web_sm")

def parseDates(text):
    """
    Extract and parse date and time information from the input text.

    Args:
        text (str): The input text containing time or date expressions.
    
    Returns:
        dict: A dictionary containing:
            - dayString: The interpreted day as a datetime object.
            - startTime: The parsed start time as a datetime object.
            - endTime: The parsed end time as a datetime object.
        str: If start and end times cannot be identified, returns an error message.
    """
    # Initializes parsedatetime's Calendar object
    cal = pdt.Calendar()
    now = datetime.today()  # Get the current date and time for context

    # Parse the input text using spaCy to extract entities
    doc = eng(text)
    time_expressions = []  # List to store identified time expressions

    # Loop through the named entities in the text
    for ent in doc.ents:
        # If the entity label is 'TIME', add it to the time expressions list
        if ent.label_ == "TIME":
            time_expressions.append(ent.text)

    # Print the identified time expressions (for debugging)
    print(time_expressions)

    # If there is one time expression, split it into start and end (e.g., "3 PM to 5 PM")
    if len(time_expressions) == 1:
        time_expressions = time_expressions[0].split('to')

    # Print the split time expressions (for debugging)
    print(time_expressions)

    # If less than two time points are identified, return an error
    if len(time_expressions) < 2:
        return "Could not find both start and end times."

    start_time = None  # Placeholder for the start time
    end_time = None    # Placeholder for the end time

    # If there are valid time expressions, parse them into datetime objects
    if len(time_expressions) > 0:
        start_time = cal.parseDT(time_expressions[0], now)[0]  # Parse the start time
        end_time = cal.parseDT(time_expressions[1], start_time)[0]  # Parse the end time relative to the start time

    # Parse the full input text to extract the general day as a datetime object
    day_string = cal.parseDT(text)[0]

    # Return the parsed day, start time, and end time
    return {
        "dayString": day_string,
        "startTime": start_time,
        "endTime": end_time
    }

def dtConverter(x: datetime):
    """
    Convert a datetime object into a list containing the hour and minute.

    Args:
        x (datetime): The datetime object to convert.

    Returns:
        list: A list containing the hour and minute as integers.
    """
    hour = x.hour  # Extract the hour
    minute = x.minute  # Extract the minute
    final = [hour, minute]  # Create a list with hour and minute
    return final

def weekdayExtractor(date: datetime):
    """
    Extract the weekday name from a datetime object.

    Args:
        date (datetime): The datetime object to extract the weekday from.

    Returns:
        str: The name of the weekday (e.g., 'Monday', 'Tuesday').
    """
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weekday = days[date.weekday()]  # Get the weekday index and map it to the corresponding weekday name in english
    return weekday
