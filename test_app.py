import pytest
from app import app, db, Todo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_add_task(client):
    response = client.post('/', data={'content': 'Test Task'})
    assert response.status_code == 302  # redirect

    # check if task exists in DB
    with app.app_context():
        task = Todo.query.first()
        assert task.content == 'Test Task'


def test_delete_task(client):
    # create task
    client.post('/', data={'content': 'Delete Me'})

    with app.app_context():
        task = Todo.query.first()

    response = client.get(f'/delete/{task.id}')
    assert response.status_code == 302

    # check if deleted
    with app.app_context():
        task = Todo.query.first()
        assert task is None


def test_update_task(client):
    # create task
    client.post('/', data={'content': 'Old Task'})

    with app.app_context():
        task = Todo.query.first()

    response = client.post(f'/update/{task.id}', data={'content': 'New Task'})
    assert response.status_code == 302

    # check update
    with app.app_context():
        updated_task = Todo.query.first()
        assert updated_task.content == 'New Task'