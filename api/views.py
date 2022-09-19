from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from api.serializers import (
    GenreSerializer,
    LabelSerializer,
    MusicianSerializer,
    BandSerializer,
    AlbumSerializer,
    ReviewSerializer,
    MusicianBandSerializer,
    UserSerializer,
)

from music_app.models import (
    Genre,
    Label,
    Musician,
    Band,
    Album,
    Review,
    MusicianBand,
)


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class LabelList(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class MusicianList(generics.ListCreateAPIView):
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer


class BandList(generics.ListCreateAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer


class AlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class ReviewList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class MusicianBandList(generics.ListCreateAPIView):
    queryset = MusicianBand.objects.all()
    serializer_class = MusicianBandSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = get_user_model().objects.all().order_by('id')
    serializer_class = UserSerializer
