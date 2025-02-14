import os
import logging
from datetime import datetime, timezone
import markdown
import json5
import subprocess
from markdown.extensions.extra import ExtraExtension
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from app import db, create_app
from app.models import Author, Category, BlogPost, Tag, BlogPostData, post_tags

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('blog_import.log')
    ]
)
logger = logging.getLogger(__name__)

POSTS_DIR = 'app/blog/posts/'

class LineBreakPreprocessor(Preprocessor):
    """Preprocessor for handling line breaks in markdown."""
    def run(self, lines):
        new_lines = []
        for line in lines:
            line = line.rstrip()
            if line.endswith('  '):
                new_lines.append(line[:-2] + '<br />')
            elif line:
                new_lines.append(line + '  ')
            else:
                new_lines.append(line)
        return new_lines

class LineBreakExtension(Extension):
    """Extension for handling line breaks in markdown."""
    def extendMarkdown(self, md):
        md.preprocessors.register(LineBreakPreprocessor(md), 'linebreaks', 175)

class NewTabLinksTreeprocessor(Treeprocessor):
    """Adds target="_blank" to all links."""
    def run(self, root):
        for link in root.iter('a'):
            link.set('target', '_blank')
        return root

class NewTabLinksExtension(Extension):
    """Extension for adding target="_blank" to links."""
    def extendMarkdown(self, md):
        md.treeprocessors.register(NewTabLinksTreeprocessor(md), 'newtablinks', 15)

def convert_markdown_to_html(content):
    """Convert markdown content to HTML with specified extensions."""
    extensions = [
        ExtraExtension(),
        LineBreakExtension(),
        'markdown.extensions.nl2br',
        NewTabLinksExtension()
    ]
    return markdown.markdown(content, extensions=extensions)

# TODO: enhance and incorporate this logic
def backup_database():
    """Create a backup before clearing tables."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_{timestamp}.sql'
        
        # Using pg_dump for PostgreSQL backup
        subprocess.run([
            'pg_dump',
            '-h', 'localhost',
            '-U', 'your_db_user',
            '-d', 'your_db_name',
            '-f', backup_file
        ], check=True)
        
        logger.info(f"Created database backup: {backup_file}")
        return True
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return False

def verify_image_files(post_data):
    """Verify all referenced images exist."""
    images = [
        post_data.featured_image,
        post_data.inside_image
    ]
    for img_path in images:
        if img_path and not os.path.exists(os.path.join('app/static/', img_path)):
            logger.warning(f"Image not found: {img_path}")
            return False
    return True

def safe_clear_tables():
    """Safely clear all related tables."""
    try:
        with db.session.begin_nested():
            db.session.execute(post_tags.delete())
            BlogPost.query.delete()
            Tag.query.delete()
            logger.info("Successfully cleared all related tables.")
            return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to clear tables: {str(e)}")
        return False

def create_initial_data():
    """Create initial author and categories if they don't exist."""
    try:
        # Create default author
        author_name = "Spark4 Technology"
        author_email = "blog@spark4.tech"
        
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name, email=author_email)
            db.session.add(author)
            db.session.commit()
            logger.info(f"Created default author: {author_name}")

        # Create default categories
        categories = ["Fitness", "Physical Therapy", "Nutrition", "Cognitive Health"]
        for category_name in categories:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name, slug=slugify(category_name))
                db.session.add(category)
                logger.info(f"Added category: {category_name}")
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating initial data: {str(e)}")
        return False

def process_post(filename, post_data):
    """Process a single blog post."""
    try:
        # Validate post data
        content_path = os.path.join(POSTS_DIR, post_data['content_file'])
        if not os.path.exists(content_path):
            logger.error(f"Content file not found: {content_path}")
            return None

        with open(content_path, 'r', encoding='utf-8') as f:
            post_data['content'] = f.read()

        post_data = BlogPostData.from_dict(post_data)
        
        # Verify images exist
        #if not verify_image_files(post_data):
        #    logger.error(f"Image verification failed for post: {post_data.title}")
        #    return None

        # Parse date
        try:
            date = datetime.strptime(post_data.date, '%Y-%m-%d')
            date = date.replace(tzinfo=timezone.utc)
        except ValueError:
            date = datetime.now(timezone.utc)
            logger.warning(f"Invalid date format in {filename}, using current date")

        # Get or create author and category
        author = Author.query.filter_by(name=post_data.author).first()
        if not author:
            author = Author(name=post_data.author, email=f"{slugify(post_data.author)}@example.com")
            db.session.add(author)
            db.session.flush()

        category = Category.query.filter_by(name=post_data.category).first()
        if not category:
            category = Category(name=post_data.category, slug=slugify(post_data.category))
            db.session.add(category)
            db.session.flush()

        # Create post
        post = BlogPost(
            title=post_data.title,
            slug=slugify(post_data.title),
            content=convert_markdown_to_html(post_data.content),
            excerpt=post_data.excerpt or extract_excerpt(post_data.content),
            created_at=date,
            updated_at=date,
            published=post_data.published,
            author=author,
            category=category,
            featured_image=post_data.featured_image,
            featured_image_alt=post_data.featured_image_alt,
            inside_image=post_data.inside_image,
            inside_image_alt=post_data.inside_image_alt,
            featured_image_caption=post_data.featured_image_caption,
            inside_image_caption=post_data.inside_image_caption
        )
        
        db.session.add(post)
        db.session.flush()

        # Process tags
        for tag_name in post_data.tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            post.tags.append(tag)

        return post

    except Exception as e:
        logger.error(f"Error processing post {filename}: {str(e)}")
        raise

def load_posts(clear_existing=False):
    """Load all blog posts from json5 files."""
    try:
        if clear_existing:
            if not safe_clear_tables():
                logger.error("Failed to clear tables safely, aborting operation")
                return []

        if not create_initial_data():
            logger.error("Failed to create initial data, aborting operation")
            return []
        
        loaded_posts = []
        json_files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.json5')]
        logger.info(f"Found {len(json_files)} post files to process")

        for filename in json_files:
            json_path = os.path.join(POSTS_DIR, filename)
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    post_data = json5.load(f)
                
                post = process_post(filename, post_data)
                if post:
                    loaded_posts.append(post)
                    logger.info(f"Successfully processed post: {post.title}")
                    db.session.commit()
                    
            except IntegrityError:
                db.session.rollback()
                logger.error(f"Database integrity error processing {filename}")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error processing file {filename}: {str(e)}")

        logger.info(f"Successfully loaded {len(loaded_posts)} posts")
        return loaded_posts

    except Exception as e:
        logger.error(f"Error in load_posts: {str(e)}")
        return []

if __name__ == '__main__':
    import sys
    app = create_app()
    with app.app_context():
        clear_existing = '--clear-tables' in sys.argv
        try:
            loaded_posts = load_posts(clear_existing)
            logger.info(f"Import completed. Loaded {len(loaded_posts)} posts.")
        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            sys.exit(1)