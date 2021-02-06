from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
from project_string.users.forms import RegistrationForm, LoginForm, RequestResetForm, UpdateAccountForm
from project_string.config import firebase
from firebase_admin import auth

users = Blueprint('users', __name__)

@users.route("/register", methods = ['GET', 'POST'])
def register():
    try:
        if session['usr']:
            return redirect(url_for('main.home'))
    except:
        form = RegistrationForm()
        if form.validate_on_submit():
            # user = firebase.auth().create_user_with_email_and_password(form.email.data, form.password.data)
            # firebase.auth().send_email_verification(user['idToken'])
            # flash(f'An email is send to your email-id to verfisy your account', 'success')
            # return redirect(url_for('users.register'))
            
            try:
                user = firebase.auth().create_user_with_email_and_password(form.email.data, form.password.data)
                firebase.auth().send_email_verification(user['idToken'])
                flash(f'An email is send to your email-id to verfisy your account', 'success')
                return redirect(url_for('users.register'))
            except:
                flash(f'Email is already is in use.', 'danger')
                return redirect(url_for('users.register')) 
            
    return render_template('register.html', title = "Register", form = form)



@users.route("/login", methods = ['GET', 'POST'])
def login():
    try:
        if session['usr']:
            return redirect(url_for('main.home'))
    except:
        form = LoginForm()
        if form.validate_on_submit():
            try:
                user = firebase.auth().sign_in_with_email_and_password(form.email.data, form.password.data)
                user_info = firebase.auth().get_account_info(user['idToken'])
                firebase.auth().send_email_verification(user['idToken'])
                if user_info['users'][0]['emailVerified'] == False:
                    flash(f'You have not verified your mail yet.', 'danger')
                    firebase.auth().send_email_verification(user['idToken'])
                    flash(f'An email is send to your email-id to verfisy your account', 'success')
                    return redirect(url_for('users.login'))
                else:
                    session['usr'] = user
                    session['email'] = form.email.data
                
                next_page = request.args.get('next')       
                #print("the current user id ", firebase.auth().current_user['loaclId'])     
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            except:
                flash('Invalid credentials.', 'danger')   
    return render_template('login.html', title = "Login", form = form)




@users.route("/account", methods = ['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    return render_template('account.html', title = 'Account', form = form)



@users.route("/logout")
def logout():
    firebase.auth().current_user = None
    session.clear()
    return redirect(url_for('main.home'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        try:
            firebase.auth().send_password_reset_email(form.email.data)
            flash(f'An email has been sent to your email-id to reset your password', 'success')
            return redirect(url_for('users.reset_request'))
        except:
            flash(f'Email not found', 'danger')
            return redirect(url_for('users.forgot_password'))
    return render_template('reset_request.html', title='Reset Password', form=form)

