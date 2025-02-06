from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os
import urllib.parse
import requests
from datetime import datetime
from playlist_sorter.get_playlist import playlist_songs
from playlist_sorter.merge_csvs import get_kaggle_data, join_data
from playlist_sorter.sorter import scale_songs, fit_PCA, show_elbow_plot, show_cluster
from playlist_sorter.create_playlists import get_user_id, create_playlist_return_id, add_songs_playlist
from playlist_sorter.KMeans import KMeans
from dotenv import load_dotenv


load_dotenv()


client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = 'http://localhost:5000/callback'


auth_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
api_base_url = 'https://api.spotify.com/v1/'


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True) # remembers login details until server is restarted
                return redirect('/authorize')
            else:
                flash('Incorrect password, try again', category='error')

        else:
            flash('Email doesn\'t exist, please sign up.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Password must match.', category='error')
        elif len(password1) < 7:
            flash('Passowrd must be greater than 6 characters.', category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/authorize')
def authorize_and_token():
    scope = 'user-read-private user-read-email playlist-modify-private playlist-modify-public'

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True
    }

    authorize_url = f'{auth_url}?{urllib.parse.urlencode(params)}'

    return redirect(authorize_url)


@auth.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})

    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(token_url, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect(url_for('views.home'))
    

@auth.route('/playlists', methods=['GET', 'POST'])
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    token = session['access_token']
    playlist_id = '6psFok7zOHD54A3dLFNN5h'
    
    kaggle_data = get_kaggle_data()
    all_tracks = playlist_songs(token, playlist_id)
    tracks_all_analysis = join_data(kaggle_data, all_tracks)
    songs = scale_songs(tracks_all_analysis)
    x_df = fit_PCA(songs)
    data_plot = show_elbow_plot(x_df, KMeans)
    
    # user_id = get_user_id(token)
    # response = create_playlist(token, user_id)

    if request.method == 'POST':
        n_clusters = request.form.get('playlist_sorter')
        print(n_clusters)
        # kmeans = KMeans(n_clusters=n_clusters)
        # kmeans.fit(x_df)
        # songs_with_label = songs.join(x_df)

        # user_id = get_user_id(token)
        
        # for cluster in range(n_clusters):
        #     songs_by_label = songs_with_label[songs_with_label['label'] == cluster]

        #     song_uris = []
        #     for _, row in songs_by_label.iterrows():
        #         song_uri = row['uri']
        #         song_uris.append(song_uri)

        #     print(song_uris)
        #     playlist_id = create_playlist_return_id(token, user_id, cluster)
        #     add_songs_playlist(token, playlist_id, song_uris)


    return render_template("playlists.html", user=current_user, data=data_plot)


@auth.route('/refresh-token')
def refresh_token():
    if 'refresh-token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret
        }

    response = requests.post(token_url, data=req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return redirect('/playlists')