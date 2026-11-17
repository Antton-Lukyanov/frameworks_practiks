from django.db import models


class Task(models.Model):
    title = models.CharField("Название", max_length=200)
    max_score = models.PositiveSmallIntegerField(
        "Максимальный балл",
        default=100,
    )
    deadline = models.DateField("Срок сдачи")

    class Meta:
        ordering = ["deadline", "id"]
        verbose_name = "задание"
        verbose_name_plural = "задания"

    def __str__(self):
        return self.title
