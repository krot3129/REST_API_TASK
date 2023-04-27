from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reference.models import Reference, ReferenceVersion


class RefBookListTests(APITestCase):

    def setUp(self):
        self.ref1 = Reference.objects.create(code='ref1', name='Reference 1', description='Reference 1 description')
        self.ref2 = Reference.objects.create(code='ref2', name='Reference 2', description='Reference 2 description')

        start_date = date(2022, 1, 1)
        self.ref1v1 = ReferenceVersion.objects.create(
            reference=self.ref1,
            version='1.0',
            start_date=start_date)
        self.ref1v2 = ReferenceVersion.objects.create(
            reference=self.ref1,
            version='2.0',
            start_date=start_date + timedelta(days=365))
        self.ref2v1 = ReferenceVersion.objects.create(
            reference=self.ref2,
            version='1.0',
            start_date=start_date)

    def test_get_all_refbooks(self):
        """
        Test GET request to RefBookList without date filter
        """
        url = reverse('refbook-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 2)
        ref1_data = response.data['refbooks'][0]
        ref2_data = response.data['refbooks'][1]
        self.assertEqual(ref1_data['id'], self.ref1.id)
        self.assertEqual(ref1_data['code'], self.ref1.code)
        self.assertEqual(ref1_data['name'], self.ref1v2.version)
        self.assertEqual(ref2_data['id'], self.ref2.id)
        self.assertEqual(ref2_data['code'], self.ref2.code)
        self.assertEqual(ref2_data['name'], self.ref2v1.version)

    def test_get_refbooks_with_date_filter(self):
        """
        Test GET request to RefBookList with date filter
        """
        url = reverse('refbook-list')
        date_filter = '2022-06-30'
        response = self.client.get(url, {'date': date_filter})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['refbooks']), 2)
        ref_data = response.data['refbooks'][0]
        self.assertEqual(ref_data['id'], self.ref1.id)
        self.assertEqual(ref_data['code'], self.ref1.code)
        self.assertEqual(ref_data['name'], self.ref1v1.version)
