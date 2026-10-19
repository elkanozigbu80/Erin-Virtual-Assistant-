import nltk
from nltk.stem.lancaster import LancasterStemmer  # For stemming words to their root forms
import numpy as np  # For numerical operations
import tflearn  # For building and training neural networks
import tensorflow as tf  # For neural network operations
import json  # For handling JSON data
import dill  # A library for saving and loading objects between execution
import random  # For random selection of bot responses
import Erin  # Custom module for managing the chatbot unit

tf.compat.v1.reset_default_graph() # Resets the kernel for each execution

# Custom unpickler to load serialized objects correctly
class Unpickler(dill.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "Scheduler"
        return super().find_class(module, name)
    # This class is used to create an unpickling object that opens a saved schedule for the program to read

# Load a pre-saved schedule object 
unpickler = Unpickler(open('schedule.obj', 'rb'))
erinSchedule = unpickler.load()

# Load intent data from a JSON file, which contains input patterns and corresponding responses
with open('intents.json') as intents:
    data = json.load(intents)

stemmer = LancasterStemmer()  # Instantiate the Lancaster stemmer for word normalization

# Initialize variables for processing intents and patterns
words = []  # List of all unique stemmed words
labels = []  # List of unique tags (intent categories)
x_docs = []  # Tokenized patterns
y_docs = []  # Corresponding intent tags for each pattern

# Process each intent in the JSON data
for intent in data['intents']:
    for pattern in intent['patterns']:
        # Tokenize each pattern into words
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)  # Add words to the main word list
        x_docs.append(wrds)  # Append tokenized words to x_docs
        y_docs.append(intent['tag'])  # Append the intent tag

        # Add the tag to the labels list if it's not already present
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

# Stem and lower all words, removing duplicates and any '?' characters
words = [stemmer.stem(w.lower()) for w in words if w not in '?']
words = sorted(list(set(words)))  # Sort and remove duplicates
labels = sorted(labels)  # Sort labels alphabetically

# Prepare training data and corresponding output labels
training = []  # Input feature vectors
output = []  # Output labels as one-hot vectors
out_empty = [0 for _ in range(len(labels))]  # Template for one-hot encoding

# Convert each pattern into a "bag of words" representation
for x, doc in enumerate(x_docs):
    bag = []  # Initialize bag of words for the current pattern
    wrds = [stemmer.stem(w) for w in doc]  # Stem the words in the pattern

    # Create a binary vector indicating whether each word in 'words' is in the current pattern
    for w in words:
        bag.append(1 if w in wrds else 0)

    # Create a one-hot encoded output for the current intent tag
    output_row = out_empty[:]
    output_row[labels.index(y_docs[x])] = 1

    training.append(bag)
    output.append(output_row)

# Convert training and output data to numpy arrays for compatibility with TensorFlow
training = np.array(training)
output = np.array(output)

# Build a neural network model using TFLearn
net = tflearn.input_data(shape=[None, len(training[0])])  # Input layer
net = tflearn.fully_connected(net, 10)  # First hidden layer with 10 neurons
net = tflearn.fully_connected(net, 10)  # Second hidden layer with 10 neurons
net = tflearn.fully_connected(net, 10)  # Third hidden layer with 10 neurons
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')  # Output layer
net = tflearn.regression(net)  # Regression layer for optimization

# Initialize and train the model
model = tflearn.DNN(net)
model.fit(training, output, n_epoch=500, batch_size=8, show_metric=True)  # Train for 500 epochs
model.save('Erin Alpha')  # Save the trained model

# Function to convert user input into a bag-of-words vector
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]  # Initialize bag of words
    s_words = nltk.word_tokenize(s)  # Tokenize user input
    s_words = [stemmer.stem(word.lower()) for word in s_words]  # Stem the words

    # Mark words present in the user input
    for s_word in s_words:
        for i, w in enumerate(words):
            if w == s_word:
                bag[i] = 1

    return np.array(bag)  # Return the bag-of-words vector as a numpy array

# Chat function to handle user input and generate responses
def chat():
    erin = Erin.Erin(model, erinSchedule)  # Initialize Erin
    while True:
        inp = input('You: ')  # Get user input
        results = model.predict([bag_of_words(inp, words)])  # Predict intent using the model
        results_index = np.argmax(results)  # Find the index of the highest probability
        tag = labels[results_index]  # Get the corresponding intent tag

        # Find responses associated with the detected intent
        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
                print(tag)
                print(f'Bot: {random.choice(responses)}')  # Randomly select a response

        # Handle special tags for schedule manipulation
        if tag == "schedule":
            erin.textToScheduler(inp)  # Send input to scheduling unit
            erin.schedule.saveSchedule()  # Save updated schedule
            erin.schedule.debugPreview()  # Used while debugging // optional statement
        if tag == 'clear':
            erin.schedule.clearSchedule()  # Clear the schedule
            erin.schedule.saveSchedule()  # Save cleared schedule
            erin.schedule.debugPreview()
        if tag == "end" or tag == "goodbye":
            break  # End the chat session
