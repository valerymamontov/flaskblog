from app import db
from datetime import datetime
import re
import random


def func_slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s.lower())
    # другая реализация логики:
    # return '{0}-{1}'.format(
    #     re.sub(pattern, '-', s.lower()),
    #     str(random.randrange(1, 17))
    # )

post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    tBody = db.Column(db.Text)
    dCreated = db.Column(db.DateTime, default=datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))

    tags = db.relationship(
        'Tag',
        secondary=post_tag,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.func_generate_slug()

    def func_generate_slug(self):
        if self.title:
            if self.dCreated:
                self.slug = func_slugify(self.title) + '-' + func_slugify(str(self.dCreated))

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    slug = db.Column(db.String(140))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = func_slugify(self.name)

    def __repr__(self):
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)
