from django.db import models
from django.db.models.fields import CharField, IntegerField,DateField,TextField
from django.contrib.auth.models import User

class User_info(models.Model):
    user_id = CharField(max_length=30,primary_key = True)
    user_pw = CharField(max_length=30)
    user_name = CharField(max_length=30)
    user_email = CharField(max_length=30)

    def __str__(self):
        return self.user_name
        
    class Meta:
        db_table = 'User'
        app_label = 'user'
        managed = False

class FundingBoard(models.Model):

    board_id = IntegerField(primary_key=True)
    user_id = CharField(max_length=30)

    title = CharField(max_length=255, null=True)
    category = CharField(max_length=30, null=True)
    language_text = CharField(max_length=30, null=True)
    target = CharField(max_length=30, null=True)
    intro = TextField(null=True)
    file_name = TextField()
    background_text = TextField()
    object_text = TextField()
    develop_content = TextField()
    func_text = TextField()
    func_a_price = IntegerField()
    func_b_price = IntegerField()
    func_c_price = IntegerField()
    fund_goal_price = IntegerField()
    fund_total_price = IntegerField()
    regi_date = DateField()
    start_date = DateField()
    end_date = DateField()
    front_crew = IntegerField()
    back_crew = IntegerField()

    
    class Meta:
        db_table = 'FundingBoard'
        app_label = 'user'
        managed = False





class JoinFund(models.Model):
    id = IntegerField(primary_key=True, auto_created=True)
    user_id = CharField(max_length=30)
    board_id = IntegerField()
    fund_price = IntegerField()
    fund_join_list = CharField(max_length=30)


    
    class Meta:
        db_table = 'JoinFund'
        app_label = 'user'
        managed = False


class JoinProject(models.Model):
    id = IntegerField(primary_key=True, auto_created=True)
    user_id = CharField(max_length=30)
    board_id = IntegerField()
    user_name = CharField(max_length=30)
    user_email = CharField(max_length=50)
    subject = CharField(max_length=255)
    message = TextField()
    check_crew = IntegerField()

    
    class Meta:
        db_table = 'JoinProject'
        app_label = 'user'
        managed = False