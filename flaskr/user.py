from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('user', __name__, url_prefix='/user')



@bp.route('/<int:id>', methods=('GET',))
@login_required
def user_profile(id):
    db = get_db()
    user = db.execute('SELECT id, username, email, bio, created FROM user WHERE id = ?',
                      (id,)).fetchone()
    if user is None:
        abort(404)

    return render_template('user/profile.html', user=user)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_profile(id):
    if g.user['id'] != id:
        abort(403)

    db = get_db()

    if request.method == 'POST':
        email = request.form['email']
        bio = request.form['bio']


        error = None
        if email and '@' not in email:
            error = 'Incorrect email.'

        if error:
            flash(error)
        else:
            db.execute(
                'UPDATE user SET email = ?, bio = ? WHERE id = ?',
                (email, bio, id)
            )
            db.commit()
            flash('Profile updated.')
            return redirect(url_for('user.edit_profile', id=id))


    user = db.execute(
        'SELECT username, email, bio FROM user WHERE id = ?',
        (id,)
    ).fetchone()
    if user is None:
        abort(404)

    return render_template('user/edit_profile.html', user=user)



