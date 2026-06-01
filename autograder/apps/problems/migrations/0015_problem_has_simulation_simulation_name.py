# Adds simulation flag + name to Problem so SvelteKit frontend can dynamically mount
# interactive svelte simulation components.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0014_remove_problem_interactor_file_alter_problem_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='has_simulation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='problem',
            name='simulation_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
