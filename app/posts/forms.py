from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Название поста:')
    body = TextAreaField('Содержание:')
