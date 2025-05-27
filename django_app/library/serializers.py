"""
Serializers for the task and book management application.

This module contains serializers for the following models:
- Book: Used to represent books owned by users.
- Task: Used to represent user tasks, including due date validation.
- User: Used for user creation with password handling.
It includes both writable and read-only representations for nested user data.

Serializers:
- BookSerializer: Read-only user field, all fields included.
- UserSerializer: Write-only password field, used for user creation.
- TaskSerializer: Basic serializer for task creation and validation.
- TaskWithUserSerializer: Handles nested user data creation and validation.
"""

from typing import Any
from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Task


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Includes the username of the related user as a read-only field.
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Book
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    The password is write-only and used during user creation.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data: dict[str, Any]) -> User:
        """
        Creates a new user instance with the provided validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating tasks.
    Validates that the due date is not in the past.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'user']

    def validate_due_date(self, value: date) -> date:
        """
        Ensure the due date is today or in the future.
        """
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class TaskWithUserSerializer(serializers.ModelSerializer):
    """
    Nested serializer for tasks with embedded user data.
    Validates the due date to ensure it's not in the past.
    """
    user = UserSerializer()

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'user']

    def validate_due_date(self, value: date) -> date:
        """
        Ensure the due date is today or in the future.
        """
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
