from django.db import migrations, models
import django.db.models.deletion
from tuli import settings

from tuli.models import image_file_upload

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lookup', models.CharField(db_index=True, max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tuli.Image')),
                ('file', models.ImageField(upload_to=image_file_upload, height_field="height", width_field="width")),
                ('height', models.PositiveSmallIntegerField()),
                ('width', models.PositiveSmallIntegerField()),
            ],
            options={
                'get_latest_by': ('image', '-width', '-height'),
            },
        ),
    ]
