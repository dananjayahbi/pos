"""Platform authentication views."""

import logging

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


class PlatformLoginView(APIView):
    """
    POST /api/v1/platform/auth/login/
    Authenticates a PlatformUser and returns JWT access + refresh tokens.
    IMPORTANT: This is SEPARATE from tenant user login at /api/v1/auth/login/
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").lower().strip()
        password = request.data.get("password", "")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Import PlatformUser explicitly (not via get_user_model which returns tenant User)
        from apps.platform.models import PlatformUser  # noqa: PLC0415

        try:
            user = PlatformUser.objects.get(email=email)
        except PlatformUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"error": "Account is disabled."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        logger.info("Platform user logged in: %s (role=%s)", user.email, user.role)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_super_admin": user.is_super_admin,
            },
        })
