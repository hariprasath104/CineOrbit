# app.py

# --- Step 1: Thevaiyana Libraries ah import panradhu ---
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

# Nammodaya project files la irundhu config, models, forms ah import panradhu
from config import Config
from models import db, User, UserRole
from forms import LoginForm, RegisterForm

# --- Step 2: Flask App ah Create Panradhu ---
app = Flask(__name__)
# config.py la irukura settings ah load panradhu (SECRET_KEY, DATABASE_URL)
app.config.from_object(Config)

# --- Step 3: Extensions ah App kooda Inaikuradhu ---
# Database (SQLAlchemy) ah nammodaya app kooda inaikuradhu
db.init_app(app)
# User login/logout ah manage panra LoginManager ah create panradhu
login_manager = LoginManager()
login_manager.init_app(app)
# Login pannama oru page ku pona, 'login' page ku anupuradhu
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- Step 4: Helper Functions (Uthavi Seiyum Functions) ---

# LoginManager ku user ah eppadi kandupudikanum nu solradhu
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# HTML templates la 'UserRole.CLIENT' nu use panradhukaga idha add panrom
@app.context_processor
def inject_user_role():
    return dict(UserRole=UserRole)

# Oru user correct ana role la thaan irukangala nu check panra function
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # User login pannirukanuma and avanga role correct ah nu check panrom
            if not current_user.is_authenticated or current_user.role != role:
                flash('Indha page ah paaka ungaluku anumathi illai.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- Step 5: Routes (Website oda Pages) ---

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # User munnadiye login pannirundha, avanga dashboard ku anupidradhu
    if current_user.is_authenticated:
        if current_user.role == UserRole.CLIENT:
            return redirect(url_for('client_dashboard'))
        elif current_user.role == UserRole.CREATOR:
            return redirect(url_for('creator_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login vetrikaramaga nadandhadhu!', 'success')
            # Login pannadhuku apram correct ana dashboard ku anupidradhu
            if user.role == UserRole.CLIENT:
                return redirect(url_for('client_dashboard'))
            elif user.role == UserRole.CREATOR:
                return redirect(url_for('creator_dashboard'))
        else:
            flash('Login tholviyadaindhadhu. Unga username and password ah sari paarunga.', 'danger')
            
    return render_template('login.html', form=form)

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        # Form la irundhu user enna role select pannanga nu edukuradhu
        user_role = UserRole[form.role.data]

        # Pudhu user ah avanga role oda create panradhu
        new_user = User(
            username=form.username.data,
            role=user_role
        )
        new_user.set_password(form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Unga account vetrikaramaga uruvaakapattadhu! Ipo neenga login seiyalam.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)

# Client Dashboard Page
@app.route('/client/dashboard')
@login_required
@role_required(UserRole.CLIENT) # Client mattum thaan indha page ah paaka mudiyum
def client_dashboard():
    return render_template('client_dashboard.html', name=current_user.username)

# Creator (Employee) Dashboard Page
@app.route('/creator/dashboard')
@login_required
@role_required(UserRole.CREATOR) # Creator mattum thaan indha page ah paaka mudiyum
def creator_dashboard():
    return render_template('creator_dashboard.html', name=current_user.username)

# Logout Function
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Neenga veliyerivittirgal.', 'info')
    return redirect(url_for('login'))

# --- Step 6: Main Execution Block (Unga Laptop la Run Panna Mattum) ---
# Indha block, neenga 'python app.py' nu run pannum pothu mattum thaan work agum.
# Render la idhu work agadhu.
if __name__ == '__main__':
    # Unga local database (database.db) ah create panradhuku
    with app.app_context():
        db.create_all()
    # Unga local server ah start panradhuku
    app.run(debug=True)
