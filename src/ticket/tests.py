from django.core.urlresolvers import reverse
from django.test import TestCase
from ticket.models import Ticket
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
def createTicket(client):
    url = reverse('ticket-list')
    data = {'request': 'wat'}
    return client.post(url, data, format='json')


class TestCreate(APITestCase):
    def setUp(self):
        self.response = createTicket(self.client)

    def test_201(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_created(self):
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().request, 'wat')


class TestUpdateTicket(APITestCase):
  """
  Ensure we can update an existing ticket item using PUT
  """
  def setUp(self):
    response = createTicket(self.client)
    self.assertEqual(Ticket.objects.get().completed, False)
    url = response['Location']
    data = {'request': 'Walk the dog', 'completed': True}
    self.response = self.client.put(url, data, format='json')

  def test_received_200_created_status_code(self):
    self.assertEqual(self.response.status_code, status.HTTP_200_OK)

  def test_item_was_updated(self):
    self.assertEqual(Ticket.objects.get().completed, True)

class TestPatchTicket(APITestCase):
  """
  Ensure we can update an existing ticket item using PATCH
  """
  def setUp(self):
    response = createTicket(self.client)
    self.assertEqual(Ticket.objects.get().completed, False)
    url = response['Location']
    data = {'request': 'Walk the dog', 'completed': True}
    self.response = self.client.patch(url, data, format='json')

  def test_received_200_ok_status_code(self):
    self.assertEqual(self.response.status_code, status.HTTP_200_OK)

  def test_item_was_updated(self):
    self.assertEqual(Ticket.objects.get().completed, True)

class TestDeleteTicket(APITestCase):
  """
  Ensure we can delete a ticket item
  """
  def setUp(self):
    response = createTicket(self.client)
    self.assertEqual(Ticket.objects.count(), 1)
    url = response['Location']
    self.response = self.client.delete(url)

  def test_received_204_no_content_status_code(self):
    self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

  def test_the_item_was_deleted(self):
    self.assertEqual(Ticket.objects.count(), 0)

class TestDeleteAllItems(APITestCase):
  """
  Ensure we can delete all ticket items
  """
  def setUp(self):
    createTicket(self.client)
    createTicket(self.client)
    self.assertEqual(Ticket.objects.count(), 2)
    self.response = self.client.delete(reverse('ticket-list'))

  def test_received_204_no_content_status_code(self):
    self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

  def test_all_items_were_deleted(self):
    self.assertEqual(Ticket.objects.count(), 0)
