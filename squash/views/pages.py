from flask import Blueprint, redirect, render_template, url_for

from squash.extensions import db, github
from squash.forms import RepoForm
from squash.services import project as project_service

blueprint = Blueprint('pages', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))


@blueprint.route('/select-repo/<token>', methods=['GET', 'POST'])
def select_repo(token):
    repos = github.get('user/repos', access_token=token)
    form = RepoForm.create(
        repos=[
            (repo['full_name'], repo['full_name'])
            for repo in repos
        ],
    )
    if form.validate():
        project_service.create(form.repo.data, token)
        db.session.commit()
        return 'Repo {} selected.'.format(form.repo.data)
    return render_template(
        'select_repo.html',
        form=form,
    )
