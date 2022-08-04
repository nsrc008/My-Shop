from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from authAppshop.models.transaction import Transaction
from authAppshop.serializer.transactionSerializer import TransactionSerializer

class TransactionDetailView(generics.RetrieveAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer
    permission_classes  = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

# retorna lista de transacciones de una cuenta
class TransactionsAccountView(generics.ListAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer
    permission_classes  = (IsAuthenticated,)

    def get_queryset(self):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Transaction.objects.filter(origin_account_id=self.kwargs['account'])
        return queryset

class TransactionCreateView(generics.CreateAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer
    permission_classes  = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != request.data['user_id']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TransactionSerializer(data=request.data['transactin_data'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response("Transaccion Exitosa", status=status.HTTP_201_CREATED)

class TransactionUpdateView(generics.UpdateAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer
    permission_classes  = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)

class TransactionDeleteView(generics.DestroyAPIView):
    queryset            = Transaction.objects.all()
    serializer_class    = TransactionSerializer
    permission_classes  = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)