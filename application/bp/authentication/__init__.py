from flask import Blueprint, render_template, redirect, url_for, flash

from application.database import User, db
from application.bp.authentication.forms import RegisterForm

authentication = Blueprint('authentication', __name__, template_folder='templates')
@authentication.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username='TestUser')

@authentication.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('authentication.registration'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)  # Assuming set_password hashes the password
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('authentication.dashboard'))

    return render_template('register.html', form=form)
