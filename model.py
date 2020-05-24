from peewee import SqliteDatabase, Model, TextField, ForeignKeyField

db = SqliteDatabase(
    "blog.db",
    pragmas={
        "journal_mode": "wal",
        "cache_size": -1 * 64000,
        "foreign_keys": 1,
        "ignore_check_constraints": 0,
        "synchronous": 0,
    },
)


class User(Model):
    username = TextField(unique=True, null=False)
    password = TextField(null=False)
    about_me = TextField(null=True)

    class Meta:
        database = db
        table_name = "users"


class Post(Model):
    title = TextField(null=False)
    text = TextField(null=True)
    user_id = ForeignKeyField(User, backref="posts", null=True)
    date_posted = TextField(null=False)

    class Meta:
        database = db
        table_name = "posts"


db.connect()
db.create_tables([User, Post])
db.close()
