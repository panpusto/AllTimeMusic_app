from django.contrib import admin

from music_app.models import Genre, Label, Musician, Band, Album, Review, MusicianBand


admin.site.register(Genre)
admin.site.register(Label)
admin.site.register(Musician)
admin.site.register(Band)
admin.site.register(Album)
admin.site.register(Review)
admin.site.register(MusicianBand)
