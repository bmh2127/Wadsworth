from models import db, Task, preprocess_text, create_tfidf_vectorizer, create_task_completion_time_predictor, train_model, predict_completion_time
from views import app, analyze_progress
from config import config
import tensorflow as tf
import numpy as np
import os
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
def add_example_tasks(example_tasks):
    for task in example_tasks:
        new_task = Task(description=task['description'], category=task['category'],
                        completion_time=task['completion_time'])
        db.session.add(new_task)
    db.session.commit()


if __name__ == '__main__':
    app.config.from_object(config['development'])

    with app.app_context():
        # Create the database tables
        db.create_all()
        # Add example tasks
        example_tasks = [
            {'description': 'Write a blog post about productivity', 'category': 'writing', 'completion_time': 60},
            {'description': 'Clean the kitchen', 'category': 'housework', 'completion_time': 45},
            {'description': 'Finish reading a book', 'category': 'reading', 'completion_time': 120},
            # Add more example tasks here...
        ]
        add_example_tasks(example_tasks)

        # Train the TF-IDF vectorizer
        tasks = Task.query.all()
        tfidf_vectorizer = create_tfidf_vectorizer(tasks)
        # Set input_size and hidden_size
        input_size = len(tfidf_vectorizer.vocabulary_)
        hidden_size = 64

        # Create the model
        model = create_task_completion_time_predictor(input_size, hidden_size)

        # Prepare the training data and labels
        train_data = []
        train_labels = []
        for task in tasks:
            train_data.append(tfidf_vectorizer.transform([task.description]).toarray())
            train_labels.append(task.completion_time)
        train_data = np.vstack(train_data)
        train_labels = np.array(train_labels)

        # Train the model
        optimizer = tf.keras.optimizers.Adam(lr=0.001)
        num_epochs = 50
        train_model(model, train_data, train_labels, optimizer, num_epochs)
        # Save the model weights
        model.save_weights('model.h5')
        # Load the trained deep learning model
        model.load_weights('model.h5')

        # Run the analyze_progress() function and print the feedback
        feedback = analyze_progress()
        for item in feedback['feedback']:
            print(f"Task ID: {item['task_id']}")
            print(f"Message: {item['message']}")
            print()