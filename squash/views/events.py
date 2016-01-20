from flask import abort, Blueprint, current_app, request

from squash.models import Project
from squash.tasks import check_commits

blueprint = Blueprint('events', __name__)


def validate_request(request):
    event = request.headers.get('X-GitHub-Event')
    if event not in ('pull_request', 'ping'):
        current_app.logger.warning('Incorrect X-GitHub-Event %r', event)
        abort(400)
    content_type = request.content_type
    if content_type != 'application/json':
        current_app.logger.warning('Incorrect Content-Type %r', content_type)
        abort(400)


def get_data(request):
    json = request.get_json(silent=True)
    if json is None:
        current_app.logger.warning('Invalid data %r', request.data)
        abort(400)
    try:
        return {
            'action': json['action'],
            'commits_url': json['pull_request']['commits_url'],
            'commit_sha': json['pull_request']['head']['sha'],
        }
    except KeyError:
        current_app.logger.warning('Invalid data %r', json)
        abort(400)


def handle_pull_request(project, request):
    data = get_data(request)
    if data.pop('action') in ('opened', 'synchronize'):
        check_commits.delay(project.id, **data)
        return '', 202
    return '', 204


def handle_ping(project, request):
    return '', 204


def handle_request(project, request):
    handlers = {
        'pull_request': handle_pull_request,
        'ping': handle_ping,
    }
    event = request.headers['X-GitHub-Event']
    return handlers[event](project, request)


@blueprint.route('/<project_id>', methods=['POST'])
def receive(project_id):
    project = Project.query.get(project_id)
    if not project:
        current_app.logger.warning('Unknown project %r', project_id)
        abort(404)
    validate_request(request)
    return handle_request(project, request)


@blueprint.route('/keep-alive')
def keep_alive():
    count = Project.query.count()
    return str(count), 200
