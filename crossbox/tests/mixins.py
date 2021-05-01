import unittest

from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        self.patcher_customer_create = unittest.mock.patch(
            'stripe.Customer.create')
        self.patcher_customer_retrieve = unittest.mock.patch(
            'stripe.Customer.retrieve')
        self.patcher_customer_delete = unittest.mock.patch(
            'stripe.Customer.delete')

        self.patcher_api_key = unittest.mock.patch('stripe.api_key')

        self.mock_customer_create = self.patcher_customer_create.start()
        self.mock_customer_retrieve = self.patcher_customer_retrieve.start()
        self.mock_customer_delete = self.patcher_customer_delete.start()
        self.mock_api_key = self.patcher_api_key.start()

        self.mock_customer_create.return_value = {'id': 'mock_customer_id'}

    def tearDown(self):
        self.patcher_customer_create.stop()
        self.patcher_customer_retrieve.stop()
        self.patcher_customer_delete.stop()
        self.patcher_api_key.stop()
