from flask import Blueprint, render_template, abort
from sqlalchemy import select
from app.models import BlogPost
from app.blog.routes import blog
import app

blog = Blueprint('blog', __name__)