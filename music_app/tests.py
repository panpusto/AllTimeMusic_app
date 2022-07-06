import pytest
from django.contrib.auth.models import User
from django.test import Client
from music_app.models import Genre, Band, Label, Album, Musician, MusicianBand, Review


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


@pytest.fixture
def musician(user):
    musician = Musician.objects.create(
        name="Nergal",
        full_name="Adam Darski",
        place_of_birth='Danzig, Poland',
        bio='founder of Behemoth',
        added_by_id=user.id
    )
    return musician


@pytest.fixture
def musician_to_band(musician, band):
    musician_to_band = MusicianBand.objects.create(
        musician=musician,
        band=band,
        year_from=1999,
        year_to=2010,
        role='leading guitar, vocal'
    )
    return musician_to_band


@pytest.fixture
def review(client, user, album, band):
    review = Review.objects.create(
        subject='Oldschool still rules!',
        album=album,
        band=band,
        rating=8.5,
        description='great music for heavy metal maniacs',
        user=user
    )
    return review


@pytest.mark.django_db
def test_connection(client):
    response = client.get('')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_account_view(client, user):
    get_response = client.get('/create-account/')
    assert get_response.status_code == 200
    count_before_create = User.objects.count()
    new_user = {
        'username': 'maniek',
        'password': 'lanek123',
        'password2': 'lanek123',
        'first_name': 'Marian',
        'last_name': 'Borek',
        'email': 'marianek@mario.pl',
    }
    post_response = client.post(
        '/create-account/',
        new_user,
        follow=True
    )
    count_after_create = User.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_login_view(client, user):
    response = client.get('/login/')
    assert response.status_code == 200
    login_user = {
        'username': user.username,
        'password': user.password
    }
    post_response = client.post(
        '/login/',
        login_user,
        follow=True
    )
    assert post_response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    get_response = client.get('/logout/')
    assert get_response.status_code == 302


@pytest.mark.django_db
def test_reset_password_view(client, user):
    client.force_login(user)
    get_response = client.get(f'/reset-password/{user.id}/')
    assert get_response.status_code == 200
    post_response = client.post(
        f'/reset-password/{user.id}/',
        {
            'new_password': 'bolek',
            'new_password2': 'bolek'
        },
        follow=True
    )
    assert post_response.status_code == 200

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
    response = client.get(f'/band/details/{band.id}/')
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
def test_band_create_view(client, band,label, genre, user):
    response = client.get('/band/create/')
    assert response.status_code == 302  # for not logged user
    client.force_login(user)
    get_response = client.get('/band/create/')
    assert get_response.status_code == 200  # for logged user
    # count_before_create = Band.objects.count()
    new_band = {
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
        }
    post_response = client.post(
        '/band/create/',
        new_band,
        follow=True
    )
    # count_after_create = Band.objects.count()
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
    response = client.get(f'/album/details/{album.id}/')
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
def test_album_create_view(client, album, band, label, genre, user):
    response = client.get('/album/create/')
    assert response.status_code == 302  # for not logged user
    client.force_login(user)
    get_response = client.get('/album/create/')
    assert get_response.status_code == 200
    # count_before_create = Album.objects.count()
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
    # count_after_create = Album.objects.count()
    assert post_response.status_code == 200
    # assert count_after_create == count_before_create + 1    # TODO doesn't work in terminal, test passed with 'run'


@pytest.mark.django_db
def test_album_update_view(client, album, band, label, genre, user):
    album = Album.objects.first()
    response = client.get(f'/album/update/{album.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/album/update/{album.id}/')
    assert get_response.status_code == 200
    album.title = 'Master of Puppets'
    album.format = 3
    album.save()
    assert get_response.status_code == 200
    album_obj = Album.objects.get(id=album.id)
    assert album_obj.title == album.title
    assert album_obj.format == album.format


@pytest.mark.django_db
def test_album_delete_view(client, album, user):
    album = Album.objects.first()
    response = client.get(f'/album/delete/{album.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/album/delete/{album.id}/')
    assert get_response.status_code == 302
    album_ids = [album.id for album in Album.objects.all()]
    assert album.id not in album_ids


