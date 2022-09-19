from rest_framework import serializers

from music_app.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
        )