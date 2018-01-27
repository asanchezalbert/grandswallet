from rest_framework.generics import ListAPIView
from . import serializers
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from grandswallet.utils import gen_code_for_exchange


class CodeView(ListAPIView):
    serializer_class = serializers.CodeSerializer

    def get_queryset(self):
        customer = self.request.user.customer
        account = customer.accounts.first()

        return account.codes.order_by('-created_date').all()

    @atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = request.user.customer
        account = customer.accounts.first()

        if account.available_balance < serializer.validated_data['amount']:
            return Response({
                'detail': 'No cuentas con saldo suficiente para generar el código.'
            }, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.save(
            code=gen_code_for_exchange(),
            account=account
        )

        serializer = self.serializer_class(code)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED)


class ExchangeView(ListAPIView):
    serializer_class = serializers.ExchangeSerializer

    def get_queryset(self):
        customer = self.request.user.customer
        account = customer.accounts.first()

        return account.exchanges.order_by('-created_date').all()

    @atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = request.user.customer
        account = customer.accounts.first()
        code = serializer.validated_data['code']
        amount = serializer.validated_data['amount']

        if code.amount < amount:
            return Response({
                'detail': 'Límite de crédito excedido.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if code.account.available_balance < amount:
            return Response({
                'detail': 'Fondos insuficientes.'
            }, status=status.HTTP_400_BAD_REQUEST)

        res = code.account.transfer(amount, account)

        ex = account.exchanges.create(
            code=code,
            amount=amount,
            details=serializer.validated_data.get('details', ''),
            authorization=res['authorisationId'],
            transaction=res['transactionId']
        )

        serializer = self.serializer_class(ex)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED)
