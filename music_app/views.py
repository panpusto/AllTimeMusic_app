from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from music_app import forms
from music_app.models import Band, Genre, Musician, Label, Album, MusicianBand, Review


class LandingPageView(View):
    def get(self, request):
        """This function display application main page."""
        return render(
            request,
            'main_page.html',
        )


class UserCreateView(View):
    def get(self, request):
        """This function display form to create new user account."""
        form = forms.UserCreateForm()

        return render(
            request,
            'create_user_form.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        """
        This function save data from create user
        form to database.
        """
        form = forms.UserCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            User.objects.create_user(
                username=data.get('username'),
                password=data.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email')
            )

            return redirect('login')

        else:
            return render(
                request,
                'create_user_form.html',
                context={
                    'form': form
                }
            )


class LoginView(View):
    def get(self, request):
        """This function display form to log in a user."""
        form = forms.LoginForm()
        return render(
            request,
            'login.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        """
        This function log in authenticated user if username and password
        are correct.
        """
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/add-board/')
            else:
                message = f"Incorrect login details"

            return render(
                request,
                'login.html',
                context={
                    'form': form,
                    'message': message
                }
            )
        else:
            return render(
                request,
                'login.html',
                context={
                    'form': form
                }
            )


class LogoutView(View):
    def get(self, request):
        """This function log out a user"""
        if request.user.is_authenticated:
            logout(request)

        return redirect('/')


class PasswordResetView(LoginRequiredMixin, View):
    permission_required = 'auth.change_user'

    def get(self, request, user_id):
        """
        This user display reset password form for logged user.
        Only for logged users.
        """
        form = forms.PasswordResetForm()

        return render(
            request,
            'reset_password.html',
            context={
                'form': form
            }
        )

    def post(self, request, user_id):
        """This function save user's new password to database."""
        user = get_object_or_404(User, id=user_id)
        form = forms.PasswordResetForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            user.set_password(data.get('new_password'))
            user.save()

            return redirect('login')

        else:
            return render(
                request,
                'login.html',
                context={
                    'form': form
                }
            )


class BandsListAlphabeticalView(View):
    """
    This function display list of all bands in database in
    alphabetical order.
    """
    def get(self, request):
        bands = Band.objects.all().order_by('name')
        paginator = Paginator(bands, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'bands_list_alphabet.html',
            context={
                'page_obj': page_obj
            }
        )


class BandsGenresListView(View):
    """This function display list of all genres in database as links."""
    def get(self, request):
        genres = Genre.objects.all().order_by('name')
        paginator = Paginator(genres, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'bands_genres_list.html',
            context={
                'page_obj': page_obj
            }
        )


class BandsListByGenreView(View):
    """This function display list of bands by genres."""
    def get(self, request, _id):
        bands = Band.objects.filter(genre=_id).order_by('name')
        paginator = Paginator(bands, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'bands_list_by_genre.html',
            context={
                'page_obj': page_obj
            }
        )


class BandCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        """
        This function display form to create a new band.
        Only for logged users.
        """
        form = forms.BandCreateForm()

        return render(
            request,
            'band_create_form.html',
            context={
                'form': form,
            }
        )

    def post(self, request):
        """This function save a new band data in database."""
        form = forms.BandCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')
            country_of_origin = data.get('country_of_origin')
            location = data.get('location')
            status = data.get('status')
            formed_in = data.get('formed_in')
            genre = request.POST.getlist('genre')
            lyrical_themes = data.get('lyrical_themes')
            current_label = data.get('current_label')
            bio = data.get('bio')
            label_id = Label.objects.get(id=current_label)

            band = Band.objects.create(name=name,
                                       country_of_origin=country_of_origin,
                                       location=location,
                                       status=status,
                                       formed_in=formed_in,
                                       lyrical_themes=lyrical_themes,
                                       current_label=label_id,
                                       bio=bio,
                                       added_by=request.user)
            band.genre.set(genre)

            return redirect(f'/band/details/{band.id}/')

        return render(
            request,
            'band_create_form.html',
            context={
                'form': form,
            }
        )


class BandDetailsView(View):
    """This function display all data about specific band."""
    def get(self, request, _id):
        band = Band.objects.get(pk=_id)
        musicians = MusicianBand.objects.filter(band_id=_id)
        genres = Genre.objects.filter(band=_id)
        albums = Album.objects.filter(band_id=_id).order_by('release_date')

        return render(
            request,
            'band_details.html',
            context={
                'band': band,
                'genres': genres,
                'albums': albums,
                'musicians': musicians
            }
        )


class BandUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display a form to update data of specific band.
        Only for logged users.
        """
        band = get_object_or_404(Band, id=_id)
        genre_ids = list(band.genre.values_list('id', flat=True))
        form = forms.BandCreateForm(initial={'name': band.name,
                                             'country_of_origin': band.country_of_origin,
                                             'location': band.location,
                                             'status': band.status,
                                             'formed_in': band.formed_in,
                                             'ended_in': band.ended_in,
                                             'genre': genre_ids,
                                             'lyrical_themes': band.lyrical_themes,
                                             'current_label': band.current_label.id,
                                             'bio': band.bio})

        return render(
            request,
            'band_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, _id):
        """This function save updated data about band to database."""
        band = Band.objects.get(id=_id)
        form = forms.BandCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')
            country_of_origin = data.get('country_of_origin')
            location = data.get('location')
            status = data.get('status')
            formed_in = data.get('formed_in')
            genre = request.POST.getlist('genre')
            lyrical_themes = data.get('lyrical_themes')
            current_label = data.get('current_label')
            bio = data.get('bio')
            label_id = Label.objects.get(id=current_label)

            band.name = name
            band.country_of_origin = country_of_origin
            band.location = location
            band.status = status
            band.formed_in = formed_in
            band.lyrical_themes = lyrical_themes
            band.current_label = label_id
            band.bio = bio
            band.added_by = request.user
            band.genre.set(genre)
            band.save()

            return redirect(f'/band/details/{_id}/')

        else:
            return render(
                request,
                'band_create_form.html',
                context={
                    'form': form
                }
            )


class BandDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function delete band data from database.
        Only for logged users.
        """
        Band.objects.get(pk=_id).delete()

        return redirect('/')


class BandDeleteConfirmView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display confirmation question before delete
        band data from database.
        Only for logged users.
        """
        band = Band.objects.get(pk=_id)
        return render(
            request,
            'band_delete_confirm.html',
            context={
                'band': band
            }
        )


class MusicianDetailsView(View):
    def get(self, request, _id):
        """This function display all data about specific musician."""
        musician = Musician.objects.get(musicianband=_id)
        # bands = MusicianBand.objects.filter(musician_id=_id)

        return render(
            request,
            'musician_details.html',
            context={
                'musician': musician,
                # 'bands': bands
            }
        )


class MusicianCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        """
        This function display form to create a new musician.
        Only for logged users.
        """
        form = forms.MusicianCreateForm()

        return render(
            request,
            'musician_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        """This function save a new musician data to database"""
        form = forms.MusicianCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')
            full_name = data.get('full_name')
            born = data.get('born')
            died = data.get('died')
            place_of_birth = data.get('place_of_birth')
            bio = data.get('bio')

            if Musician.objects.filter(name=name).exists() and Musician.objects.filter(full_name=full_name).exists():
                message = 'This musician already exists in database. You can update it!'
                return render(
                    request,
                    'musician_create_form.html',
                    context={
                        'form': form,
                        'message': message
                    }
                )

            Musician.objects.create(
                name=name,
                full_name=full_name,
                born=born,
                died=died,
                place_of_birth=place_of_birth,
                bio=bio,
                added_by=request.user)

            return redirect('add-board')

        else:
            return render(
                request,
                'musician_create_form.html',
                context={
                    'form': form
                }
            )


class MusicianUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display form to update musician data.
        Only for logged users.
        """
        musician = get_object_or_404(Musician, id=_id)
        form = forms.MusicianCreateForm(initial={'name': musician.name,
                                                 'full_name': musician.full_name,
                                                 'born': musician.born,
                                                 'died': musician.died,
                                                 'place_of_birth': musician.place_of_birth,
                                                 'bio': musician.bio
                                                 })

        return render(
            request,
            'musician_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, _id):
        """This function save updated musician data to database."""
        musician = Musician.objects.get(pk=_id)
        form = forms.MusicianCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')
            full_name = data.get('full_name')
            born = data.get('born')
            died = data.get('died')
            place_of_birth = data.get('place_of_birth')
            bio = data.get('bio')

            musician.name = name
            musician.full_name = full_name
            musician.born = born
            musician.died = died
            musician.place_of_birth = place_of_birth
            musician.bio = bio
            musician.save()

            return redirect('/')

        else:
            return render(
                request,
                'musician_create_form.html',
                context={
                    'form': form
                }
            )


class MusicianDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function delete musician data from database.
        Only for logged users.
        """
        Musician.objects.get(id=_id).delete()

        return redirect('/')


class MusicianDeleteConfirmView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display confirmation question before
        delete band data from database.
        Only for logged users.
        """
        musician = Musician.objects.get(id=_id)
        return render(
            request,
            'musician_delete_confirm.html',
            context={
                'musician': musician
            }
        )


class LabelCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        """
        This function display form to create new label data.
        Only for logged users.
        """
        form = forms.LabelCreateForm()

        return render(
            request,
            'label_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        """This function save new label data to database."""
        form = forms.LabelCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')
            address = data.get('address')
            country = data.get('country')
            status = data.get('status')
            styles = data.get('styles')
            founding_year = data.get('founding_year')

            if Label.objects.filter(name=name).exists():
                message = "This label already exists in database. You can update it!"
                return render(
                    request,
                    'label_create_form.html',
                    context={
                        'form': form,
                        'message': message
                    }
                )

            Label.objects.create(
                name=name,
                address=address,
                country=country,
                status=status,
                styles=styles,
                founding_year=founding_year,
                added_by=request.user
            )

            return redirect('add-board')

        else:
            return render(
                request,
                'label_create_form.html',
                context={
                    'form': form
                }
            )


class LabelDetailsView(View):
    def get(self, request, _id):
        """This function display all details about specific label."""
        label = Label.objects.get(pk=_id)

        return render(
            request,
            'label_details.html',
            context={
                'label': label
            }
        )


class LabelUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display form to update data about specific label.
        Only for logged users.
        """
        label = get_object_or_404(Label, pk=_id)
        form = forms.LabelCreateForm(initial={'name': label.name,
                                              'address': label.address,
                                              'country': label.country,
                                              'status': label.status,
                                              'styles': label.styles,
                                              'founding_year': label.founding_year
                                              })

        return render(
            request,
            'label_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, _id):
        """This function save updated label data to database."""
        label = Label.objects.get(pk=_id)
        form = forms.LabelCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')
            address = data.get('address')
            country = data.get('country')
            status = data.get('status')
            styles = data.get('styles')
            founding_year = data.get('founding_year')

            label.name = name
            label.address = address
            label.country = country
            label.status = status
            label.styles = styles
            label.founding_year = founding_year
            label.save()

            return redirect('/')

        else:
            return render(
                request,
                'label_create_form.html',
                context={
                    'form': form
                }
            )


class LabelListView(View):
    def get(self, request):
        """
        This function display list of all labels in database
        in alphabetical order.
        """
        labels = Label.objects.all().order_by('name')
        paginator = Paginator(labels, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'labels_list.html',
            context={
                'page_obj': page_obj
            }
        )


class LabelDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function delete specific label from database.
        Only for logged users.
        """
        Label.objects.get(id=_id).delete()

        return redirect('/')


class LabelDeleteConfirmView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display confirmation question
        before delete specific label from database.
        Only for logged users.
        """
        label = Label.objects.get(id=_id)
        return render(
            request,
            'label_delete_confirm.html',
            context={
                'label': label
            }
        )


class AlbumLastAddedView(View):
    def get(self, request):
        """
        This function display list of all albums
        ordered by date of adding descending.
        """
        albums = Album.objects.all().order_by('-added')
        paginator = Paginator(albums, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'albums_last_added.html',
            context={
                'page_obj': page_obj
            }
        )


class AlbumDetailsView(View):
    def get(self, request, album_id):
        """This function display all data about specific album."""
        album = Album.objects.get(pk=album_id)
        return render(
            request,
            'album_details.html',
            context={
                'album': album,
            }
        )


class AlbumCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        """
        This function display a form to create a new album.
        Only for logged users.
        """
        form = forms.AlbumCreateForm()

        return render(
            request,
            'album_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        """This function save new album data in database."""
        form = forms.AlbumCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            title = data.get('title')
            band = data.get('band')
            genre = request.POST.getlist('genre')
            type_record = data.get('type')
            release_date = data.get('release_date')
            catalog_id = data.get('catalog_id')
            label = data.get('label')
            format_music = data.get('format')

            label_id = Label.objects.get(id=label)
            band_id = Band.objects.get(id=band)

            if Album.objects.filter(title=title).exists():
                message = 'This album already exists in database!'
                return render(
                    request,
                    'album_create_form.html',
                    context={
                        'form': form,
                        'message': message
                    }
                )

            album = Album.objects.create(
                title=title,
                band=band_id,
                type=type_record,
                release_date=release_date,
                catalog_id=catalog_id,
                label=label_id,
                format=format_music,
                added_by=request.user
            )

            album.genre.set(genre)

            return redirect(f'/album/details/{album.id}/')

        else:
            return render(
                request,
                'album_create_form.html',
                context={
                    'form': form
                }
            )


class AlbumUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display form to update album data.
        Only for logged users.
        """
        album = get_object_or_404(Album, pk=_id)
        genre_ids = list(album.genre.values_list('id', flat=True))
        form = forms.AlbumCreateForm(initial={'title': album.title,
                                              'band': album.band.id,
                                              'genre': genre_ids,
                                              'type': album.type,
                                              'release_date': album.release_date,
                                              'catalog_id': album.catalog_id,
                                              'label': album.label.id,
                                              'format': album.format
                                              })

        return render(
            request,
            'album_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, _id):
        """This function save updated album data to database."""
        album = Album.objects.get(pk=_id)
        form = forms.AlbumCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            title = data.get('title')
            band = data.get('band')
            genre = request.POST.getlist('genre')
            type_record = data.get('type')
            release_date = data.get('release_date')
            catalog_id = data.get('catalog_id')
            label = data.get('label')
            format = data.get('format')

            band_id = Band.objects.get(id=band)
            label_id = Label.objects.get(id=label)

            album.title = title
            album.band = band_id
            album.type = type_record
            album.release_date = release_date
            album.catalog_id = catalog_id
            album.label = label_id
            album.format = format
            album.added_by = request.user
            album.genre.set(genre)
            album.save()

            return redirect('/')

        else:
            return render(
                request,
                'album_create_form.html',
                context={
                    'form': form
                }
            )


class AlbumDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function delete album from database.
        Only for logged users.
        """
        Album.objects.get(id=_id).delete()

        return redirect('/')


class AlbumDeleteConfirmView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display a confirmation question
        before delete specific album from database.
        Only for logged users.
        """
        album = Album.objects.get(id=_id)
        return render(
            request,
            'album_delete_confirm.html',
            context={
                'album': album
            }
        )


class GenreCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        """
        This function display form to create new genre.
        Only for logged users.
        """
        genres = Genre.objects.all().order_by('name')
        form = forms.GenreCreateForm()

        return render(
            request,
            'genre_create_form.html',
            context={
                'form': form,
                'genres': genres
            }
        )

    def post(self, request):
        """This function save new genre data to database."""
        form = forms.GenreCreateForm(request.POST)
        genres = Genre.objects.all().order_by('name')

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')

            if Genre.objects.filter(name=name).exists():
                message = "This genre already exists!"
                return render(
                    request,
                    'genre_create_form.html',
                    context={
                        'form': form,
                        'message': message,
                        'genres': genres
                    }
                )
            Genre.objects.create(name=name)

            return redirect('add-board')

        else:
            return render(
                request,
                'genre_create_form.html',
                context={
                    'form': form
                }
            )


class GenreUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display form to update genre data.
        Only for logged users.
        """
        genre = get_object_or_404(Genre, pk=_id)
        form = forms.GenreCreateForm(initial={'name': genre.name})

        return render(
            request,
            'genre_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, _id):
        """This function save updated genre data to database"""
        genre = Genre.objects.get(pk=_id)
        form = forms.GenreCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            name = data.get('name')

            genre.name = name
            genre.save()

            return redirect('/bands/genres/')

        else:
            return render(
                request,
                'genre_create_form.html',
                context={
                    'form': form
                }
            )


class GenreDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function delete specific genre from database.
        Only for logged users.
        """
        Genre.objects.get(id=_id).delete()

        return redirect('/bands/genres/')


class GenreDeleteConfirmView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display confirmation question
        before delete specific genre from database.
        Only for logged users.
        """
        genre = Genre.objects.get(id=_id)
        return render(
            request,
            'genre_delete_confirm.html',
            context={
                'genre': genre
            }
        )


class ReviewCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, album_id, band_id):
        """
        This function display a form to create album review.
        Only for logged users.
        """
        album = Album.objects.get(pk=album_id)
        band = Band.objects.get(pk=band_id)
        form = forms.ReviewCreateForm()

        return render(
            request,
            'review_create_form.html',
            context={
                'form': form,
                'album': album,
                'band': band
            }
        )

    def post(self, request, album_id, band_id):
        """This form save album review data to database."""
        album = Album.objects.get(pk=album_id)
        band = Band.objects.get(pk=band_id)
        form = forms.ReviewCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            subject = data.get('subject')
            title = album.id
            band_name = band.id
            rating = data.get('rating')
            description = data.get('description')

            Review.objects.create(
                subject=subject,
                album_id=title,
                band_id=band_name,
                rating=rating,
                description=description,
                user=request.user
            )

            return redirect(f'/band/details/{band_id}')

        else:
            return render(
                request,
                'review_create_form.html',
                context={
                    'form': form,
                    'album': album,
                    'band': band
                }
            )


class AddMusicianToBand(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        """
        This function display a form to add musician to specific band.
        Only for logged users.
        """
        form = forms.AddMusicianToBandForm()

        return render(
            request,
            'add_musician_to_band.html',
            context={
                'form': form
            }
        )

    def post(self, request):
        """
        This function save adding musician to band data
        to database.
        """
        form = forms.AddMusicianToBandForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            musician = data.get('musician')
            band = data.get('band')
            year_from = data.get('year_from')
            year_to = data.get('year_to')
            role = data.get('role')

            MusicianBand.objects.create(
                musician_id=musician,
                band_id=band,
                year_from=year_from,
                year_to=year_to,
                role=role
            )

            return redirect('add-board')

        else:
            return render(
                request,
                'add_musician_to_band.html',
                context={
                    'form': form
                }
            )


class DeleteMusicianFromBandView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function delete musician data from band.
        Only for logged users.
        """
        MusicianBand.objects.get(id=_id).delete()

        return redirect('/')


class DeleteMusicianFromBandConfirmView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display confirmation question
        before delete musician from band.
        Only for logged users.
        """
        musician = MusicianBand.objects.get(id=_id)
        return render(
            request,
            'musician_band_delete_confirm.html',
            context={
                'musician': musician
            }
        )


class ReviewsListView(View):
    def get(self, request):
        """
        This function display a list of all reviews
        ordered by adding date descending.
        """
        reviews = Review.objects.all().order_by('-added')
        paginator = Paginator(reviews, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'reviews_list.html',
            context={
                'page_obj': page_obj
            }
        )


class ReviewDetailsView(View):
    def get(self, request, _id):
        """This function display all details about specific review."""
        review = Review.objects.get(pk=_id)

        return render(
            request,
            'review_details.html',
            context={
                'review': review
            }
        )


class ReviewUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display form to update review data.
        Only for logged users.
        """
        review = get_object_or_404(Review, pk=_id)
        form = forms.ReviewCreateForm(initial={'subject': review.subject,
                                               'album': review.album,
                                               'band': review.band,
                                               'description': review.description,
                                               'rating': review.rating})

        return render(
            request,
            'review_create_form.html',
            context={
                'form': form
            }
        )

    def post(self, request, _id):
        """
        This form save updated review data to database.
        Only for logged users.
        """
        review = Review.objects.get(pk=_id)
        form = forms.ReviewCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            subject = data.get('subject')
            description = data.get('description')
            rating = data.get('rating')
            user = request.user

            review.subject = subject
            review.description = description
            review.rating = rating
            review.user = user
            review.save()

            return redirect('reviews-list')

        else:
            return render(
                request,
                'review_create_form.html',
                context={
                    'form': form
                }
            )


class ReviewDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function delete review data from database.
        Only for logged users.
        """
        Review.objects.get(id=_id).delete()

        return redirect('reviews-list')


class ReviewDeleteConfirmView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, _id):
        """
        This function display confirmation question
        before delete review data from database.
        Only for logged users.
        """
        review = Review.objects.get(id=_id)
        return render(
            request,
            'review_delete_confirm.html',
            context={
                'review': review
            }
        )


class AddMusicDataView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        """This function display board with adding options, only for logged users."""
        return render(
            request,
            'add_board.html',
        )


def search_band(request):
    """This function searching a band by name."""
    band = Band.objects.all()
    searching_band = request.GET['query']

    if searching_band:
        band = Band.objects.filter(name__icontains=searching_band)

        if not band:
            message = "No results"

            return render(
                request,
                'searching-results.html',
                context={
                    'band': band,
                    'message': message
                }
            )

        return render(
            request,
            'searching-results.html',
            context={
                'band': band,
            }
        ),

    return render(
        request,
        'searching-results.html',
        context={
            'message': 'Type a band name before searching.'
        }
    )

