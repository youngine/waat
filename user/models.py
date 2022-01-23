from django.db import models
from django.db.models.fields import CharField

class User_info(models.Model):
    user_id = CharField(max_length=30,primary_key = True)
    user_pw = CharField(max_length=30)
    user_name = CharField(max_length=30)
    user_email = CharField(max_length=30)

    class Meta:
        db_table = 'User'
        app_label = 'user'
        managed = False