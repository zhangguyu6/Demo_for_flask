from . import auth
from flask import render_template,redirect,request,url_for,flash
from .forms import LoginForm
from ..models import Administrator
from flask import current_app
from flask_login import login_user,login_required,logout_user


@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=Administrator.query.filter_by(email=form.email.data).first()

        if user is not None and form.password.data==current_app.config['PASSWORD']:
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('个人博客，高手勿扰')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出')
    return redirect(url_for('main.index'))