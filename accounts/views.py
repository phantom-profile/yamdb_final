from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .permissions import AccountOwner, IsAdmin
from .serializers import ConfirmationCodeEmailSerializer, UserSerializer
from .utils import Email


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['username']
    search_fields = ['username']
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[IsAuthenticated, AccountOwner],
            url_path='me', url_name='my-account')
    def my_account(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def send_confirmation_code(request):
    email = request.data['email']
    serializer = ConfirmationCodeEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(email=email)
    user = get_object_or_404(User, email=email)

    SUBJECT = 'YaMDb Confirmation Code'
    confirmation_code = default_token_generator.make_token(user=user)
    BODY = (f'Hello,\n\n'
            'Here you have your confirmation code to recieve an '
            'authentication token: \n\n'
            f'{confirmation_code}')

    data = {'email': email, 'subject': SUBJECT, 'body': BODY}

    Email.send_email(data)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def obtain_token(request):
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user=user,
                                           token=confirmation_code):
        token = user.token
        data = {'token': token}
        return Response(data, status=status.HTTP_200_OK)
    return Response({'detail': 'Неправильные данные'},
                    status=status.HTTP_401_UNAUTHORIZED)
