# faq/views.py
from rest_framework.generics import ListAPIView
from .models import FAQ
from .serializers import FAQSerializer

class FAQListView(ListAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}