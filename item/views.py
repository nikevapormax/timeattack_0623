from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import ItemSerializer

from .models import Category

# Create your views here.
class ItemView(APIView):
    
    def get(self, request):
        print(request.data)
        category = Category.objects.filter(name=request)
        
        serialized_items = ItemSerializer(data=request.data, many=True, partial=True)
        return Response(serialized_items, status=status.HTTP_200_OK)
    