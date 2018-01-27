from django.db.transaction import atomic
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models


class SignUpView(APIView):
    permission_classes = []
    serializer_class = serializers.SignUpSerializer

    @atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        merchant = serializer.save()
        token = models.MerchantToken.objects.create(
            user=merchant
        )

        return Response({
            'token': token.key
        })
