"""
This is a draft implementation of adding partners to the database.
ToDo Needs to be modified or built into an existing system.
"""
from flask import render_template, request, abort, flash, redirect, url_for

from app.main import main
from app.models import insert_or_update
from app.models.partner import Partner


@main.route('/register', methods=['POST', 'GET'])
def register():
    """Form for partner registration in the system."""
    if request.method == 'POST':
        login = request.form.get('login', None)
        password = request.form.get('password', None)
        # ToDo Should be replaced - implemented as an example
        if login != '2@2.com' or password != 'vasyaPupkin123':
            return abort(401, {'msg': 'Bad username or password'})

        partner = Partner(
            email=request.form.get('email'),
            psw=request.form.get('psw'),
            websites_name=request.form.get('websites_name'),
        )
        result, partner = insert_or_update(partner)
        if not result:
            flash('Something went wrong. Our programmers have been notified.')
            return redirect(url_for('register'))

        flash(f'Partner successfully added: {partner}')

    return render_template('register.html')
