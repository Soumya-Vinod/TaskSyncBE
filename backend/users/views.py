from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Team
from .serializers import UserSerializer, TeamSerializer
from django.contrib.auth.hashers import make_password
from .permissions import IsAdminOrPartialAdmin


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrPartialAdmin]

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(["POST"])
@permission_classes([permissions.AllowAny])  # Public endpoint
def signup(request):
    """Handles user registration"""
    data = request.data

    if User.objects.filter(username=data.get("username")).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=data.get("email")).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    password = data.get("password")
    if not password or len(password) < 6:
        return Response({"error": "Password must be at least 6 characters long"}, status=status.HTTP_400_BAD_REQUEST)

    team = None
    if "team" in data:
        try:
            team = Team.objects.get(id=data["team"])
        except Team.DoesNotExist:
            return Response({"error": "Invalid team ID"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=data["username"],
        email=data["email"],
        password=make_password(password),
        role=data.get("role", "user"),
        team=team,
    )

    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
