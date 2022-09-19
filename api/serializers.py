from rest_framework import serializers

from music_app.models import (
    Genre,
    Label,
    Musician,
    Band,
    Album,
    Review,
    MusicianBand,
    LABEL_STATUS,
    BAND_STATUS,
    ALBUM_TYPES,
    FORMAT_TYPES,
)


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
        )
        model = Genre


class LabelSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=LABEL_STATUS)

    class Meta:
        fields = (
            'id',
            'name',
            'address',
            'country',
            'status',
            'styles',
            'founding_year',
        )
        model = Label


class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'full_name',
            'born',
            'died',
            'place_of_birth',
            'bio',
        )
        model = Musician


class BandSerializer(serializers.ModelSerializer):
    status = ChoiceField(choices=BAND_STATUS)
    current_label = serializers.CharField(source='current_label.name')
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        fields = (
            'id',
            'name',
            'country_of_origin',
            'location',
            'status',
            'formed_in',
            'ended_in',
            'genre',
            'lyrical_themes',
            'bio',
            'current_label',
        )
        model = Band


class AlbumSerializer(serializers.ModelSerializer):
    type = ChoiceField(choices=ALBUM_TYPES)
    format = ChoiceField(choices=FORMAT_TYPES)
    band = serializers.CharField(source='band.name')
    label = serializers.CharField(source='label.name')
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        fields = (
            'id',
            'title',
            'genre',
            'type',
            'release_date',
            'catalog_id',
            'format',
            'band',
            'label',
        )
        model = Album


class ReviewSerializer(serializers.ModelSerializer):
    album = serializers.CharField(source='album.title')
    band = serializers.CharField(source='band.name')
    user = serializers.CharField(source='user.username')

    class Meta:
        fields = (
            'id',
            'subject',
            'rating',
            'description',
            'album',
            'band',
            'user',
        )
        model = Review


class MusicianBandSerializer(serializers.ModelSerializer):
    band = serializers.CharField(source='band.name')
    real_name = serializers.CharField(source='musician.full_name')
    nickname = serializers.CharField(source='musician.name')

    class Meta:
        fields = (
            'id',
            'year_from',
            'year_to',
            'role',
            'band',
            'real_name',
            'nickname',
        )
        model = MusicianBand


