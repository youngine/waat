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
    file_name = CharField(max_length=30, null=True)
    background_text = CharField(max_length=200, null=True)
    object_text = CharField(max_length = 200, null=True)
    develop_content = CharField(max_length=200, null=True)
    func_a_price = IntegerField()
    func_b_price = IntegerField()
    func_c_price = IntegerField()
    fund_goal_price = IntegerField()
    fund_total_price = IntegerField()
    regi_date = DateField()
    start_date = DateField()
    end_date = DateField()

    
    class Meta:
        db_table = 'FundingBoard'
        app_label = 'app'
        managed = False
