"""
Models for the Library API.

This module defines the data models used in the Library API. It includes:
- `Book`: Stores book information.
- `TokenUsage`: Tracks authentication token usage.
- `AuthorBookAction`: Logs actions related to authors and books.
- `Task`: Represents user-assigned tasks.
- `hash_token`: Utility function for hashing authentication tokens.
"""

import hashlib

from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Model representing a book in the library.
    """

    title: models.CharField = models.CharField(max_length=255)
    author: models.CharField = models.CharField(max_length=255)
    genre: models.CharField = models.CharField(max_length=100)
    publication_year: models.PositiveIntegerField = models.PositiveIntegerField()
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    updated_by: models.CharField = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        """
        Returns the title of the book as its string representation.

        Returns:
            str: The title of the book.
        """
        return str(self.title)


def hash_token(token: str) -> str:
    """
    Hashes a token using SHA-256.

    Args:
        token (str): The token to be hashed.

    Returns:
        str: The SHA-256 hashed token string.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class TokenUsage(models.Model):
    """
    Model representing the usage of an authentication token.
    """

    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    token_hash: models.CharField = models.CharField(max_length=64, unique=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    ip_address: models.GenericIPAddressField = models.GenericIPAddressField(
        null=True, blank=True
    )

    def __str__(self) -> str:
        """
        Returns a string representation of the token usage.

        Returns:
            str: A string containing the username and hashed token.
        """
        return f"{self.user.username} - {self.token_hash}"


class AuthorBookAction(models.Model):
    """
    Model for tracking author and book actions (created/updated) for auditing/logging.
    """

    ACTION_CHOICES = [
        ("author_created", "Author Created"),
        ("author_updated", "Author Updated"),
        ("book_created", "Book Created"),
        ("book_updated", "Book Updated"),
    ]

    author_id: models.IntegerField = models.IntegerField(null=True, blank=True)
    author_name: models.CharField = models.CharField(max_length=255, null=True, blank=True)
    book_id: models.IntegerField = models.IntegerField(null=True, blank=True)
    book_title: models.CharField = models.CharField(max_length=255, null=True, blank=True)
    action: models.CharField = models.CharField(max_length=50, choices=ACTION_CHOICES)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Returns a readable summary of the action.

        Returns:
            str: Description of the action.
        """
        return f"{self.action} | Author: {self.author_name or '-'} | Book: {self.book_title or '-'}"


class Task(models.Model):
    """
    Model representing a task assigned to a user.
    """

    title: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(blank=True)
    due_date: models.DateField = models.DateField()
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self) -> str:
        """
        Returns the title of the task as its string representation.

        Returns:
            str: The task title.
        """
        return self.title
