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
            flash('Already Registered', 'danger')
            return redirect(url_for('authentication.registration'))

        # Use the updated create method to create the user
        new_user = User.create(form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('authentication.dashboard'))

    return render_template('registration.html', form=form)
