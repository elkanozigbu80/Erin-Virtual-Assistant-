import spacy
from spacy.matcher import Matcher

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

matcher = Matcher(nlp.vocab)
# initialise the basic patterns to be used by the pattern matcher
event_patterns = [
    [{"POS": "PROPN"}, {"TEXT": "'s"}, {"LOWER": "funeral"}],
    [{"POS": "PROPN"}, {"TEXT": "'s"}, {"LOWER": "wedding"}], 
    [{"POS": "PROPN"}, {"TEXT": "'s"}, {"LOWER": "football match"}],
    [{"POS": "PROPN"}, {"TEXT": "'s"}, {"LOWER": "graduation"}],
    [{"POS": "PROPN"}, {"TEXT": "'s"}, {"LOWER": "anniversary"}],
    [{"POS": "PROPN"}, {"TEXT": "'s"}, {"LOWER": "appointment"}],
    [{"POS": "PROPN"}, {"TEXT": "'s"}, {"POS": "NOUN"}],
    [{"POS": "PROPN"}, {"LOWER": "funeral"}],
    [{"POS": "PROPN"}, {"LOWER": "wedding"}], 
    [{"POS": "PROPN"}, {"LOWER": "football match"}],
    [{"POS": "PROPN"}, {"LOWER": "graduation"}],
    [{"POS": "PROPN"}, {"LOWER": "anniversary"}],
    [{"POS": "PROPN"}, {"LOWER": "appointment"}],
    [{"POS": "PROPN"}, {"POS": "NOUN"}],
    [{"POS": "NOUN"}, {"POS":"NOUN"}],
    [{"POS": "NOUN"},{"TEXT": "'s"}, {"POS": "NOUN"}],
    [{"POS": "NOUN"},{"TEXT": "’s"}, {"POS": "NOUN"}],
    [{"POS": "NOUN"}, {"POS": "NOUN"},{"POS": "NOUN"}],
    [{"POS": "ADJECTIVE"}, {"POS": "NOUN"},{"POS": "NOUN"}],
    [{"POS": "NOUN"},{"TEXT": "-"},{"POS": "NOUN"}, {"POS": "NOUN"}],
    [{"POS": "NOUN"}, {"POS": "VERB"}],
    [{"TEXT": "a"}, {"POS": "NOUN"}]
]

# Add patterns to the matcher
matcher.add("EVENTS", event_patterns)

def extract_event(sentence):
    '''
    Extract event-related phrases from the input sentence based on pattern matching.

    Args:
        sentence (str): The input sentence containing potential event descriptions.

    Returns:
        list: A list of event phrases extracted from the sentence, excluding the word "schedule".
    '''
    
    # Process the input sentence using the NLP pipeline (assumes `nlp` is defined globally)
    doc = nlp(sentence)
    
    # Use the matcher
    matches = matcher(doc)
    
    # Initialize an empty list to store identified events
    events = []
    
    # Iterate over the matched patterns returned by the matcher
    for match_id, start, end in matches:
        # Extract the span of the text that matches the pattern
        event_span = doc[start:end]
        
        # Exclude the word "schedule" from the list of events
        if event_span.text.lower() != "schedule":
            events.append(event_span.text)  # Add the event to the list
    
    # Return the list of parsed events
    return events

if __name__ == "__main__":
    print(extract_event("Please schedule my yoga class on Wednesday from 9:00 AM to 10:30 AM. "))
