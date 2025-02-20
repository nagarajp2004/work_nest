from django import forms
from .models import Task
from datetime import date, timedelta,datetime

class TaskForm(forms.ModelForm):
    due_in_days = forms.IntegerField(
        required=True,
        min_value=1,
        label="Number of days from today"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'priority', 'status']  # Removed 'due_date'

    def clean_due_in_days(self):
        days = self.cleaned_data.get('due_in_days')
        if days < 1:
            raise forms.ValidationError("Number of days must be greater than 0")
        return days

    def save(self, commit=True):
        instance = super().save(commit=False)
        due_in_days = self.cleaned_data.get("due_in_days")

        # Set due_date dynamically based on today's date
        instance.due_date = date.today() + timedelta(days=due_in_days)


        if commit:
            instance.save()

        return instance
