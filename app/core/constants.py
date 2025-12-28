# File and directory names to be hidden and blocked
FORBIDDEN_NAMES = {'.git', '.idea', 'venv', '__pycache__', 'node_modules'}
FORBIDDEN_EXTENSIONS = {'.pyc', '.gitignore', '.env', '.iml'}

# Extensions that we want to show in the gallery preview
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico', '.bmp'}
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.webm', '.avi', '.mov', '.3gp', '.3g2'}
TEXT_EXTENSIONS = {
    '.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yml', '.yaml', 
    '.xml', '.sh', '.sql', '.log', '.ini', '.conf', '.bat', '.bash'
}

PREVIEWABLE_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | TEXT_EXTENSIONS
