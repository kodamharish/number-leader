# Generated by Django 5.0.6 on 2024-07-17 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflow',
            name='begin_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='cashflow',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='cashflow',
            name='modified_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='modified_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
