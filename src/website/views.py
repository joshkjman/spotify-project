from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from playlist_sorter.spotify_home import get_top_5


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    token = session['access_token']
    top_5_artists = get_top_5(token, 'artists')
    top_5_tracks = get_top_5(token, 'tracks')

    return render_template("home.html", user=current_user, artists=top_5_artists, tracks=top_5_tracks)
