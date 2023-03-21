from flask import Flask, render_template, request, jsonify
from config import config
from models import db, Task, create_task_completion_time_predictor, preprocess_text, predict_completion_time
import json

app = Flask(__name__)
app.config.from_object(config['development'])
db.init_app(app)

# ... (other routes)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_data = request.get_json()
    description = task_data['description']
    category = task_data['category']

    # Preprocess task description
    processed_description = preprocess_text(description)

    # Save the task to the database
    new_task = Task(description=description, category=category, completion_time=-1)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task added successfully"})

@app.route('/update_task', methods=['POST'])
def update_task():
    task_data = request.get_json()
    task_id = task_data['id']
    completion_time = task_data['completion_time']

    task = Task.query.get(task_id)
    task.completion_time = completion_time
    db.session.commit()

    return jsonify({"message": "Task updated successfully"})

@app.route('/analyze_progress', methods=['GET'])
def analyze_progress():
    # Load the trained deep learning model
    model = create_task_completion_time_predictor(input_size, hidden_size)
    model.load_weights('model.h5')

    # Analyze tasks and provide insights
    tasks = Task.query.all()
    feedback = []

    for task in tasks:
        processed_description = preprocess_text(task.description)

        # Convert the processed_description to a feature vector using TF-IDF
        feature_vector = tfidf_vectorizer.transform([' '.join(processed_description)]).toarray()

        inputs = tf.convert_to_tensor(feature_vector, dtype=tf.float32)
        predicted_completion_time = predict_completion_time(model, inputs)

        # Provide feedback based on the model's insights
        if task.completion_time > predicted_completion_time:
            feedback.append({
                'task_id': task.id,
                'message': "Consider breaking this task into smaller tasks to improve productivity."
            })

    return jsonify({"feedback": feedback})

# ... (rest of your app setup)

if __name__ == '__main__':
    app.run()
