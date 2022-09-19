from rest_framework import generics, permissions

from api.serializers import GenreSerializer
from music_app.models import Genre


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
