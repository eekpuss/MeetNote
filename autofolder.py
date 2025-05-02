import os

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def create_file(path):
    """Create empty file if it doesn't exist"""
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass  # Create empty file
        print(f"Created file: {path}")

def create_project_structure():
    """Create the entire project structure for MeetNote"""
    # Root directory
    root_dir = "meetnote"
    create_directory(root_dir)
    
    # Backend directories
    backend_dirs = [
        "backend",
        "backend/models",
        "backend/controllers",
        "backend/utils",
        "backend/database"
    ]
    
    for dir_path in backend_dirs:
        create_directory(os.path.join(root_dir, dir_path))
    
    # Backend files
    backend_files = [
        "backend/app.py",
        "backend/config.py",
        "backend/requirements.txt",
        "backend/models/__init__.py",
        "backend/models/user.py",
        "backend/models/meeting.py",
        "backend/models/todo.py",
        "backend/controllers/__init__.py",
        "backend/controllers/auth.py",
        "backend/controllers/meeting.py",
        "backend/controllers/todo.py",
        "backend/utils/__init__.py",
        "backend/utils/pdf.py",
        "backend/utils/email.py",
        "backend/utils/integrations.py",
        "backend/database/meetnote.db"
    ]
    
    for file_path in backend_files:
        create_file(os.path.join(root_dir, file_path))
    
    # Frontend directories
    frontend_dirs = [
        "frontend",
        "frontend/assets",
        "frontend/assets/css",
        "frontend/assets/js",
        "frontend/assets/img",
        "frontend/assets/fonts",
        "frontend/components",
        "frontend/pages",
        "frontend/pages/meetings",
        "frontend/pages/todos"
    ]
    
    for dir_path in frontend_dirs:
        create_directory(os.path.join(root_dir, dir_path))
    
    # Frontend files
    frontend_files = [
        "frontend/index.html",
        "frontend/login.html",
        "frontend/assets/css/main.css",
        "frontend/assets/css/responsive.css",
        "frontend/assets/js/main.js",
        "frontend/assets/js/meeting.js",
        "frontend/assets/js/todo.js",
        "frontend/components/sidebar.html",
        "frontend/components/header.html",
        "frontend/components/footer.html",
        "frontend/pages/dashboard.html",
        "frontend/pages/meetings/list.html",
        "frontend/pages/meetings/create.html",
        "frontend/pages/meetings/view.html",
        "frontend/pages/todos/list.html",
        "frontend/pages/todos/create.html",
        "frontend/pages/todos/view.html"
    ]
    
    for file_path in frontend_files:
        create_file(os.path.join(root_dir, file_path))
    
    # Documentation directory and files
    docs_dir = os.path.join(root_dir, "docs")
    create_directory(docs_dir)
    
    docs_files = [
        "docs/setup.md",
        "docs/api.md"
    ]
    
    for file_path in docs_files:
        create_file(os.path.join(root_dir, file_path))
    
    print("\nProject structure for MeetNote has been successfully created!")

if __name__ == "__main__":
    create_project_structure()