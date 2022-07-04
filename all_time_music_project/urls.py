"""all_time_music_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from music_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPageView.as_view(), name='landing-page'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create-account/', views.UserCreateView.as_view(), name='create-account'),
    path('reset-password/<int:user_id>/', views.PasswordResetView.as_view(), name='reset-password'),
    path('bands/alphabetical/', views.BandsListAlphabeticalView.as_view(), name='bands-list-alphabetical'),
    path('bands/genres/', views.BandsGenresListView.as_view(), name='bands-genres-list'),
    path('bands/genres/<int:_id>/', views.BandsListByGenreView.as_view(), name='bands-list-by-genre'),
    path('band/details/<int:_id>/', views.BandDetailsView.as_view(), name='band-details'),
    path('band/create/', views.BandCreateView.as_view(), name='band-create'),
    path('band/update/<int:_id>/', views.BandUpdateView.as_view(), name='band-update'),
    path('band/delete/confirm/<int:_id>/', views.BandDeleteConfirmView.as_view(), name='band-delete-confirm'),
    path('band/delete/<int:_id>/', views.BandDeleteView.as_view(), name='band-delete'),
    path('add/musician-to-band/', views.AddMusicianToBand.as_view(), name='add-musician-to-band'),
    path('delete/musician-from-band/confirm/<int:_id>/',
         views.DeleteMusicianFromBandConfirmView.as_view(), name='delete-music-from-band-confirm'),
    path('delete/musician-from-band/<int:_id>/',
         views.DeleteMusicianFromBand.as_view(), name='delete-musician-from-band'),
    path('musician/details/<int:_id>/', views.MusicianDetailsView.as_view(), name='musician-details'),
    path('musician/create/', views.MusicianCreateView.as_view(), name='musician-create'),
    path('musician/update/<int:_id>/', views.MusicianUpdateView.as_view(), name='musician-update'),
    path('musician/delete/confirm/<int:_id>/', views.MusicianDeleteConfirmView.as_view(), name='musician-delete-confirm'),
    path('musician/delete/<int:_id>/', views.MusicianDeleteView.as_view(), name='musician-delete'),
    path('labels/', views.LabelListView.as_view(), name='labels-list'),
    path('label/details/<int:_id>/', views.LabelDetailsView.as_view(), name='label-details'),
    path('label/create/', views.LabelCreateView.as_view(), name='label-create'),
    path('label/update/<int:_id>/', views.LabelUpdateView.as_view(), name='label-update'),
    path('label/delete/confirm/<int:_id>/', views.LabelDeleteConfirmView.as_view(), name='label-delete-confirm'),
    path('label/delete/<int:_id>/', views.LabelDeleteView.as_view(), name='label-delete'),
    path('genre/create/', views.GenreCreateView.as_view(), name='genre-create'),
    path('genre/update/<int:_id>/', views.GenreUpdateView.as_view(), name='genre-update'),
    path('genre/delete/confirm/<int:_id>/', views.GenreDeleteConfirmView.as_view(), name='genre-delete-confirm'),
    path('genre/delete/<int:_id>/', views.GenreDeleteView.as_view(), name='genre-delete'),
    path('albums/last-added/', views.AlbumLastAddedView.as_view(), name='albums-last-added'),
    path('album/details/<int:album_id>/', views.AlbumDetailsView.as_view(), name='album-details-view'),
    path('album/create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('album/update/<int:_id>/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('album/delete/confirm/<int:_id>/', views.AlbumDeleteConfirmView.as_view(), name='album-delete-confirm'),
    path('album/delete/<int:_id>/', views.AlbumDeleteView.as_view(), name='album-delete'),
    path('review/create/<int:album_id>/<int:band_id>/', views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/list/', views.ReviewsListView.as_view(), name='reviews-list'),
    path('add-board/', views.AddMusicDataView.as_view(), name='add-board'),
]
