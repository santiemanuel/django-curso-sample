# Generated by Django 4.2.6 on 2023-12-05 18:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0003_curso_contenido_curso_metodologia_curso_objetivos"),
    ]

    operations = [
        migrations.AddField(
            model_name="estudiante",
            name="facebook",
            field=models.URLField(blank=True, null=True, verbose_name="Facebook"),
        ),
        migrations.AddField(
            model_name="estudiante",
            name="habilidades",
            field=models.TextField(blank=True, null=True, verbose_name="Habilidades"),
        ),
        migrations.AddField(
            model_name="estudiante",
            name="nivel_educativo",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SEC", "Secundaria"),
                    ("PRE", "Pregrado"),
                    ("POS", "Posgrado"),
                    ("OTR", "Otro"),
                ],
                default="SEC",
                max_length=3,
                null=True,
                verbose_name="Nivel Educativo",
            ),
        ),
    ]