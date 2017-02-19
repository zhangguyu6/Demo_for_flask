from ..models import Post,Category,db
from flask import flash,current_app,render_template,request,redirect,url_for
from . import main
from .forms import PostForm
from flask_login import login_required



@main.route('/',methods=['GET','POST'])
def index():
    post=Post.query.order_by(Post.timestamp.desc()).first()
    return render_template('index.html',post=post)

@main.route('/articles',methods=['GET','POST'])
def articles():
    #查询字符串的格式是/?key=value
    page=request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts=pagination.items
    return render_template('atricles.html',posts=posts,pagination=pagination)


@main.route('/post/<int:id>')
def post(id):
    post=Post.query.get_or_404(id)
    if not post.view_times:
        post.view_times=1
    else:
        post.view_times+=1
    db.session.add(post)
    db.session.commit()
    return render_template('post.html',posts=[post])


@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post=Post.query.get_or_404(id)

    if post.category_id:
        category=Category.query.get_or_404(post.category_id)

    form=PostForm()

    if form.validate_on_submit():
        post.title=form.title.data
        post.into=form.into.data
        post.body=form.body.data
        if form.category_name.data:
            category_name_exits=Category.query.filter_by\
                (category_name=form.category_name.data).first()
            if not category_name_exits:

                category=Category(category_name=form.category_name.data)
                db.session.add(category)
                db.session.commit()
                post.category_id=category.id
            else:
                post.category_id=category_name_exits.id

        db.session.add(post)
        db.session.commit()
        flash("编辑的文章已提交")
        return redirect(url_for('.post',id=post.id))
    form.title.data=post.title
    form.into.data=post.into
    form.body.data=post.body
    if post.category_id:
        category=Category.query.filter_by(id=post.category_id).first()
        form.category_name.data=category.category_name
    return render_template('edit_post.html',form=form)


@main.route('/new',methods=['GET','POST'])
@login_required
def new():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,into=form.into.data,body=form.body.data)
        if form.category_name.data:
            category=Category(category_name=form.category_name.data)
            post.category_id=category.id
            db.session.add(category)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.articles'))
    return render_template('new.html',form=form)


@main.route('/delete/<int:id>')
@login_required
def delete(id):
    post=Post.query.get_or_404(id)
    flash('文章{}已删除'.format(post.title))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.articles'))
