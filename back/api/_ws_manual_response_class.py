import json
from flask import Flask, Response, abort, request, g
from .utils import JSON_MIME_TYPE, search_workshop, send_email, json_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#workshops = [{
#    'id': 33,
#    'title': 'The Raven',
#    'author_id': 1
#}]

workshops = [{
    'id': 10,
    'type': 'Design Thinking',
    'itemsPerParticipant': [
      {
        'name': 'Postit 20x10',
        'quantity': 10
      },
      {
        'name': 'Whiteboard marker (Black)',
        'quantity': 1
      },
      {
        'name': 'Whiteboard marker (Blue)',
        'quantity': 1
      }
    ],
    'commonItems': [
      {
        'name': 'Whiteboard eraser',
        'quantity': 1
      },
      {
        'name': 'Magnets',
        'quantity': 10
      }
    ]
  },
  {
    'id': 20,
    'type': 'Traditional brainstorming',
    'itemsPerParticipant': [
      {
        'name': 'Postit 20x10',
        'quantity': 10
      },
      {
        'name': 'Whiteboard marker (Black)',
        'quantity': 1
      },
      {
        'name': 'Whiteboard marker (Blue)',
        'quantity': 1
      }
    ],
    'commonItems': [
      {
        'name': 'Whiteboard eraser',
        'quantity': 1
      },
      {
        'name': 'Magnets',
        'quantity': 10
      }
    ]
  }
]

@app.route('/workshops')
def workshop_list():
    response = Response(
        json.dumps(workshops), status=200, mimetype=JSON_MIME_TYPE)
    return response


@app.route('/workshops/<int:workshop_id>')
def book_detail(workshop_id):
    workshop = search_workshop(workshops, workshop_id)
    if workshop is None:
        abort(404)

    content = json.dumps(workshop)
    return content, 200, {'Content-Type': JSON_MIME_TYPE}

@app.route('/workshops', methods=['POST'])
def workshop_create():
    if request.content_type != JSON_MIME_TYPE:
        error = json.dumps({'error': 'Invalid Content Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('workshopName'), data.get('type')]):
        error = json.dumps({'error': 'Missing field/s (workshopName, type)'})
        return json_response(error, 400)

    send_email("accounts@oddeven.ch", json.dumps(data))

#    query = ('INSERT INTO workshops ("author_id", "title") '
#             'VALUES (:author_id, :title);')
#    params = {
#        'title': data['title'],
#        'author_id': data['author_id']
#    }
#    g.db.execute(query, params)
#    g.db.commit()

    return json_response(status=201)

@app.errorhandler(404)
def not_found(e):
    return '', 404
