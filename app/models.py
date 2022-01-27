from ast import In
from enum import auto
from django.db import models
from django.db.models.fields import CharField, IntegerField, DateField, TextField

label_name = 'app'
class User1(models.Model):

    user_id = CharField(max_length=30, primary_key=True)
    user_pw = CharField(max_length=30)
    user_name = CharField(max_length = 30)
    user_email = CharField(max_length=30)

    class Meta:
        db_table = 'User'
        app_label = label_name
        managed = False


class FundingBoard(models.Model):

    board_id = IntegerField(primary_key=True)
    user_id = CharField(max_length=30)
    title = CharField(max_length=255, null=True)
    category = CharField(max_length=30, null=True)
    language_text = CharField(max_length=30, null=True)
    target = CharField(max_length=30, null=True)
    intro = TextField()
    file_name = TextField()
    background_text = TextField()
    object_text = TextField()
    develop_content = TextField()
    func_text = TextField()
    regi_date = DateField()
    start_date = DateField()
    end_date = DateField()




    
    class Meta:
        db_table = 'FundingBoard'
        app_label = label_name
        managed = False

# 펀딩 게시물에서 가격 관련 DB
class FundingBoardPrice(models.Model):

    # FundingBoard Forign key, primary key
    board_id = IntegerField(primary_key = True)

    # func_'a~c'_price : A~C 기능 가격
    # fund_goal_price : 펀딩 목표 가격
    # fund_total_price : 펀딩으로 모인 금액
    func_a_price = IntegerField()
    func_b_price = IntegerField()
    func_c_price = IntegerField()
    fund_goal_price = IntegerField()
    fund_total_price = IntegerField()

    class Meta:
        db_table = 'FundingBoardPrice'
        app_label = label_name
        managed = False


# 펀딩 참여 DB
class JoinFund(models.Model):

    # auto increse id 값, primary key
    jf_id = IntegerField(primary_key=True, auto_created=True)

    # user_id : User Forign key
    # board_id : FundingBoard Forign key
    user_id = CharField(max_length=30)
    board_id = IntegerField()

    # fund_price : 펀딩 참여한 금액
    # fund_join_list : 펀딩 선택 값
    fund_price = IntegerField()
    fund_join_list = CharField(max_length=40)

    class Meta:
        db_table = 'JoinFund'
        app_label = label_name
        managed = False

# 펀딩 게시물에서 원하는 크루 인원
class FundingBoardCrew(models.Model):

    # FundingBoard Forign key, primary key
    board_id = IntegerField(primary_key=True)

    # front_crew : 구하는 프론트앤드 팀원 수
    # back_crew : 구하는 백엔드 팀원 수
    front_crew = IntegerField()
    back_crew = IntegerField()

    class Meta:
        db_table = 'FundingBoardCrew'
        app_label = label_name
        managed = False

# 팀원 모집 DB
class JoinProject(models.Model):
    
    # primary key
    jp_id = IntegerField(primary_key=True, auto_created=True)

    # user_id : User Forign key
    # board_id : FundingBoard Forign key
    user_id = CharField(max_length=30)
    board_id = IntegerField()

    # user_name : 유저 이름
    # back_crew : 구하는 백엔드 팀원 수   
    user_name = CharField(max_length=30)
    user_email = CharField(max_length=50)
    subject = CharField(max_length=255)
    message = TextField()
    check_crew = IntegerField()


    
    class Meta:
        db_table = 'JoinProject'
        app_label = label_name
        managed = False