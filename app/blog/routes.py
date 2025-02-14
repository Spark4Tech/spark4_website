# blog/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from app import blog
from app import db
from app.models import BlogPost, Category, Author, Tag
from app.blog.forms import BlogPostForm
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload

blog = Blueprint('blog', __name__, template_folder='templates')  # Specify template folder

@blog.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=10)
    print('Blog index route called')
    print(f"Number of posts: {len(posts.items)}")
    for post in posts.items:
        print(f"Post: {post.title}, Published: {post.published}")
    return render_template('blog_index.html', posts=posts)

@blog.route('/<slug>')
def post(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).options(selectinload(BlogPost.category)).first_or_404()
    return render_template('post.html', post=post)

@blog.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(category=category, published=True).order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('category.html', category=category, posts=posts)

@blog.route('/new', methods=['GET', 'POST'])
def new_post():
    form = BlogPostForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.author.choices = [(a.id, a.name) for a in Author.query.all()]
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            excerpt=form.excerpt.data,
            author_id=form.author.data,
            category_id=form.category.data,
            published=form.published.data,
            featured_image=form.featured_image.data,
            inside_image=form.inside_image.data
        )
        post.generate_slug()
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('blog.index'))
    return render_template('blog/new_post.html', form=form)

@blog.route('/tag/<slug>')
def tag(slug):
    tag = Tag.query.filter(Tag.name.ilike(slug)).first_or_404()
    posts = BlogPost.query.filter(
        BlogPost.tags.contains(tag),
        BlogPost.published == True
    ).order_by(BlogPost.created_at.desc()).all()
    return render_template('tag.html', tag=tag, posts=posts)

# Add more routes as needed (edit, delete, etc.)
