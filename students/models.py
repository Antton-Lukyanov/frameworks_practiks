from django.db import models


class Student(models.Model):
    name = models.CharField("Имя", max_length=120)
    group = models.CharField("Группа", max_length=40)

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "студент"
        verbose_name_plural = "студенты"

    def __str__(self):
        return f"{self.name} ({self.group})"
