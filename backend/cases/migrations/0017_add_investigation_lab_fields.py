# Generated migration for adding lab value fields to Investigations model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0016_alter_studentnotes_case_and_more'),
    ]

    operations = [
        # Change white_cell_count from PositiveIntegerField to FloatField
        migrations.AlterField(
            model_name='investigations',
            name='white_cell_count',
            field=models.FloatField(blank=True, help_text='Bạch cầu (10^9/L)', null=True),
        ),
        # Add new lab value fields
        migrations.AddField(
            model_name='investigations',
            name='platelet_count',
            field=models.FloatField(blank=True, help_text='Tiểu cầu (10^9/L)', null=True),
        ),
        migrations.AddField(
            model_name='investigations',
            name='sodium_level',
            field=models.FloatField(blank=True, help_text='Natri (mmol/L)', null=True),
        ),
        migrations.AddField(
            model_name='investigations',
            name='potassium_level',
            field=models.FloatField(blank=True, help_text='Kali (mmol/L)', null=True),
        ),
        migrations.AddField(
            model_name='investigations',
            name='microbiology_results',
            field=models.TextField(blank=True, help_text='Kết quả vi sinh'),
        ),
        migrations.AddField(
            model_name='investigations',
            name='other_investigations',
            field=models.TextField(blank=True, help_text='Xét nghiệm khác'),
        ),
    ]
