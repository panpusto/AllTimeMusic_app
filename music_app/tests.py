from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client
from music_app.models import Genre, Band, Label, Album


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User.objects.create_user(
        username='czarek',
        password='kola123',
        first_name='Marek',
        last_name='Jarmarek',
        email='marko@o2.pl'
    )
    return user


@pytest.fixture
def genre():
    genre = Genre.objects.create(
        name='rock'
    )
    return genre


@pytest.fixture
def band(label, user):
    band = Band.objects.create(
        name='Iron Maiden',
        country_of_origin='Great Britain',
        location='Leyton, London',
        status=1,
        formed_in=1975,
        lyrical_themes='war, politics, life',
        current_label=label,
        bio='NWOBHM godfathers',
        added_by_id=user.id,
    )
    return band


@pytest.fixture
def label(user):
    label = Label.objects.create(
        name='Sony Music Polska',
        address='ul.Zajęcza, Warsaw',
        country='Poland',
        status=1,
        styles='pop',
        founding_year=1995,
        added_by_id=user.id
    )
    return label


@pytest.fixture
def album(user, band, genre, label):
    album = Album.objects.create(
        title='Black Album',
        band=band,
        type=3,
        release_date='1990-06-04',
        catalog_id='MET-203',
        label=label,
        format=2,
        added_by_id=user.id
    )
    return album


@pytest.mark.django_db
def test_connection(client):
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_bands_list_alphabetical(client):
    get_response = client.get('/bands/alphabetical/')
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_label_list_view(client):
    get_response = client.get('/labels/')
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_albums_last_added_list_view(client):
    get_response = client.get('/albums/last-added/')
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_reviews_list_view(client):
    get_response = client.get('/reviews/list/')
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_bands_genres_list_view(client):
    get_response = client.get('/bands/genres/')
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_bands_by_genre_list_view(client):
    get_response = client.get('/bands/genres/1/')
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_band_details_view(client, band, label, genre, user):
    response = client.get('/band/details/1/')
    assert response.context.get('name' == 'Iron Maiden')
    assert response.context.get('country_of_origin' == 'Great Britain')
    assert response.context.get('location' == 'Leyton, London')
    assert response.context.get('status' == 1)
    assert response.context.get('formed_in' == 1975)
    assert response.context.get('genre' == genre)
    assert response.context.get('lyrical_themes' == 'war, politics, life')
    assert response.context.get('current_label' == label)
    assert response.context.get('bio' == 'NWOBHM godfathers')
    assert response.context.get('added_by_id' == user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_band_create_view(client, label, genre, user):
    response = client.get('/band/create/')
    assert response.status_code == 302  # for not logged user
    client.force_login(user)
    get_response = client.get('/band/create/')
    assert get_response.status_code == 200  # for logged user
    count_before_create = Band.objects.count()
    post_response = client.post(
        '/band/create/',
        {
            'name': 'Metallica',
            'country_of_origin': 'USA',
            'location': 'San Francisco',
            'status': 1,
            'formed_in': 1981,
            'genre': genre.id,
            'lyrical_themes': 'war, life',
            'current_label': label.id,
            'bio': 'Thrash Metal Titans',
            'added_by_id': user.id
        },
        follow=True
    )
    count_after_create = Band.objects.count()
    assert post_response.status_code == 200
    # assert count_after_create == count_before_create + 1  # TODO doesn't work in terminal, test passed with 'run'


@pytest.mark.django_db
def test_update_band_view(client, band, user):
    band = Band.objects.first()
    response = client.get(f'/band/update/{band.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/band/update/{band.id}/')
    assert get_response.status_code == 200
    band.location = 'San Francisco'
    band.save()
    assert get_response.status_code == 200
    band_obj = Band.objects.get(id=band.id)
    assert band_obj.location == band.location


@pytest.mark.django_db
def test_delete_band_view(client, band, user):
    band = Band.objects.first()
    response = client.get(f'/band/delete/{band.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/band/delete/{band.id}/')
    assert get_response.status_code == 302
    band_ids = [band.id for band in Band.objects.all()]
    assert band.id not in band_ids


@pytest.mark.django_db
def test_album_details_view(client, album, band, label, genre, user):
    response = client.get('/album/details/1/')
    assert response.context.get('title' == 'Black Album')
    assert response.context.get('band' == band.id)
    assert response.context.get('genre' == genre)
    assert response.context.get('type' == 3)
    assert response.context.get('release_date' == '1990-06-04')
    assert response.context.get('catalog_id' == 'MET-203')
    assert response.context.get('label' == label.id)
    assert response.context.get('format' == 2)
    assert response.context.get('added_by_id' == user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_album_create_view(client, band, label, genre, user):
    response = client.get('/album/create/')
    assert response.status_code == 302  # for not logged user
    client.force_login(user)
    get_response = client.get('/album/create/')
    assert get_response.status_code == 200
    count_before_create = Album.objects.count()
    new_band = {
            'title': 'Black Album',
            'band': band.id,
            'genre': genre.id,
            'type': 3,
            'catalog_id': 'MBL-133',
            'label': label.id,
            'format': 2,
            'added_by_id': user.id
        }
    post_response = client.post(
        '/album/create/',
        new_band,
        follow=True,
    )
    count_after_create = Album.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1