# run.py
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from app import create_app, db
from flask_migrate import Migrate
from app.models import BlogPost, Category, Tag 
import os
import markdown
import frontmatter

# Create log directory if not exists
LOG_DIR = "log"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
log_filename = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logging.basicConfig(
    level=logging.ERROR,  # Log only errors or higher
    format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger()

app = create_app()

# Optional: Shell context for flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'BlogPost': BlogPost,
        'Category': Category,
        'Tag': Tag
    }

POSTS_DIR = 'app/blog/posts/'

def load_posts():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                post_data = frontmatter.load(f)
                html_content = markdown.markdown(post_data.content)
                posts.append({
                    'slug': filename[:-3],  # Remove '.md' extension
                    'title': post_data.get('title', 'Untitled'),
                    'date': post_data.get('date', ''),
                    'author': post_data.get('author', ''),
                    'content': html_content
                })
    # Sort posts by date (optional)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

if __name__ == '__main__':
        app.run(debug=True)
