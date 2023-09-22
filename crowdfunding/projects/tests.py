from django.test import TestCase
import json
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from .models import Project, Pledge

@pytest.mark.django_db
def test_create_pledge_authenticated(api_client, user, project):
    """
    Test creating a pledge by an authenticated user for an open project.
    """
    api_client.force_authenticate(user=user)
    pledge_data = {
        "amount": 100,
        "comment": "Test Pledge",
        "anonymous": False,
        "project": project.pk,
    }
    response = api_client.post(reverse("pledge-list"), pledge_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Pledge.objects.count() == 1
    assert Pledge.objects.first().supporter == user
    assert Pledge.objects.first().is_deleted is False