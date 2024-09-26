from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class StaticJsonView(APIView):
    def get(self, request):
        # Static JSON data
        data = {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "published_date": "1925-04-10"
        }
        return Response(data, status=status.HTTP_200_OK)
