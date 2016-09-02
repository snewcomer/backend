from django.shortcuts import render
from ticket.models import Ticket
from ticket.serializers import TicketSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.response import Response


class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.url = reverse('ticket-detail', args=[instance.pk], request=self.request)
        instance.save()

    def delete(self, request):
        Ticket.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

