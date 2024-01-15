from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_list = [
        {
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        } for message in messages
    ]
    return jsonify(messages_list)

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.get(id)
    returned_message = {
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at,
            'updated_at': message.updated_at
    }
    return returned_message

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message created successfully'})

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'}), 404
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify({'message': 'Message updated successfully'})

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'message': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'})


if __name__ == '__main__':
    app.run(port=5555)
