# Generated manually for issue/return tracking feature

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_labitem_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="ItemIssue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("student_name", models.CharField(max_length=120)),
                ("taken_at", models.DateTimeField(auto_now_add=True)),
                ("returned_at", models.DateTimeField(blank=True, null=True)),
                (
                    "item",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="issues", to="inventory.labitem"),
                ),
            ],
            options={"ordering": ["-taken_at"]},
        ),
    ]
