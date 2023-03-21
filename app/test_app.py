from models import db, Task, preprocess_text, create_tfidf_vectorizer
from views import analyze_progress
from app import app


def add_example_tasks(example_tasks):
    for task in example_tasks:
        new_task = Task(description=task['description'], category=task['category'],
                        completion_time=task['completion_time'])
        db.session.add(new_task)
    db.session.commit()


if __name__ == '__main__':
    app.config.from_object(config['development'])
    db.init_app(app)

    with app.app_context():
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

        # Run the analyze_progress() function and print the feedback
        feedback = analyze_progress()
        for item in feedback['feedback']:
            print(f"Task ID: {item['task_id']}")
            print(f"Message: {item['message']}")
            print()