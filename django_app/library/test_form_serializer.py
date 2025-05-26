"""
Unit tests for Task-related forms and serializers.

This module includes validation tests for:
- Django form `TaskForm`
- DRF serializers `TaskSerializer` and `TaskWithUserSerializer`

Tests cover field validation, missing or invalid data, and nested serialization.
"""
import os

import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from .forms import TaskForm
from .serializers import TaskSerializer, TaskWithUserSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')

def test_form_valid() -> None:
    """
    Test that a form with valid data is considered valid.
    """
    form = TaskForm(data={
        "title": "Test Task",
        "description": "Test Description",
        "due_date": date.today() + timedelta(days=1),
    })
    assert form.is_valid()


def test_form_missing_required_fields() -> None:
    """
    Test that the form is invalid when required fields are missing.
    """
    form = TaskForm(data={})
    assert not form.is_valid()
    assert "title" in form.errors
    assert "due_date" in form.errors


def test_form_due_date_in_past() -> None:
    """
    Test that the form is invalid if the due date is in the past.
    """
    form = TaskForm(data={
        "title": "Past Task",
        "description": "Desc",
        "due_date": date.today() - timedelta(days=1),
    })
    assert not form.is_valid()
    assert "due_date" in form.errors


def test_serializer_valid() -> None:
    """
    Test that the serializer accepts valid data.
    """
    serializer = TaskSerializer(data={
        "title": "Test Task",
        "description": "Testing",
        "due_date": date.today() + timedelta(days=1),
    })
    assert serializer.is_valid()


def test_serializer_missing_title() -> None:
    """
    Test that the serializer is invalid if the title is missing.
    """
    serializer = TaskSerializer(data={
        "description": "No title",
        "due_date": date.today() + timedelta(days=1),
    })
    assert not serializer.is_valid()
    assert "title" in serializer.errors


def test_serializer_due_date_in_past() -> None:
    """
    Test that the serializer is invalid if the due date is in the past.
    """
    serializer = TaskSerializer(data={
        "title": "Old Task",
        "description": "Old",
        "due_date": date.today() - timedelta(days=1),
    })
    assert not serializer.is_valid()
    assert "due_date" in serializer.errors


@pytest.mark.django_db
def test_nested_serializer_valid() -> None:
    """
    Test that the nested serializer is valid with a real user.
    """
    user = User.objects.create_user(username="tester", password="pass")
    data = {
        "title": "Test Nested",
        "description": "Nested Test",
        "due_date": date.today() + timedelta(days=1),
        "user": {"id": user.id, "username": user.username},
    }
    serializer = TaskWithUserSerializer(data=data)
    assert serializer.is_valid()


def test_nested_serializer_invalid_user() -> None:
    """
    Test that the nested serializer is invalid when user data is incorrect.
    """
    data = {
        "title": "Test Bad User",
        "description": "Bad",
        "due_date": date.today() + timedelta(days=1),
        "user": {"id": 999, "username": "ghost"},
    }
    serializer = TaskWithUserSerializer(data=data)
    assert not serializer.is_valid()
    assert "user" in serializer.errors
