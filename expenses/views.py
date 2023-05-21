from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from expenses.serializers import ExpensesSerializer,RegisterUserSerializer
from expenses.models import Expenses,User
from django.db.models import Sum
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUser(APIView):
    def post(self, request):
        try:
            reg_serializer = RegisterUserSerializer(data=request.data)
            if reg_serializer.is_valid():
                newUser = reg_serializer.save()
                if newUser:
                    return Response({'message': 'Created user'}, status=201)
            return Response(reg_serializer.errors, status=400)
        except Exception as e:
            return Response({'Error':str(e)},status=400)


class LoginUser(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({'Error': 'User Not Found'}, status=404)
            if not user.check_password(password):
                return Response({'Error': 'Password Incorrect'}, status=401)
            refresh = RefreshToken.for_user(user)
            return Response({'firstName': user.first_name, 'lastName': user.last_name, 'access_token': str(
                    refresh.access_token), 'refresh_token': str(refresh)}, status=200)
        except Exception as e:
            return Response({'Error': str(e)})


class ExpensesAPIView(APIView):
    def post(self,request):
        try:
            data = request.data
            if(data['amount']<0):
                data['typeof']='Expenditure'
            else:
                data['typeof']='Income'
            serializer = ExpensesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Transaction Added'},status=200)
            else:
                return Response({'Error':'Incorrect Inputs'},status=400)
        except Exception as e:
            return Response({'Error':str(e)},status=400)

class BalanceAPIView(APIView):
    def get(self,request):
        try:
            total_amount = Expenses.objects.aggregate(Sum('amount'))
            return Response({'total':total_amount['amount__sum']},status=200)
        except Exception as e:
            return Response({'Error':str(e)},status=400)

class TotalAPIView(APIView):
    def get(self,request):
        try:
            income = Expenses.objects.filter(typeof='Income').aggregate(Sum('amount'))
            expen = Expenses.objects.filter(typeof='Expenditure').aggregate(Sum('amount'))
            return Response({'income':income['amount__sum'],'expense':expen['amount__sum']},status=200)
        except Exception as e:
            return Response({'Error':str(e)},status=400)