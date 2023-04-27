from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reference.models import Reference, ReferenceVersion, ReferenceElement


class RefbookElementsViewTestCase(APITestCase):

    def setUp(self):
        start_date = date(2022, 1, 1)
        self.refbook = Reference.objects.create(name='Test Refbook')
        self.version = ReferenceVersion.objects.create(
            reference=self.refbook,
            version='1.0',
            start_date=start_date
        )
        ReferenceElement.objects.create(
            version=self.version,
            code='CODE1',
            value='value_1',
        )
        ReferenceElement.objects.create(
            version=self.version,
            code='CODE2',
            value='value_2',
        )
        ReferenceElement.objects.create(
            version=self.version,
            code='CODE3',
            value='value_3',
        )

    def test_get_refbook_elements_without_version(self):
        """
        Test GET request to RefbookElementsView without version parameter
        """
        url = reverse('refbook_elements_list', kwargs={'id': self.refbook.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 3)

    def test_get_refbook_elements_with_valid_version(self):
        """
        Test GET request to RefbookElementsView with valid version parameter
        """
        url = reverse('refbook_elements_list', kwargs={'id': self.refbook.id})
        response = self.client.get(url, {'version': '1.0'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 3)

    def test_get_refbook_elements_with_nonexistent_refbook(self):
        """
        Test GET request to RefbookElementsView with nonexistent refbook id
        """
        url = reverse('refbook_elements_list', kwargs={'id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
