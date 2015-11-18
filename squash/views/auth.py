from flask import abort, Blueprint, redirect, url_for

from squash.extensions import github

blueprint = Blueprint('auth', __name__)


@blueprint.route('/login')
def login():
    # For public repos repo:status,write:repo_hook would be enough,
    # but with those permissions fetching the commits fails in private
    # repos.
    return github.authorize(scope='repo')


@blueprint.route('/github-callback')
@github.authorized_handler
def github_authorized(token):
    if token is None:
        # Auth failed.
        abort(400)

    return redirect(url_for('pages.select_repo', token=token))
