from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import BLANK_CHOICE_DASH
from music_app.models import BAND_STATUS, Musician, Genre, Label, LABEL_STATUS, ALBUM_TYPES, FORMAT_TYPES, Band
from .validators import validate_password


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreateForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='Repeat password')
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Passwords don't match")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError("This username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = User.objects.filter(email=email)
        if email:
            raise ValidationError("This email address is already connected to another account")
        return email


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="Enter new password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Re-enter new password")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('new_password2'):
            raise ValidationError("Passwords don't match")


class BandCreateForm(forms.Form):
    name = forms.CharField()
    country_of_origin = forms.CharField()
    location = forms.CharField()
    status = forms.ChoiceField(choices=BAND_STATUS)
    formed_in = forms.IntegerField()
    ended_in = forms.IntegerField(required=False)
    genre = forms.MultipleChoiceField(choices=[
        (genre.id, f'{genre}') for genre in Genre.objects.all().order_by('name')
        ],
        widget=forms.CheckboxSelectMultiple(),
        label='Genre',
        required=True
    )
    lyrical_themes = forms.CharField(max_length=60)
    current_label = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [
        (label.id, f'{label}') for label in Label.objects.all()
        ],
        required=True
    )
    bio = forms.CharField(widget=forms.Textarea(attrs={'col': 40, 'rows': 10}), required=False)


class MusicianCreateForm(forms.Form):
    name = forms.CharField()
    full_name = forms.CharField(label='Full name/Real name:')
    born = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}), required=False)
    died = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}), required=False)
    place_of_birth = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea(attrs={'col': 40, 'rows': 10}), required=False)


class LabelCreateForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    country = forms.CharField()
    status = forms.ChoiceField(choices=LABEL_STATUS)
    styles = forms.CharField()
    founding_year = forms.IntegerField()


class AlbumCreateForm(forms.Form):
    title = forms.CharField(max_length=50)
    band = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [
        (band.id, f'{band}') for band in Band.objects.all()
        ]
    )
    genre = forms.MultipleChoiceField(choices=[
        (genre.id, f'{genre}') for genre in Genre.objects.all()
    ],
        widget=forms.CheckboxSelectMultiple(),
        label='Genre',
        required=True
    )
    type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + ALBUM_TYPES)
    release_date = forms.DateField(widget=forms.NumberInput(attrs={'type': 'date'}), required=False)
    catalog_id = forms.CharField(max_length=16)
    label = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [
        (label.id, f'{label}') for label in Label.objects.all()
    ],
        required=True
    )
    format = forms.ChoiceField(choices=BLANK_CHOICE_DASH + FORMAT_TYPES)


class GenreCreateForm(forms.Form):
    name = forms.CharField()


class AddMusicianToBandForm(forms.Form):
    musician = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [
        (musician.id, f'{musician}') for musician in Musician.objects.all()
        ]
    )
    band = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [
        (band.id, f'{band}') for band in Band.objects.all()
        ]
    )
    year_from = forms.IntegerField()
    year_to = forms.IntegerField(required=False)
    role = forms.CharField()


class ReviewCreateForm(forms.Form):
    subject = forms.CharField()
    rating = forms.DecimalField(max_digits=3,
                                decimal_places=1,
                                widget=forms.NumberInput(
                                    attrs={
                                        'step': 0.5,
                                        'min': 0,
                                        'max': 10
                                    }
                                )
                                )
    description = forms.CharField(widget=forms.Textarea(attrs={'col': 60, 'rows': 15}), required=True)