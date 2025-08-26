# app.py

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

from config import Config
from models import db, User, UserRole  # Import UserRole
from forms import LoginForm, RegisterForm

# --- App Initialization ---
app = Flask(__name__)
app.config.from_object(Config)

# --- Extensions Initialization ---
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- Helper Functions ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# This makes 'UserRole' available in all templates
@app.context_processor
def inject_user_role():
    return dict(UserRole=UserRole)

# Custom decorator to check for roles
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirect to the correct dashboard based on role
        if current_user.role == UserRole.CLIENT:
            return redirect(url_for('client_dashboard'))
        elif current_user.role == UserRole.CREATOR:
            return redirect(url_for('creator_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            # Redirect to the correct dashboard after login
            if user.role == UserRole.CLIENT:
                return redirect(url_for('client_dashboard'))
            elif user.role == UserRole.CREATOR:
                return redirect(url_for('creator_dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
            
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the role from the form and convert it to an Enum
        user_role = UserRole[form.role.data]

        new_user = User(
            username=form.username.data,
            role=user_role  # Set the role here
        )
        new_user.set_password(form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)

# --- NEW DASHBOARD ROUTES ---
@app.route('/client/dashboard')
@login_required
@role_required(UserRole.CLIENT) # Protects this route for clients only
def client_dashboard():
    return render_template('client_dashboard.html', name=current_user.username)

@app.route('/creator/dashboard')
@login_required
@role_required(UserRole.CREATOR) # Protects this route for creators only
def creator_dashboard():
    return render_template('creator_dashboard.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- Main Execution Block ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
