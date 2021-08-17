from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response


class IsSeller(MiddlewareMixin):
    def process_request(self, request):
        url = request.path
        # request.user.is_authenticated and request.user.is_seller
        if "/api/seller/" in url:
            if not request.user.is_authenticated or not request.user.is_seller:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
