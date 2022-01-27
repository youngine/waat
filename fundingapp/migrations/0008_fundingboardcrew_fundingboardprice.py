
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundingapp', '0007_joinproject'),
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
    ]
