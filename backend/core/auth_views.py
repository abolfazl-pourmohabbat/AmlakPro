from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = str(request.data.get('username') or '').strip()
        password = str(request.data.get('password') or '')
        first_name = str(request.data.get('first_name') or '').strip()
        last_name = str(request.data.get('last_name') or '').strip()
        email = str(request.data.get('email') or '').strip()

        if not username or not password:
            return Response({'detail': 'نام کاربری و رمز عبور الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username__iexact=username).exists():
            return Response({'detail': 'این نام کاربری قبلاً ثبت شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except Exception as exc:
            return Response({'detail': ' '.join(str(item) for item in exc.messages)}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'name': user.get_full_name() or user.username}, status=status.HTTP_201_CREATED)
