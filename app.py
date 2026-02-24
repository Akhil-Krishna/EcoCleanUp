"""
EcoCleanUp Hub - Main Application
COMP639 S1 2026 - Individual Assignment
A web-based community cleanup management system for GreenSteps Initiative.

Name : Sneha Kuriakose
Student ID: 

GenAI Acknowledgement: Gemini and Claude were used to assist in generating 
realistic test data for populate_database.sql and to help structure some 
template layouts. Prompts included: "Generate 20 realistic NZ volunteer 
profiles for a community cleanup web app database" and "Help structure 
Bootstrap navbar with role-based links".
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import re
from datetime import datetime, date
from connect import get_connection

app = Flask(__name__)
app.secret_key = 'ecocleanup_secret_key_2026_greensteps'
app.jinja_env.globals['enumerate'] = enumerate

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ─── Helper Functions ────────────────────────────────────────────────────────

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_password(password):
    """
    Validate password meets requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains a digit
    - Contains a special character
    Returns (bool, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]]', password):
        return False, "Password must contain at least one special character."
    return True, "Password is valid."


def get_db_connection():
    """Get a database connection."""
    return get_connection()


# ─── Access Control Decorators ───────────────────────────────────────────────

def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific roles for a route."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_unread_notifications():
    """Get unread notifications for the current user."""
    if 'user_id' not in session:
        return []
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT n.notification_id, n.message, n.created_at, e.event_name, e.event_date
        FROM notifications n
        LEFT JOIN events e ON n.event_id = e.event_id
        WHERE n.user_id = %s AND n.is_read = FALSE
        ORDER BY n.created_at DESC
    """, (session['user_id'],))
    notifications = cur.fetchall()
    cur.close()
    conn.close()
    return notifications


# ─── Home & Auth Routes ──────────────────────────────────────────────────────

@app.route('/')
def home():
    """Home page with login and registration links."""
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for all users (volunteers, event leaders, admins)."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('auth/login.html')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username, password_hash, full_name, role, status FROM users WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[2], password):
            if user[5] == 'inactive':
                flash('Your account has been deactivated. Please contact an administrator.', 'danger')
                return render_template('auth/login.html')

            session['user_id'] = user[0]
            session['username'] = user[1]
            session['full_name'] = user[3]
            session['role'] = user[4]

            # Check for unread notifications
            notifications = get_unread_notifications()
            if notifications:
                session['has_notifications'] = True

            flash(f'Welcome back, {user[3]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page for new volunteers only."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        home_address = request.form.get('home_address', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        environmental_interests = request.form.get('environmental_interests', '').strip()

        # Validation
        errors = []
        if not all([username, email, password, confirm_password, full_name]):
            errors.append('Please fill in all required fields.')
        if password != confirm_password:
            errors.append('Passwords do not match.')

        valid_pw, pw_msg = validate_password(password)
        if not valid_pw:
            errors.append(pw_msg)

        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append('Please enter a valid email address.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('auth/register.html', form_data=request.form)

        # Check username uniqueness
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            flash('Username already taken. Please choose a different username.', 'danger')
            cur.close()
            conn.close()
            return render_template('auth/register.html', form_data=request.form)

        # Handle profile image upload
        profile_image = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{username}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_image = filename

        # Hash password and insert user
        hashed_password = generate_password_hash(password)
        cur.execute("""
            INSERT INTO users (username, password_hash, full_name, email, contact_number, 
                               home_address, profile_image, environmental_interests, role, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'volunteer', 'active')
            RETURNING user_id
        """, (username, hashed_password, full_name, email, contact_number,
              home_address, profile_image, environmental_interests))
        conn.commit()
        cur.close()
        conn.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', form_data={})


@app.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))


# ─── Dashboard ───────────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    """Role-based dashboard redirect."""
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'event_leader':
        return redirect(url_for('leader_dashboard'))
    else:
        return redirect(url_for('volunteer_dashboard'))


# ─── Profile Routes ──────────────────────────────────────────────────────────

@app.route('/profile')
@login_required
def profile():
    """View current user profile."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, username, full_name, email, contact_number, 
               home_address, profile_image, environmental_interests, role, status, created_at
        FROM users WHERE user_id = %s
    """, (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('shared/profile.html', user=user, notifications=notifications)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit current user profile."""
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        home_address = request.form.get('home_address', '').strip()
        environmental_interests = request.form.get('environmental_interests', '').strip()
        remove_image = request.form.get('remove_image') == '1'

        if not full_name or not email:
            flash('Full name and email are required.', 'danger')
            return redirect(url_for('edit_profile'))

        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('edit_profile'))

        # Get current profile image
        cur.execute("SELECT profile_image FROM users WHERE user_id = %s", (session['user_id'],))
        current_image = cur.fetchone()[0]
        profile_image = current_image

        if remove_image:
            profile_image = None
        elif 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{session['username']}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_image = filename

        cur.execute("""
            UPDATE users SET full_name=%s, email=%s, contact_number=%s, 
                             home_address=%s, profile_image=%s, environmental_interests=%s
            WHERE user_id=%s
        """, (full_name, email, contact_number, home_address, profile_image,
              environmental_interests, session['user_id']))
        conn.commit()
        session['full_name'] = full_name
        flash('Profile updated successfully.', 'success')
        cur.close()
        conn.close()
        return redirect(url_for('profile'))

    cur.execute("""
        SELECT user_id, username, full_name, email, contact_number, 
               home_address, profile_image, environmental_interests, role
        FROM users WHERE user_id = %s
    """, (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('shared/edit_profile.html', user=user, notifications=notifications)


@app.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE user_id = %s", (session['user_id'],))
        user = cur.fetchone()

        if not check_password_hash(user[0], current_password):
            flash('Current password is incorrect.', 'danger')
            cur.close()
            conn.close()
            return redirect(url_for('change_password'))

        if check_password_hash(user[0], new_password):
            flash('New password cannot be the same as the current password.', 'danger')
            cur.close()
            conn.close()
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            cur.close()
            conn.close()
            return redirect(url_for('change_password'))

        valid_pw, pw_msg = validate_password(new_password)
        if not valid_pw:
            flash(pw_msg, 'danger')
            cur.close()
            conn.close()
            return redirect(url_for('change_password'))

        hashed = generate_password_hash(new_password)
        cur.execute("UPDATE users SET password_hash=%s WHERE user_id=%s",
                    (hashed, session['user_id']))
        conn.commit()
        cur.close()
        conn.close()
        flash('Password changed successfully.', 'success')
        return redirect(url_for('profile'))

    notifications = get_unread_notifications()
    return render_template('shared/change_password.html', notifications=notifications)


# ─── Notifications ────────────────────────────────────────────────────────────

@app.route('/notifications/mark-read', methods=['POST'])
@login_required
def mark_notifications_read():
    """Mark all notifications as read for the current user."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE notifications SET is_read=TRUE WHERE user_id=%s", (session['user_id'],))
    conn.commit()
    cur.close()
    conn.close()
    session['has_notifications'] = False
    return redirect(request.referrer or url_for('dashboard'))


# ─── Event Browsing (All Roles) ──────────────────────────────────────────────

@app.route('/events')
@login_required
def browse_events():
    """Browse all upcoming cleanup events with filtering."""
    filter_date = request.args.get('date', '')
    filter_location = request.args.get('location', '').strip()
    filter_type = request.args.get('type', '').strip()

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT e.event_id, e.event_name, e.location, e.event_type, e.event_date, 
               e.start_time, e.end_time, e.duration, e.description, e.status,
               u.full_name as leader_name,
               (SELECT COUNT(*) FROM eventregistrations er WHERE er.event_id = e.event_id) as registered_count
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        WHERE e.status != 'cancelled'
    """
    params = []

    if filter_date:
        query += " AND e.event_date = %s"
        params.append(filter_date)
    if filter_location:
        query += " AND LOWER(e.location) LIKE %s"
        params.append(f'%{filter_location.lower()}%')
    if filter_type:
        query += " AND e.event_type = %s"
        params.append(filter_type)

    query += " ORDER BY e.event_date ASC, e.start_time ASC"
    cur.execute(query, params)
    events = cur.fetchall()

    # Get event types for filter dropdown
    cur.execute("SELECT DISTINCT event_type FROM events WHERE event_type IS NOT NULL ORDER BY event_type")
    event_types = [row[0] for row in cur.fetchall()]

    # Get user's registrations if volunteer
    user_registrations = []
    if session.get('role') == 'volunteer':
        cur.execute("SELECT event_id FROM eventregistrations WHERE volunteer_id=%s", (session['user_id'],))
        user_registrations = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('shared/browse_events.html', events=events, event_types=event_types,
                           user_registrations=user_registrations, notifications=notifications,
                           filter_date=filter_date, filter_location=filter_location, filter_type=filter_type)


@app.route('/events/<int:event_id>')
@login_required
def event_detail(event_id):
    """View detailed information about a specific event."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.event_id, e.event_name, e.location, e.event_type, e.event_date, 
               e.start_time, e.end_time, e.duration, e.description, e.supplies, 
               e.safety_instructions, e.status, u.full_name as leader_name, e.event_leader_id
        FROM events e
        JOIN users u ON e.event_leader_id = u.user_id
        WHERE e.event_id = %s
    """, (event_id,))
    event = cur.fetchone()

    if not event:
        flash('Event not found.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('browse_events'))

    is_registered = False
    if session.get('role') == 'volunteer':
        cur.execute("SELECT registration_id FROM eventregistrations WHERE event_id=%s AND volunteer_id=%s",
                    (event_id, session['user_id']))
        is_registered = cur.fetchone() is not None

    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('shared/event_detail.html', event=event, is_registered=is_registered,
                           notifications=notifications)


# ─── Volunteer Routes ─────────────────────────────────────────────────────────

@app.route('/volunteer/dashboard')
@role_required('volunteer')
def volunteer_dashboard():
    """Volunteer dashboard with overview."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Upcoming registered events
    cur.execute("""
        SELECT e.event_id, e.event_name, e.event_date, e.start_time, e.location, er.attendance
        FROM eventregistrations er
        JOIN events e ON er.event_id = e.event_id
        WHERE er.volunteer_id = %s AND e.event_date >= CURRENT_DATE AND e.status != 'cancelled'
        ORDER BY e.event_date ASC
        LIMIT 5
    """, (session['user_id'],))
    upcoming = cur.fetchall()

    # Total events participated
    cur.execute("""
        SELECT COUNT(*) FROM eventregistrations er
        JOIN events e ON er.event_id = e.event_id
        WHERE er.volunteer_id = %s AND er.attendance = 'attended'
    """, (session['user_id'],))
    total_attended = cur.fetchone()[0]

    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('volunteer/dashboard.html', upcoming=upcoming,
                           total_attended=total_attended, notifications=notifications)


@app.route('/volunteer/register-event/<int:event_id>', methods=['POST'])
@role_required('volunteer')
def register_for_event(event_id):
    """Register a volunteer for a cleanup event."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Check event exists and is upcoming
    cur.execute("SELECT event_id, event_date, start_time, end_time, event_name FROM events WHERE event_id=%s AND status='upcoming'",
                (event_id,))
    event = cur.fetchone()
    if not event:
        flash('Event not available for registration.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('browse_events'))

    # Check if already registered
    cur.execute("SELECT registration_id FROM eventregistrations WHERE event_id=%s AND volunteer_id=%s",
                (event_id, session['user_id']))
    if cur.fetchone():
        flash('You are already registered for this event.', 'warning')
        cur.close()
        conn.close()
        return redirect(url_for('event_detail', event_id=event_id))

    # Check for scheduling conflicts
    cur.execute("""
        SELECT e.event_name, e.event_date, e.start_time, e.end_time
        FROM eventregistrations er
        JOIN events e ON er.event_id = e.event_id
        WHERE er.volunteer_id = %s 
          AND e.event_date = %s 
          AND e.status != 'cancelled'
          AND er.attendance != 'cancelled'
          AND (
              (e.start_time <= %s AND e.end_time > %s) OR
              (e.start_time < %s AND e.end_time >= %s) OR
              (e.start_time >= %s AND e.end_time <= %s)
          )
    """, (session['user_id'], event[1], event[3], event[2], event[3], event[2], event[2], event[3]))
    conflict = cur.fetchone()

    if conflict:
        flash(f'Registration declined: You are already registered for "{conflict[0]}" on {conflict[1]} '
              f'from {conflict[2]} to {conflict[3]}, which conflicts with this event.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('event_detail', event_id=event_id))

    # Register volunteer
    cur.execute("""
        INSERT INTO eventregistrations (event_id, volunteer_id, attendance, registered_at)
        VALUES (%s, %s, 'registered', CURRENT_TIMESTAMP)
    """, (event_id, session['user_id']))
    conn.commit()

    flash(f'Successfully registered for "{event[4]}"!', 'success')
    cur.close()
    conn.close()
    return redirect(url_for('event_detail', event_id=event_id))


@app.route('/volunteer/participation-history')
@login_required
def participation_history():
    """View volunteer participation history."""
    user_id = request.args.get('user_id', session['user_id'])
    # Only admins and event leaders can view other users' history
    if int(user_id) != session['user_id'] and session.get('role') not in ('admin', 'event_leader'):
        user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.event_id, e.event_name, e.event_date, e.location, e.event_type,
               er.attendance, er.registered_at,
               (SELECT f.rating FROM feedback f WHERE f.event_id=e.event_id AND f.volunteer_id=er.volunteer_id LIMIT 1) as rating
        FROM eventregistrations er
        JOIN events e ON er.event_id = e.event_id
        WHERE er.volunteer_id = %s
        ORDER BY e.event_date DESC
    """, (user_id,))
    history = cur.fetchall()

    cur.execute("SELECT full_name FROM users WHERE user_id=%s", (user_id,))
    user_name = cur.fetchone()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('volunteer/participation_history.html', history=history,
                           user_name=user_name[0] if user_name else 'Unknown',
                           viewing_self=(int(user_id) == session['user_id']),
                           notifications=notifications)


@app.route('/volunteer/submit-feedback/<int:event_id>', methods=['GET', 'POST'])
@role_required('volunteer')
def submit_feedback(event_id):
    """Submit feedback for a completed event."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Verify volunteer attended this event
    cur.execute("""
        SELECT er.registration_id FROM eventregistrations er
        JOIN events e ON er.event_id = e.event_id
        WHERE er.event_id=%s AND er.volunteer_id=%s AND er.attendance='attended'
    """, (event_id, session['user_id']))
    registration = cur.fetchone()

    if not registration:
        flash('You can only submit feedback for events you have attended.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('participation_history'))

    # Check if already submitted feedback
    cur.execute("SELECT feedback_id FROM feedback WHERE event_id=%s AND volunteer_id=%s",
                (event_id, session['user_id']))
    if cur.fetchone():
        flash('You have already submitted feedback for this event.', 'warning')
        cur.close()
        conn.close()
        return redirect(url_for('participation_history'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        comments = request.form.get('comments', '').strip()

        if not rating:
            flash('Please provide a star rating.', 'danger')
        else:
            cur.execute("""
                INSERT INTO feedback (event_id, volunteer_id, rating, comments, submitted_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (event_id, session['user_id'], int(rating), comments))
            conn.commit()
            flash('Thank you for your feedback!', 'success')
            cur.close()
            conn.close()
            return redirect(url_for('participation_history'))

    cur.execute("SELECT event_name, event_date FROM events WHERE event_id=%s", (event_id,))
    event = cur.fetchone()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('volunteer/submit_feedback.html', event=event, event_id=event_id,
                           notifications=notifications)


# ─── Event Leader Routes ──────────────────────────────────────────────────────

@app.route('/leader/dashboard')
@role_required('event_leader')
def leader_dashboard():
    """Event leader dashboard."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT event_id, event_name, event_date, location, status,
               (SELECT COUNT(*) FROM eventregistrations er WHERE er.event_id=e.event_id) as reg_count
        FROM events e
        WHERE event_leader_id = %s
        ORDER BY event_date DESC LIMIT 5
    """, (session['user_id'],))
    recent_events = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM events WHERE event_leader_id=%s", (session['user_id'],))
    total_events = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM eventregistrations er
        JOIN events e ON er.event_id=e.event_id
        WHERE e.event_leader_id=%s
    """, (session['user_id'],))
    total_registrations = cur.fetchone()[0]

    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/dashboard.html', recent_events=recent_events,
                           total_events=total_events, total_registrations=total_registrations,
                           notifications=notifications)


@app.route('/leader/events')
@role_required('event_leader')
def leader_events():
    """List all events created by this leader."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.event_id, e.event_name, e.event_date, e.location, e.event_type, e.status,
               (SELECT COUNT(*) FROM eventregistrations er WHERE er.event_id=e.event_id) as reg_count
        FROM events e
        WHERE e.event_leader_id = %s
        ORDER BY e.event_date DESC
    """, (session['user_id'],))
    events = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/events.html', events=events, notifications=notifications)


@app.route('/leader/events/create', methods=['GET', 'POST'])
@role_required('event_leader')
def create_event():
    """Create a new cleanup event."""
    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        location = request.form.get('location', '').strip()
        event_type = request.form.get('event_type', '').strip()
        event_date = request.form.get('event_date', '')
        start_time = request.form.get('start_time', '')
        end_time = request.form.get('end_time', '')
        duration = request.form.get('duration', '')
        description = request.form.get('description', '').strip()
        supplies = request.form.get('supplies', '').strip()
        safety_instructions = request.form.get('safety_instructions', '').strip()

        if not all([event_name, location, event_date, start_time]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('event_leader/create_event.html',
                                   notifications=get_unread_notifications(), form_data=request.form)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO events (event_name, event_leader_id, location, event_type, event_date,
                                start_time, end_time, duration, description, supplies, safety_instructions, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'upcoming')
            RETURNING event_id
        """, (event_name, session['user_id'], location, event_type, event_date,
              start_time, end_time or None, duration or None, description, supplies, safety_instructions))
        conn.commit()
        cur.close()
        conn.close()
        flash(f'Event "{event_name}" created successfully!', 'success')
        return redirect(url_for('leader_events'))

    notifications = get_unread_notifications()
    return render_template('event_leader/create_event.html', notifications=notifications, form_data={})


@app.route('/leader/events/<int:event_id>/edit', methods=['GET', 'POST'])
@role_required('event_leader', 'admin')
def edit_event(event_id):
    """Edit an existing event."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Admin can edit any event; leader can only edit their own
    if session['role'] == 'event_leader':
        cur.execute("SELECT * FROM events WHERE event_id=%s AND event_leader_id=%s",
                    (event_id, session['user_id']))
    else:
        cur.execute("SELECT * FROM events WHERE event_id=%s", (event_id,))
    event = cur.fetchone()

    if not event:
        flash('Event not found or you do not have permission to edit it.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        location = request.form.get('location', '').strip()
        event_type = request.form.get('event_type', '').strip()
        event_date = request.form.get('event_date', '')
        start_time = request.form.get('start_time', '')
        end_time = request.form.get('end_time', '')
        duration = request.form.get('duration', '')
        description = request.form.get('description', '').strip()
        supplies = request.form.get('supplies', '').strip()
        safety_instructions = request.form.get('safety_instructions', '').strip()
        status = request.form.get('status', 'upcoming')

        cur.execute("""
            UPDATE events SET event_name=%s, location=%s, event_type=%s, event_date=%s,
                              start_time=%s, end_time=%s, duration=%s, description=%s,
                              supplies=%s, safety_instructions=%s, status=%s
            WHERE event_id=%s
        """, (event_name, location, event_type, event_date, start_time, end_time or None,
              duration or None, description, supplies, safety_instructions, status, event_id))
        conn.commit()
        cur.close()
        conn.close()
        flash('Event updated successfully.', 'success')
        if session['role'] == 'admin':
            return redirect(url_for('admin_events'))
        return redirect(url_for('leader_events'))

    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/edit_event.html', event=event, notifications=notifications)


@app.route('/leader/events/<int:event_id>/cancel', methods=['POST'])
@role_required('event_leader', 'admin')
def cancel_event(event_id):
    """Cancel an event."""
    conn = get_db_connection()
    cur = conn.cursor()

    if session['role'] == 'event_leader':
        cur.execute("UPDATE events SET status='cancelled' WHERE event_id=%s AND event_leader_id=%s",
                    (event_id, session['user_id']))
    else:
        cur.execute("UPDATE events SET status='cancelled' WHERE event_id=%s", (event_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Event has been cancelled.', 'info')
    if session['role'] == 'admin':
        return redirect(url_for('admin_events'))
    return redirect(url_for('leader_events'))


@app.route('/leader/events/<int:event_id>/volunteers')
@role_required('event_leader', 'admin')
def event_volunteers(event_id):
    """View list of volunteers registered for an event."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT event_name, event_date, location, event_leader_id FROM events WHERE event_id=%s", (event_id,))
    event = cur.fetchone()

    if not event:
        flash('Event not found.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    # Leaders can only view their own events
    if session['role'] == 'event_leader' and event[3] != session['user_id']:
        flash('You do not have permission to view this event.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    cur.execute("""
        SELECT er.registration_id, u.user_id, u.full_name, u.email, u.contact_number,
               er.attendance, er.registered_at
        FROM eventregistrations er
        JOIN users u ON er.volunteer_id = u.user_id
        WHERE er.event_id = %s
        ORDER BY er.registered_at ASC
    """, (event_id,))
    volunteers = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/event_volunteers.html', event=event, event_id=event_id,
                           volunteers=volunteers, notifications=notifications)


@app.route('/leader/events/<int:event_id>/volunteers/<int:volunteer_id>/remove', methods=['POST'])
@role_required('event_leader', 'admin')
def remove_volunteer(event_id, volunteer_id):
    """Remove a volunteer from an event."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM eventregistrations WHERE event_id=%s AND volunteer_id=%s",
                (event_id, volunteer_id))
    conn.commit()
    cur.close()
    conn.close()
    flash('Volunteer removed from event.', 'info')
    return redirect(url_for('event_volunteers', event_id=event_id))


@app.route('/leader/events/<int:event_id>/attendance', methods=['GET', 'POST'])
@role_required('event_leader')
def track_attendance(event_id):
    """Track attendance for volunteers at an event."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT event_name, event_date, event_leader_id FROM events WHERE event_id=%s", (event_id,))
    event = cur.fetchone()

    if not event or event[2] != session['user_id']:
        flash('Event not found or permission denied.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('attendance_'):
                reg_id = key.split('_')[1]
                cur.execute("UPDATE eventregistrations SET attendance=%s WHERE registration_id=%s",
                            (value, reg_id))
        conn.commit()
        flash('Attendance updated successfully.', 'success')

    cur.execute("""
        SELECT er.registration_id, u.full_name, u.email, er.attendance
        FROM eventregistrations er
        JOIN users u ON er.volunteer_id = u.user_id
        WHERE er.event_id = %s
        ORDER BY u.full_name
    """, (event_id,))
    volunteers = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/track_attendance.html', event=event, event_id=event_id,
                           volunteers=volunteers, notifications=notifications)


@app.route('/leader/events/<int:event_id>/outcomes', methods=['GET', 'POST'])
@role_required('event_leader')
def record_outcomes(event_id):
    """Record event outcomes."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT event_name, event_date, event_leader_id FROM events WHERE event_id=%s", (event_id,))
    event = cur.fetchone()

    if not event or event[2] != session['user_id']:
        flash('Event not found or permission denied.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    if request.method == 'POST':
        num_attendees = request.form.get('num_attendees', 0)
        bags_collected = request.form.get('bags_collected', 0)
        recyclables_sorted = request.form.get('recyclables_sorted', 0)
        other_achievements = request.form.get('other_achievements', '').strip()

        # Check if outcome already exists
        cur.execute("SELECT outcome_id FROM eventoutcomes WHERE event_id=%s", (event_id,))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE eventoutcomes SET num_attendees=%s, bags_collected=%s, 
                                         recyclables_sorted=%s, other_achievements=%s, recorded_at=CURRENT_TIMESTAMP
                WHERE event_id=%s
            """, (num_attendees, bags_collected, recyclables_sorted, other_achievements, event_id))
        else:
            cur.execute("""
                INSERT INTO eventoutcomes (event_id, num_attendees, bags_collected, recyclables_sorted, 
                                           other_achievements, recorded_by, recorded_at)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (event_id, num_attendees, bags_collected, recyclables_sorted,
                  other_achievements, session['user_id']))

        # Update event status to completed
        cur.execute("UPDATE events SET status='completed' WHERE event_id=%s", (event_id,))
        conn.commit()
        flash('Event outcomes recorded successfully.', 'success')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    cur.execute("SELECT * FROM eventoutcomes WHERE event_id=%s", (event_id,))
    existing_outcome = cur.fetchone()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/record_outcomes.html', event=event, event_id=event_id,
                           existing_outcome=existing_outcome, notifications=notifications)


@app.route('/leader/events/<int:event_id>/send-reminder', methods=['POST'])
@role_required('event_leader')
def send_reminder(event_id):
    """Send reminder notification to all registered volunteers."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT event_name, event_date, start_time, location, event_leader_id FROM events WHERE event_id=%s",
                (event_id,))
    event = cur.fetchone()

    if not event or event[4] != session['user_id']:
        flash('Event not found or permission denied.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    cur.execute("""
        SELECT volunteer_id FROM eventregistrations 
        WHERE event_id=%s AND attendance NOT IN ('cancelled', 'absent')
    """, (event_id,))
    volunteers = cur.fetchall()

    message = (f'Reminder: You are registered for "{event[0]}" on {event[1]} '
               f'at {event[2]}. Location: {event[3]}. See you there!')

    for vol in volunteers:
        cur.execute("""
            INSERT INTO notifications (user_id, event_id, message, is_read, created_at)
            VALUES (%s, %s, %s, FALSE, CURRENT_TIMESTAMP)
        """, (vol[0], event_id, message))

    conn.commit()
    cur.close()
    conn.close()
    flash(f'Reminders sent to {len(volunteers)} volunteer(s).', 'success')
    return redirect(url_for('event_volunteers', event_id=event_id))


@app.route('/leader/events/<int:event_id>/feedback')
@role_required('event_leader', 'admin')
def review_feedback(event_id):
    """Review feedback for a specific event."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT event_name, event_date, event_leader_id FROM events WHERE event_id=%s", (event_id,))
    event = cur.fetchone()

    if not event:
        flash('Event not found.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    if session['role'] == 'event_leader' and event[2] != session['user_id']:
        flash('Permission denied.', 'danger')
        cur.close()
        conn.close()
        return redirect(url_for('leader_events'))

    cur.execute("""
        SELECT f.feedback_id, u.full_name, f.rating, f.comments, f.submitted_at
        FROM feedback f
        JOIN users u ON f.volunteer_id = u.user_id
        WHERE f.event_id = %s
        ORDER BY f.submitted_at DESC
    """, (event_id,))
    feedbacks = cur.fetchall()

    cur.execute("SELECT AVG(rating) FROM feedback WHERE event_id=%s", (event_id,))
    avg_rating = cur.fetchone()[0]
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/review_feedback.html', event=event, event_id=event_id,
                           feedbacks=feedbacks, avg_rating=avg_rating, notifications=notifications)


@app.route('/leader/participation-history')
@role_required('event_leader')
def leader_participation_history():
    """Event leader views participation history across all managed events."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.full_name, e.event_name, e.event_date, er.attendance, er.registered_at
        FROM eventregistrations er
        JOIN events e ON er.event_id = e.event_id
        JOIN users u ON er.volunteer_id = u.user_id
        WHERE e.event_leader_id = %s
        ORDER BY e.event_date DESC, u.full_name ASC
    """, (session['user_id'],))
    history = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('event_leader/participation_history.html', history=history,
                           notifications=notifications)


@app.route('/leader/reports')
@role_required('event_leader', 'admin')
def event_reports():
    """Event reports for leaders (their events) and admins (all events)."""
    conn = get_db_connection()
    cur = conn.cursor()

    if session['role'] == 'event_leader':
        cur.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.location, e.status,
                   COUNT(DISTINCT er.volunteer_id) as registered,
                   SUM(CASE WHEN er.attendance='attended' THEN 1 ELSE 0 END) as attended,
                   eo.bags_collected, eo.recyclables_sorted, eo.num_attendees,
                   AVG(f.rating) as avg_rating
            FROM events e
            LEFT JOIN eventregistrations er ON er.event_id=e.event_id
            LEFT JOIN eventoutcomes eo ON eo.event_id=e.event_id
            LEFT JOIN feedback f ON f.event_id=e.event_id
            WHERE e.event_leader_id = %s
            GROUP BY e.event_id, eo.bags_collected, eo.recyclables_sorted, eo.num_attendees
            ORDER BY e.event_date DESC
        """, (session['user_id'],))
    else:
        cur.execute("""
            SELECT e.event_id, e.event_name, e.event_date, e.location, e.status,
                   COUNT(DISTINCT er.volunteer_id) as registered,
                   SUM(CASE WHEN er.attendance='attended' THEN 1 ELSE 0 END) as attended,
                   eo.bags_collected, eo.recyclables_sorted, eo.num_attendees,
                   AVG(f.rating) as avg_rating
            FROM events e
            LEFT JOIN eventregistrations er ON er.event_id=e.event_id
            LEFT JOIN eventoutcomes eo ON eo.event_id=e.event_id
            LEFT JOIN feedback f ON f.event_id=e.event_id
            GROUP BY e.event_id, eo.bags_collected, eo.recyclables_sorted, eo.num_attendees
            ORDER BY e.event_date DESC
        """)
    reports = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('shared/event_reports.html', reports=reports, notifications=notifications)


# ─── Admin Routes ─────────────────────────────────────────────────────────────

@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    """Admin dashboard with platform-wide statistics."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users WHERE role='volunteer'")
    total_volunteers = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM users WHERE role='event_leader'")
    total_leaders = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM feedback")
    total_feedback = cur.fetchone()[0]
    cur.execute("SELECT AVG(rating) FROM feedback")
    avg_rating = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM eventregistrations")
    total_registrations = cur.fetchone()[0]

    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('admin/dashboard.html',
                           total_volunteers=total_volunteers,
                           total_leaders=total_leaders,
                           total_events=total_events,
                           total_feedback=total_feedback,
                           avg_rating=round(avg_rating, 2) if avg_rating else 0,
                           total_registrations=total_registrations,
                           notifications=notifications)


@app.route('/admin/users')
@role_required('admin')
def admin_users():
    """Admin view all users with search and filtering."""
    search = request.args.get('search', '').strip()
    filter_role = request.args.get('role', '')
    filter_status = request.args.get('status', '')

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT user_id, username, full_name, email, role, status, created_at
        FROM users WHERE 1=1
    """
    params = []

    if search:
        query += " AND (LOWER(full_name) LIKE %s OR LOWER(username) LIKE %s)"
        params.extend([f'%{search.lower()}%', f'%{search.lower()}%'])
    if filter_role:
        query += " AND role = %s"
        params.append(filter_role)
    if filter_status:
        query += " AND status = %s"
        params.append(filter_status)

    query += " ORDER BY created_at DESC"
    cur.execute(query, params)
    users = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('admin/users.html', users=users, notifications=notifications,
                           search=search, filter_role=filter_role, filter_status=filter_status)


@app.route('/admin/users/<int:user_id>')
@role_required('admin')
def admin_view_user(user_id):
    """Admin view a specific user's profile."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, username, full_name, email, contact_number, 
               home_address, profile_image, environmental_interests, role, status, created_at
        FROM users WHERE user_id = %s
    """, (user_id,))
    user = cur.fetchone()

    # Get participation history
    cur.execute("""
        SELECT e.event_name, e.event_date, er.attendance
        FROM eventregistrations er
        JOIN events e ON er.event_id=e.event_id
        WHERE er.volunteer_id=%s
        ORDER BY e.event_date DESC
    """, (user_id,))
    history = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('admin/view_user.html', user=user, history=history, notifications=notifications)


@app.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@role_required('admin')
def toggle_user_status(user_id):
    """Toggle a user's active/inactive status."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT status FROM users WHERE user_id=%s", (user_id,))
    user = cur.fetchone()
    if user:
        new_status = 'inactive' if user[0] == 'active' else 'active'
        cur.execute("UPDATE users SET status=%s WHERE user_id=%s", (new_status, user_id))
        conn.commit()
        flash(f'User status updated to {new_status}.', 'success')
    cur.close()
    conn.close()
    return redirect(url_for('admin_users'))


@app.route('/admin/events')
@role_required('admin')
def admin_events():
    """Admin view all events."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.event_id, e.event_name, e.event_date, e.location, e.status,
               u.full_name as leader,
               COUNT(er.registration_id) as reg_count
        FROM events e
        JOIN users u ON e.event_leader_id=u.user_id
        LEFT JOIN eventregistrations er ON er.event_id=e.event_id
        GROUP BY e.event_id, u.full_name
        ORDER BY e.event_date DESC
    """)
    events = cur.fetchall()
    cur.close()
    conn.close()
    notifications = get_unread_notifications()
    return render_template('admin/events.html', events=events, notifications=notifications)


@app.route('/admin/reports')
@role_required('admin')
def admin_reports():
    """Admin platform-wide reports."""
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
