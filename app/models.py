from app import db
from datetime import datetime
import re
import random

from flask_security import UserMixin, RoleMixin


post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


def func_slugify(s):
    return s.lower()
    # pattern = r'[^\w+]'
    # slug = re.sub(pattern, '-', s)
    # return slug

    # return s
    # return re.sub(pattern, '-', s.lower())
    # другая реализация логики:
    # return '{0}-{1}'.format(
    #     re.sub(pattern, '-', s.lower()),
    #     str(random.randrange(1, 17))
    # )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    tBody = db.Column(db.Text)
    dCreated = db.Column(db.DateTime, default=datetime.now())

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
            self.slug = func_slugify(self.title)

            # if self.dCreated:
            #     self.slug = func_slugify(self.title.lower()) + '-' + func_slugify(str(self.dCreated))

    def __repr__(self):
        return '{}'.format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    slug = db.Column(db.String(140))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = func_slugify(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


# для flask-security

roles_users = db.Table(
    'roles_users',
    db.Column('id_user', db.Integer(), db.ForeignKey('user.id')),
    db.Column('id_role', db.Integer(), db.ForeignKey('role.id'))
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(140))
    date_create = db.Column(db.DateTime, default=datetime.now())
    active = db.Column(db.Boolean())

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
        )


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
