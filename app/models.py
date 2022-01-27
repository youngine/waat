from enum import auto
from django.db import models
from django.db.models.fields import CharField, IntegerField,DateField,TextField

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
        app_label = 'app'
        managed = False
