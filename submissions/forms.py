"""Forms for filtering and managing assignment submissions."""

from django import forms
from django.utils import timezone

from .models import Submission


class SubmissionFilterForm(forms.Form):
    """Validated GET filters for the submissions list."""

    STATUS_CHOICES = (
        ("", "Все"),
        ("active", "Активные"),
        ("cancelled", "Отменённые"),
    )
    ORDER_CHOICES = (
        ("date", "Сначала новые"),
        ("date_asc", "Сначала старые"),
        ("score", "По баллам"),
        ("student", "По студенту"),
        ("task", "По заданию"),
    )

    q = forms.CharField(
        label="Поиск",
        required=False,
        max_length=100,
        widget=forms.SearchInput(attrs={"class": "form-control"}),
    )
    status = forms.ChoiceField(
        label="Статус",
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    order = forms.ChoiceField(
        label="Сортировка",
        required=False,
        choices=ORDER_CHOICES,
        initial="date",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class SubmissionForm(forms.ModelForm):
    """Create or edit a submission with server-side business validation."""

    class Meta:
        model = Submission
        fields = (
            "student",
            "task",
            "file_name",
            "file_size_mb",
            "score",
            "submission_date",
        )
        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "task": forms.Select(attrs={"class": "form-select"}),
            "file_name": forms.TextInput(attrs={"class": "form-control"}),
            "file_size_mb": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "step": "0.01"}
            ),
            "score": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "step": "1"}
            ),
            "submission_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def clean_submission_date(self):
        submission_date = self.cleaned_data["submission_date"]
        if submission_date > timezone.localdate():
            raise forms.ValidationError("Дата сдачи не может быть в будущем.")
        return submission_date

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get("task")
        score = cleaned_data.get("score")
        student = cleaned_data.get("student")

        if task and score is not None and score > task.max_score:
            self.add_error(
                "score",
                f"Максимальный балл за задание — {task.max_score}.",
            )

        if task and student:
            duplicates = Submission.objects.filter(
                student=student,
                task=task,
                is_cancelled=False,
            )
            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                raise forms.ValidationError(
                    "У этого студента уже есть активная сдача данного задания."
                )
        return cleaned_data
