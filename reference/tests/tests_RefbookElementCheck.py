from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reference.models import Reference, ReferenceVersion, ReferenceElement


class RefbookElementCheckViewTestCase(APITestCase):
    def setUp(self):
        start_date = date(2022, 1, 1)
        self.refbook = Reference.objects.create(name="Test Reference")
        self.version = ReferenceVersion.objects.create(reference=self.refbook,
                                                       version="1.0",
                                                       start_date=start_date)
        self.element = ReferenceElement.objects.create(version=self.version,
                                                       code="TEST_CODE",
                                                       value="Test Value")

    def test_check_element_exists(self):
        url = reverse("check_refbook_element", args=[self.refbook.id])
        data = {"code": "TEST_CODE", "value": "Test Value", "version": "1.0"}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["exists"], True)

    def test_check_element_does_not_exist(self):
        url = reverse("check_refbook_element", args=[self.refbook.id])
        data = {"code": "OTHER_CODE", "value": "Other Value", "version": "1.0"}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["exists"], False)

    def test_check_element_no_version(self):
        url = reverse("check_refbook_element", args=[self.refbook.id])
        data = {"code": "TEST_CODE", "value": "Test Value"}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["exists"], True)

    def test_check_element_no_current_version(self):
        self.version.delete()
        url = reverse("check_refbook_element", args=[self.refbook.id])
        data = {"code": "TEST_CODE", "value": "Test Value"}
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "No current version found")
