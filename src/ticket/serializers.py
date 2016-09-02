from rest_framework import serializers
from ticket.models import Ticket

class TicketSerializer(serializers.HyperlinkedModelSerializer):
  url = serializers.ReadOnlyField()
  class Meta:
    model = Ticket
    fields = ('url', 'request', 'completed', 'order')
