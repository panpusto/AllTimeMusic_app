from django.db import models
from django.contrib.auth.models import User

BAND_STATUS = [
    (1, 'active'),
    (2, 'on hold'),
    (3, 'split-up'),
    (4, 'unknown'),
    (5, 'changed name'),
    (6, 'disputed'),
]

LABEL_STATUS = [
    (1, 'active'),
    (2, 'closed'),
    (3, 'unknown'),
]

ALBUM_TYPES = [
    (1, 'Full-length'),
    (2, 'EP/Mini-albums'),
    (3, 'Compilation'),
    (4, 'Single'),
    (5, 'Mixtape'),
    (6, 'DJ Mix'),
    (7, 'Bootleg/Unauthorized'),
    (8, 'Live album'),
    (9, 'Video'),
    (10, 'Soundtrack'),
    (11, 'Promo'),
]

FORMAT_TYPES = [
    (1, 'CD'),
    (2, 'vinyl'),
    (3, 'cassette'),
    (4, 'CD/DVD'),
    (5, 'digibook'),
    (6, 'digital'),
    (7, 'all formats'),
]


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=128)
    country = models.CharField(max_length=30)
    status = models.IntegerField(choices=LABEL_STATUS)
    styles = models.CharField(max_length=128)
    founding_year = models.IntegerField()

    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Musician(models.Model):
    name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50)
    born = models.DateField(null=True)
    died = models.DateField(null=True)
    place_of_birth = models.CharField(max_length=50)
    bio = models.TextField(null=True)

    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.full_name}'


class Band(models.Model):
    name = models.CharField(max_length=50)
    country_of_origin = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    status = models.IntegerField(choices=BAND_STATUS)
    formed_in = models.IntegerField()
    ended_in = models.IntegerField(null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    lyrical_themes = models.CharField(max_length=60)
    current_label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='current_label')
    bio = models.TextField(null=True)
    members = models.ManyToManyField(Musician, through='MusicianBand')

    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}, {self.country_of_origin}'


class Album(models.Model):
    title = models.CharField(max_length=50)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='album_by')
    genre = models.ManyToManyField(Genre)
    type = models.IntegerField(choices=ALBUM_TYPES)
    release_date = models.DateField()
    catalog_id = models.CharField(max_length=16)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    format = models.IntegerField(choices=FORMAT_TYPES)

    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MusicianBand(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    year_from = models.IntegerField(null=True)
    year_to = models.IntegerField(null=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.musician.name} - {self.musician.full_name}'



