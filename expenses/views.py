from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from expenses.serializers import ExpensesSerializer,RegisterUserSerializer,UserProfileSerializer
from expenses.models import Expenses,User
from django.db.models import Sum
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            data = request.data
            data['user_ref'] = request.user.pk
            print(data)
            serializer = ExpensesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Transaction Added'},status=200)
            else:
                return Response({'errors':serializer.errors},status=400)
        except Exception as e:
            return Response({'Error':str(e)},status=400)

class BalanceAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            income_amount = Expenses.objects.filter(Q(user_ref=user) & Q(typeof="Income")).aggregate(Sum('amount'))['amount__sum']
            expen_amount = Expenses.objects.filter(Q(user_ref=user) & Q(typeof="Expenditure")).aggregate(Sum('amount'))['amount__sum']
            if income_amount is None:
                income_amount = 0
            if expen_amount is None:
                expen_amount = 0
            total = income_amount - expen_amount
            return Response({'total': total}, status=200)
        except Exception as e:
            return Response({'Error': str(e)}, status=400)

class TotalAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user = request.user
            income = Expenses.objects.filter(Q(typeof='Income') & Q(user_ref=user)).aggregate(Sum('amount'))
            expen = Expenses.objects.filter(Q(typeof='Expenditure') & Q(user_ref=user)).aggregate(Sum('amount'))
            return Response({'income':income['amount__sum'],'expense':expen['amount__sum']},status=200)
        except Exception as e:
            return Response({'Error':str(e)},status=400)

class GetProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            user = request.user
            user_det = User.objects.get(email=user)
            user_serializer = UserProfileSerializer(user_det)
            return Response({'data':user_serializer.data},status=200)
        except Exception as e:
            return Response({'Error':str(e)},status=400)

class HistoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            history = Expenses.objects.filter(user_ref=request.user).order_by('-createdOn')
            serializer = ExpensesSerializer(history,many=True)
            return Response(serializer.data,status=200)
        except Exception as e:
            return Response({'Error':str(e)},status=400)

class DeleteTransaction(APIView):
    def delete(self,request,id):
        try:
            trans = Expenses.objects.get(id=id)
            trans.delete()
            return Response({'message':'Transaction Deleted'},status=200)
        except Exception as e:
            return Response({'Error':str(e)},status=400)

