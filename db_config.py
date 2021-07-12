from peewee import (BooleanField, CharField, DateTimeField, FloatField,
                    IntegerField, Model, SqliteDatabase)

user_db = SqliteDatabase("UserData.db")
articles_db = SqliteDatabase("ArticlesData.db")

class UserData(Model):
    uid = IntegerField(primary_key=True)
    uslug = CharField()
    user_url = CharField()
    name = CharField()
    gender = CharField()
    badges = CharField()
    avatar_url = CharField()
    background_image_url = CharField()
    followings_count = IntegerField()
    fans_count = IntegerField()
    total_wordage = IntegerField()
    total_likes_count = IntegerField()
    FP_count = FloatField()
    FTN_count = FloatField()
    last_update_time = DateTimeField()
    introduction_text = CharField()
    
    class Meta:
        database = user_db

class ArticlesData(Model):
    aid = IntegerField(primary_key=True)
    aslug = CharField()
    title = CharField()
    wordage = IntegerField()
    FP_count = FloatField()
    likes_count = IntegerField()
    comments_count = IntegerField()
    most_valuable_comments_count = IntegerField()
    paid_type = CharField()
    nid = IntegerField()
    commentable = BooleanField()
    reprintable = BooleanField()
    publish_time = DateTimeField()
    update_time = DateTimeField()
    description = CharField()
    
    class Meta:
        database = articles_db
        