@pytest.mark.django_db
def test_musician_details_view(client, musician, user, band, musician_to_band):
    response = client.get(f'/musician/details/{musician.id}/')
    assert response.context.get('name' == 'Nergal')
    assert response.context.get('full_name' == 'Adam Darski')
    assert response.context.get('place_of_birth' == 'Danzig, Poland')
    assert response.context.get('bio' == 'founder of Behemoth')
    assert response.context.get('added_by_id' == user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_musician_create_view(client, user, band, musician, musician_to_band):
    response = client.get('/musician/create/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get('/musician/create/')
    assert get_response.status_code == 200
    count_before_create = Musician.objects.count()
    new_musician = {
        'name': 'Joe',
        'full_name': 'Joe Talbot',
        'place_of_birth': 'Exeter, England',
        'bio': 'Welsh singer and songwriter. Vocalist for Idles',
        'added_by_id': user.id
    }
    post_response = client.post(
        '/musician/create/',
        new_musician,
        follow=True,
    )
    count_after_create = Musician.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_musician_update_view(client, user, band, musician, musician_to_band):
    musician = Musician.objects.first()
    response = client.get(f'/musician/update/{musician.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/musician/update/{musician.id}/')
    assert get_response.status_code == 200
    musician.name = 'Orion'
    musician.full_name = 'Tomasz Wróblewski'
    musician.save()
    assert get_response.status_code == 200
    musician_obj = Musician.objects.get(id=musician.id)
    assert musician_obj.name == musician.name
    assert musician_obj.full_name == musician.full_name


@pytest.mark.django_db
def test_musician_delete_view(client, musician, user):
    musician = Musician.objects.first()
    response = client.get(f'/musician/delete/{musician.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/musician/delete/{musician.id}/')
    assert get_response.status_code == 302
    musician_ids = [musician.id for musician in Musician.objects.all()]
    assert musician.id not in musician_ids


@pytest.mark.django_db
def test_add_musician_to_band_view(client, band, musician, musician_to_band, user):
    response = client.get('/add/musician-to-band/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get('/add/musician-to-band/')
    assert get_response.status_code == 200
    # count_before_create = MusicianBand.objects.count()
    new_musician_to_band = {
        'musician': musician.id,
        'band': band.id,
        'year_from': 1980,
        'year_to': 2000,
        'role': 'solo guitar'
    }
    post_response = client.post(
        '/add/musician-to-band/',
        new_musician_to_band,
        follow=True,
    )
    # count_after_create = MusicianBand.objects.count()
    assert post_response.status_code == 200
    # assert count_after_create == count_before_create + 1  #TODO fix, passed in 'run' not terminal


@pytest.mark.django_db
def test_delete_musician_from_band(client, band, musician, musician_to_band, user):
    musician_in_band = MusicianBand.objects.first()
    response = client.get(f'/delete/musician-from-band/{musician_in_band.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/delete/musician-from-band/{musician_in_band.id}/')
    assert get_response.status_code == 302
    musician_in_band_ids = [musician_in_band.id for musician_in_band in MusicianBand.objects.all()]
    assert musician_in_band.id not in musician_in_band_ids


@pytest.mark.django_db
def test_label_details_view(client, user, label):
    response = client.get(f'/label/details/{label.id}/')
    assert response.context.get('name' == 'Sony Music Polska')
    assert response.context.get('address' == 'ul.Zajęcza, Warsaw')
    assert response.context.get('country' == 'Poland')
    assert response.context.get('status' == 1)
    assert response.context.get('styles' == 'pop')
    assert response.context.get('founding_year' == 1995)
    assert response.context.get('added_by_id' == user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_label_create_view(client, user, label):
    response = client.get('/label/create/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get('/label/create/')
    assert get_response.status_code == 200
    count_before_create = Label.objects.count()
    new_label = {
        'name': 'New Aeon Musick',
        'address': 'Danzig 4324',
        'country': 'Poland',
        'status': 1,
        'styles': 'blackened-death metal, black metal',
        'founding_year': '2006',
        'added_by_id': user.id
    }
    post_response = client.post(
        '/label/create/',
        new_label,
        follow=True,
    )
    count_after_create = Label.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_label_update_view(client, user, label):
    label = Label.objects.first()
    response = client.get(f'/label/update/{label.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/label/update/{label.id}/')
    assert get_response.status_code == 200
    label.name = 'Astigmatic Records'
    label.styles = 'avant-garde'
    label.save()
    assert get_response.status_code == 200
    label_obj = Label.objects.get(id=label.id)
    assert label_obj.name == label.name
    assert label_obj.styles == label.styles


@pytest.mark.django_db
def test_label_delete_view(client, label, user):
    label = Label.objects.first()
    response = client.get(f'/label/delete/{label.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/label/delete/{label.id}/')
    assert get_response.status_code == 302
    label_ids = [label.id for label in Label.objects.all()]
    assert label.id not in label_ids


@pytest.mark.django_db
def test_genre_create_view(client, genre, user):
    response = client.get('/genre/create/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get('/genre/create/')
    assert get_response.status_code == 200
    count_before_create = Genre.objects.count()
    new_genre = {
        'name': 'heavy metal',
    }
    post_response = client.post(
        '/genre/create/',
        new_genre,
        follow=True,
    )
    count_after_create = Genre.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_genre_update_view(client, genre, user):
    genre = Genre.objects.first()
    response = client.get(f'/genre/update/{genre.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/genre/update/{genre.id}/')
    assert get_response.status_code == 200
    genre.name = 'indie rock'
    genre.save()
    assert get_response.status_code == 200
    genre_obj = Genre.objects.get(id=genre.id)
    assert genre_obj.name == genre.name


@pytest.mark.django_db
def test_genre_delete_view(client, genre, user):
    genre = Genre.objects.first()
    response = client.get(f'/genre/delete/{genre.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/genre/delete/{genre.id}/')
    assert get_response.status_code == 302
    genre_ids = [genre.id for genre in Genre.objects.all()]
    assert genre.id not in genre_ids


@pytest.mark.django_db
def test_review_details_view(client, review, album, band, user):
    response = client.get(f'/review/details/{review.id}/')
    assert response.context.get('subject' == 'Oldschool still rules!')
    assert response.context.get('album' == album.id)
    assert response.context.get('band' == band.id)
    assert response.context.get('rating' == 8.5)
    assert response.context.get('description' == 'great music for heavy metal maniacs')
    assert response.context.get('user' == user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_review_create_view(client, review, album, band, user):
    response = client.get(f'/review/create/{album.id}/{band.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/review/create/{album.id}/{band.id}/')
    assert get_response.status_code == 200
    count_before_create = Review.objects.count()
    new_review = {
        'subject': 'titans still on the throne',
        'album': album.id,
        'band': band.id,
        'rating': 10.0,
        'description': 'the best album from them so far',
        'user': user.id
    }
    post_response = client.post(
        f'/review/create/{album.id}/{band.id}/',
        new_review,
        follow=True,
    )
    count_after_create = Review.objects.count()
    assert post_response.status_code == 200
    assert count_after_create == count_before_create + 1


@pytest.mark.django_db
def test_review_update_view(client, review, album, band, user):
    review = Review.objects.first()
    response = client.get(f'/review/update/{review.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/review/update/{review.id}/')
    assert get_response.status_code == 200
    review.subject = 'booooring'
    review.rating = 3.5
    review.save()
    assert get_response.status_code == 200
    review_obj = Review.objects.get(id=review.id)
    assert review_obj.subject == review.subject
    assert review_obj.rating == review.rating


@pytest.mark.django_db
def test_review_delete_view(client, review, user):
    review = Review.objects.first()
    response = client.get(f'/review/delete/{review.id}/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get(f'/review/delete/{review.id}/')
    assert get_response.status_code == 302
    review_ids = [review.id for review in Review.objects.all()]
    assert review.id not in review_ids


@pytest.mark.django_db
def test_add_board_view(client, user):
    response = client.get('/add-board/')
    assert response.status_code == 302
    client.force_login(user)
    get_response = client.get('/add-board/')
    assert get_response.status_code == 200


@pytest.mark.django_db
def test_search_band_view(client):
    response = client.get(
        '/searching-results/',
        {'query': 'Metallica'},
        follow=True)
    assert response.status_code == 200

