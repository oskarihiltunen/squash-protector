from flask import current_app
from flask.ext.github import GitHubError
from sqlalchemy.exc import IntegrityError

from squash.extensions import celery, db, github
from squash.models import CommitStatus, Project


@celery.task
def check_commits(project_id, commits_url, commit_sha):
    project = Project.query.get(project_id)
    commit_status = CommitStatus(
        project_id=project_id,
        commit_sha=commit_sha,
        status='pending',
    )
    db.session.add(commit_status)
    try:
        db.session.commit()
    except IntegrityError:
        # Checking this commit has already started or been done.
        return
    try:
        _set_status(project, commit_sha, 'pending')
        commits = _fetch_commits(project, commits_url)
        status = _get_status(commits)
        commit_status.status = status
        db.session.commit()
        _set_status(project, commit_sha, status)
    except GitHubError as e:
        current_app.logger.error(e)


def _set_status(project, commit_sha, status):
    descriptions = {
        'success': 'All good!',
        'failure': 'There are squash! or fixup! commits in the pull request.',
    }
    data = {
        'context': 'squash! protector',
        'state': status,
    }
    if status in descriptions:
        data['description'] = descriptions[status]
    return github.post(
        'repos/{}/statuses/{}'.format(project.repo, commit_sha),
        data=data,
        access_token=project.access_token,
    )


def _fetch_commits(project, commits_url):
    return github.get(
        commits_url[len(github.base_url):],
        access_token=project.access_token,
    )


def _get_status(commits):
    messages = (
        commit['commit']['message']
        for commit in commits
    )
    has_squashes_or_fixups = any(
        message.startswith('squash! ') or
        message.startswith('fixup! ')
        for message in messages
    )
    if has_squashes_or_fixups:
        return 'failure'
    else:
        return 'success'
