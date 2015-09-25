from flask_wtf import Form
from wtforms import SelectField


class RepoForm(Form):
    repo = SelectField('Repository')

    @staticmethod
    def create(repos):
        form = RepoForm()
        form.repo.choices = repos
        return form
