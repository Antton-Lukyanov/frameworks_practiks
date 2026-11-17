from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Task(models.Model):
    title = models.CharField("Название", max_length=200)
    max_score = models.PositiveSmallIntegerField(
        "Максимальный балл",
        default=100,
    )
    deadline = models.DateField("Срок сдачи")
    slug = models.SlugField(
        "URL-идентификатор",
        max_length=180,
        unique=True,
        editable=False,
    )

    class Meta:
        ordering = ["deadline", "id"]
        verbose_name = "задание"
        verbose_name_plural = "задания"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.title)) or "task"
            self.slug = base_slug[:160]
            if self.pk is not None:
                self.slug = f"{self.slug}-{self.pk}"

        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.slug and not self.slug.endswith(f"-{self.pk}"):
            self.slug = f"{self.slug}-{self.pk}"
            super().save(update_fields=("slug",))

    def get_absolute_url(self):
        return reverse("tasks:detail", kwargs={"slug": self.slug})
