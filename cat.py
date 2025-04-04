import os
from gitignore_parser import parse_gitignore

# Define the files to be concatenated
files_to_concatenate = [
    'run.py',
    'config.py',
    
    'app/__init__.py',
#    'app/models.py',
    'app/routes.py',

#    'app/static/js/main.js',
#    'app/static/css/main.css',

#    'app/templates/index.html',
    'app/templates/base.html',
    'app/templates/stash_it.html',
    'app/templates/stash_it_privacy_policy.html',

#    'app/templates/partials/service_details.html',
    
#    'app/email/email_service.py',
    
#    'app/blog/__init__.py',
#    'app/blog/templates/blog_index.html',
#    'app/blog/templates/post.html',
#    'app/blog/templates/new_post.html',
#    'app/blog/templates/category.html',
#    'app/blog/forms.py',
#    'app/blog/routes.py',
#    'app/blog/posts/post1_content.md',
#    'app/blog/posts/post1.json5',
#    'app/blog/posts/footer.md',
    
#    'package.json',
#    'import_posts.py',
    'zzz_nginx.md',
    'zzz_systemd.md'
]

# Define the output file
output_file = 'combined.txt'

def create_directory_tree(startpath):
    """Generate a string representation of the directory tree, excluding .gitignore files, migrations/, and .git/."""
    tree = []
    
    # Parse .gitignore file
    gitignore_file = os.path.join(startpath, '.gitignore')
    if os.path.exists(gitignore_file):
        ignorer = parse_gitignore(gitignore_file)
    else:
        ignorer = lambda f: False  # If no .gitignore, don't ignore anything
    
    # Additional directories to exclude
    exclude_dirs = {'migrations', '.git'}
    
    for root, dirs, files in os.walk(startpath, topdown=True):
        # Remove ignored and explicitly excluded directories
        dirs[:] = [d for d in dirs if not ignorer(os.path.join(root, d)) and d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if not ignorer(os.path.join(root, f)):
                tree.append(f"{subindent}{f}")
    return '\n'.join(tree)

def concatenate_files(file_list, output_file):
    tree = create_directory_tree('.')  # Adjust '.' to the root of your project if necessary
    with open(output_file, 'w') as outfile:
        outfile.write("# Project Directory Structure\n")
        outfile.write(tree + "\n\n# End of Directory Structure\n\n")
        for file_name in file_list:
            if os.path.exists(file_name):
                with open(file_name, 'r') as infile:
                    outfile.write(f'# Start of {file_name}\n')
                    outfile.write(infile.read())
                    outfile.write(f'\n# End of {file_name}\n\n')
            else:
                print(f"File {file_name} does not exist.")

if __name__ == '__main__':
    concatenate_files(files_to_concatenate, output_file)
    print(f"Files concatenated into {output_file}")
