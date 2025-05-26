"""
Contains a Django form for the Task model.

This module defines the TaskForm, which includes validation to ensure the
due date is not set in the past.
"""
from datetime import date
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    A Django form for creating and updating Task instances.

    Includes validation to ensure the due date is not in the past.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

    def clean_due_date(self) -> date:
        """
        Validates that the due_date is not in the past.

        Returns:
            date: The cleaned due date.

        Raises:
            forms.ValidationError: If the due date is earlier than today.
        """
        due_date = self.cleaned_data['due_date']
        if due_date < date.today():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date