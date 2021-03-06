
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingBoardCrew',
            fields=[
                ('board_id', models.IntegerField(primary_key=True, serialize=False)),
                ('front_crew', models.IntegerField()),
                ('back_crew', models.IntegerField()),
            ],
            options={
                'db_table': 'FundingBoardCrew',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FundingBoardPrice',
            fields=[
                ('board_id', models.IntegerField(primary_key=True, serialize=False)),
                ('func_a_price', models.IntegerField()),
                ('func_b_price', models.IntegerField()),
                ('func_c_price', models.IntegerField()),
                ('fund_goal_price', models.IntegerField()),
                ('fund_total_price', models.IntegerField()),
            ],
            options={
                'db_table': 'FundingBoardPrice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JoinFund',
            fields=[
                ('jf_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=30)),
                ('board_id', models.IntegerField()),
                ('fund_price', models.IntegerField()),
                ('fund_join_list', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'JoinFund',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JoinProject',
            fields=[
                ('jp_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=30)),
                ('board_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=30)),
                ('user_email', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('check_crew', models.IntegerField()),
            ],
            options={
                'db_table': 'JoinProject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User1',
            fields=[
                ('user_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('user_pw', models.CharField(max_length=30)),
                ('user_name', models.CharField(max_length=30)),
                ('user_email', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'User',
                'managed': False,
            },
        ),
    ]
