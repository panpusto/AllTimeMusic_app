from django.urls import path
from api import views as v


urlpatterns = [
    path("genres/", v.GenreList.as_view(), name="api-genre-list"),
    path("genres/<int:pk>/", v.GenreDetail.as_view(), name="api-genre-detail"),
    path("labels/", v.LabelList.as_view(), name="api-label-list"),
    path("musicians/", v.MusicianList.as_view(), name="api-musicians-list"),
    path("bands/", v.BandList.as_view(), name="api-bands-list"),
    path("albums/", v.AlbumList.as_view(), name="api-albums-list"),
    path("reviews/", v.ReviewList.as_view(), name="api-reviews-list"),
    path("musician-to-band/", v.MusicianBandList.as_view(), name='api-musician-band-list'),
]
