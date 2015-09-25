import os
import subprocess

from flask.ext.script import Manager

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATABASE_DUMP_FILENAME = os.path.join(PROJECT_ROOT, 'dump.sql')

manager = Manager()


@manager.command
def create():
    """Create the database."""
    from squash.extensions import db
    return subprocess.call(['createdb', db.engine.url.database])


@manager.command
def migrate():
    """Run database migrations."""
    return subprocess.call(['alembic', 'upgrade', 'head'], cwd=PROJECT_ROOT)


@manager.command
def kill_connections():
    from squash.extensions import db
    query = '''
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '{}'
    '''.format(db.engine.url.database)
    return subprocess.call([
        'psql',
        '--command', query
    ])


@manager.command
def drop():
    """Drop the database."""
    from squash.extensions import db
    return (
        kill_connections() or
        subprocess.call(['dropdb', '--if-exists', db.engine.url.database])
    )


@manager.command
def reset():
    """Re-create database, run migrations and restore data from dump."""
    return drop() or create() or migrate() or restore()


@manager.command
def dump():
    """Dump database data to a file."""
    args = [
        'pg_dump',
        '--data-only',
        '--no-owner',
        '--exclude-table', 'alembic_version',
        '--file', DATABASE_DUMP_FILENAME,
    ] + _get_pg_args_from_database_url()
    return subprocess.call(args)


@manager.command
def restore():
    """Restore data from database dump."""
    args = [
        'psql',
        '--file', DATABASE_DUMP_FILENAME,
    ] + _get_pg_args_from_database_url()
    return subprocess.call(args)


def _get_pg_args_from_database_url():
    from squash.extensions import db
    args = [
        '--dbname', db.engine.url.database,
        '--host', db.engine.url.host,
    ]
    if db.engine.url.port:
        args += ['--port', str(db.engine.url.port)]
    if db.engine.url.username:
        args += ['--username', db.engine.url.username]
    return args
