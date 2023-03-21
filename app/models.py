from flask_sqlalchemy import SQLAlchemy
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import string

db = SQLAlchemy()

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())

    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens

def create_tfidf_vectorizer(tasks):
    vectorizer = TfidfVectorizer()
    task_descriptions = [task.description for task in tasks]
    vectorizer.fit(task_descriptions)
    return vectorizer


# SQLAlchemy data model for tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    completion_time = db.Column(db.Float, nullable=False)

    def __init__(self, description, category, completion_time):
        self.description = description
        self.category = category
        self.completion_time = completion_time

# PyTorch deep learning model for task completion time prediction
def create_task_completion_time_predictor(input_size, hidden_size):
    model = Sequential()
    model.add(Dense(hidden_size, input_dim=input_size, activation='relu'))
    model.add(Dense(hidden_size, activation='relu'))
    model.add(Dense(1, activation='linear'))
    return model

def train_model(model, train_data, train_labels, optimizer, num_epochs):
    model.compile(optimizer=optimizer, loss='mse')
    model.fit(train_data, train_labels, epochs=num_epochs)

def predict_completion_time(model, inputs):
    outputs = model(inputs, training=False)
    return outputs.numpy().item()
