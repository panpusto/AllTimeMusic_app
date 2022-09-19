from django.urls import path
from api import views as v


urlpatterns = [
    path("genres/", v.GenreList.as_view(), name="api-genre-list"),
    path("genres/<int:pk>/", v.GenreDetail.as_view(), name="api-genre-detail"),
]
