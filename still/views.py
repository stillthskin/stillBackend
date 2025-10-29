from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView     
from rest_framework.response import Response 
from rest_framework.decorators import action  # 👈 add this line
from django.views import View
from .models import DynamicData
from .serializers import DynamicDataSerializer

class TestView(APIView):
    def get(self, request):
        return Response({"message": "Hello World"})

class DynamicDataViewSet(viewsets.ModelViewSet):
    queryset = DynamicData.objects.all().order_by('-created_at')
    serializer_class = DynamicDataSerializer


    # Custom filter endpoint e.g. /api/dynamicdata/by_type/?type=currency
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        data_type = request.query_params.get('type')
        if not data_type:
            return Response({"error": "type query param is required"}, status=400)
        queryset = DynamicData.objects.filter(type__iexact=data_type).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)