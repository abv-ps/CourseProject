"""
Unit tests for task-related forms and serializers using pytest and pytest-django.

This module tests the following:
- TaskForm: Validations for required fields and due date.
- TaskSerializer: Ensures serializer validation for input data.
- TaskWithUserSerializer: Tests nested user data with tasks.

The tests verify form validation logic, serializer correctness,
and edge cases such as missing fields or invalid nested structures.
"""

from datetime import date, timedelta
import pytest
from django.contrib.auth.models import User
from .forms import TaskForm
from .serializers import (
    TaskSerializer,
    TaskWithUserSerializer,
)

pytestmark = pytest.mark.django_db


class TestTaskForm:
    """
    Tests for TaskForm including validation and required fields.
    """

    def test_form_valid(self) -> None:
        """
        Test valid data results in a valid form.
        """
        form = TaskForm(data={
            "title": "Test Task",
            "description": "Test Description",
            "due_date": date.today() + timedelta(days=1),
        })
        assert form.is_valid()

    def test_form_missing_required_fields(self) -> None:
        """
        Test form fails validation if required fields are missing.
        """
        form = TaskForm(data={})
        assert not form.is_valid()
        assert "title" in form.errors
        assert "due_date" in form.errors

    def test_form_due_date_in_past(self) -> None:
        """
        Test form fails if due date is in the past.
        """
        form = TaskForm(data={
            "title": "Past Task",
            "description": "Desc",
            "due_date": date.today() - timedelta(days=1),
        })
        assert not form.is_valid()
        assert "due_date" in form.errors


class TestTaskSerializer:
    """
    Tests for the TaskSerializer.
    """

    def test_serializer_valid(self) -> None:
        """
        Test valid data is accepted by the serializer.
        """
        user = User.objects.create_user(username="tester", password="pass")
        data = {
            "title": "Test Task",
            "description": "Testing write",
            "due_date": date.today() + timedelta(days=1),
            "user": user.id,
        }
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_serializer_missing_title(self) -> None:
        """
        Test missing title field results in serializer error.
        """
        serializer = TaskSerializer(data={
            "description": "No title",
            "due_date": date.today() + timedelta(days=1),
        })
        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_serializer_due_date_in_past(self) -> None:
        """
        Test due date in the past fails validation.
        """
        serializer = TaskSerializer(data={
            "title": "Old Task",
            "description": "Old",
            "due_date": date.today() - timedelta(days=1),
        })
        assert not serializer.is_valid()
        assert "due_date" in serializer.errors


class TestTaskWithUserSerializer:
    """
    Tests for nested TaskWithUserSerializer.
    """

    def test_nested_serializer_valid(self) -> None:
        """
        Test valid nested user data is accepted.
        """
        data = {
            "title": "Nested Task",
            "description": "Test with nested user",
            "due_date": date.today() + timedelta(days=1),
            "user": {
                "username": "tester",
                "email": "tester@example.com",
                "password": "pass1234"
            }
        }
        serializer = TaskWithUserSerializer(data=data)
        assert serializer.is_valid(), serializer.errors

    def test_nested_serializer_invalid_user(self) -> None:
        """
        Test invalid nested user data causes serializer to fail.
        """
        data = {
            "title": "Bad Nested",
            "description": "Invalid user data",
            "due_date": date.today() + timedelta(days=1),
            "user": {
                "username": "",
                "email": "not-an-email",
                "password": ""
            },
        }
        serializer = TaskWithUserSerializer(data=data)
        assert not serializer.is_valid()
        assert "user" in serializer.errors
