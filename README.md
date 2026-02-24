# EcoCleanUp Hub
### Community Cleanup Management System — GreenSteps Initiative
**COMP639 S1 2026 | Individual Assignment**
**Author:** Sneha Kuriakose | **Student ID:** [Your Student ID]

---

## About EcoCleanUp Hub

EcoCleanUp Hub is a web-based community cleanup management platform built for the fictional environmental organisation **GreenSteps Initiative**. It allows volunteers to discover and register for local EcoCleanUp events, event leaders to coordinate and manage events, and administrators to oversee the entire platform.

---

## Technology Stack

- **Backend:** Python 3, Flask
- **Frontend:** Bootstrap 5, Jinja2 Templates, JavaScript
- **Database:** PostgreSQL (hosted on PythonAnywhere)
- **Password Hashing:** Werkzeug (scrypt)
- **Deployment:** PythonAnywhere

---

## Project Structure

```
EcoCleanUp/
├── app.py                      # Main Flask application
├── connect.py                  # Database connection (excluded from Git)
├── requirements.txt            # Python dependencies
├── create_database.sql         # Database schema creation script
├── populate_database.sql       # Database population script (test data)
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles (sustainability theme)
│   ├── js/
│   │   └── main.js             # JavaScript utilities
│   └── uploads/                # User profile images
└── templates/
    ├── base.html               # Base layout with navbar and footer
    ├── home.html               # Public home page
    ├── auth/
    │   ├── login.html
    │   └── register.html
    ├── shared/
    │   ├── profile.html
    │   ├── edit_profile.html
    │   ├── change_password.html
    │   ├── browse_events.html
    │   ├── event_detail.html
    │   └── event_reports.html
    ├── volunteer/
    │   ├── dashboard.html
    │   ├── participation_history.html
    │   └── submit_feedback.html
    ├── event_leader/
    │   ├── dashboard.html
    │   ├── events.html
    │   ├── create_event.html
    │   ├── edit_event.html
    │   ├── event_volunteers.html
    │   ├── track_attendance.html
    │   ├── record_outcomes.html
    │   ├── review_feedback.html
    │   └── participation_history.html
    └── admin/
        ├── dashboard.html
        ├── users.html
        ├── view_user.html
        └── events.html
```

---

## Local Development Setup

### Prerequisites
- Python 3.10+
- PostgreSQL (local instance for development)
- pip

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/[your-username]/EcoCleanUp.git
   cd EcoCleanUp
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `connect.py`** (NOT committed to Git):
   ```python
   def get_connection():
       import psycopg2
       conn = psycopg2.connect(
           host='localhost',
           port=5432,
           database='ecocleanup_db',
           user='your_db_user',
           password='your_db_password'
       )
       return conn
   ```

5. **Create the database and tables:**
   ```bash
   psql -U your_db_user -d ecocleanup_db -f create_database.sql
   ```

6. **Populate with test data:**
   ```bash
   psql -U your_db_user -d ecocleanup_db -f populate_database.sql
   ```

7. **Run the application:**
   ```bash
   python app.py
   ```
   Visit: `http://127.0.0.1:5000`

---

## PythonAnywhere Deployment

1. **Upload files** via PythonAnywhere Files tab or Git clone into your home directory.

2. **Create `connect.py`** in your app folder with PythonAnywhere credentials (see email from course admin):
   ```python
   def get_connection():
       import psycopg2
       conn = psycopg2.connect(
           host='lincolnmac-5080.postgres.pythonanywhere-services.com',
           port=15080,
           database='sneha_kuriakose_ecu',
           user='sneha_kuriakose',
           password='your_password'
       )
       return conn
   ```

3. **Set up the database** via PythonAnywhere Bash console:
   ```bash
   export PGPASSWORD='your_password'
   psql -h lincolnmac-5080.postgres.pythonanywhere-services.com -p 15080 -U sneha_kuriakose -d sneha_kuriakose_ecu -f /home/sneha_kuriakose/EcoCleanUp/create_database.sql
   psql -h lincolnmac-5080.postgres.pythonanywhere-services.com -p 15080 -U sneha_kuriakose -d sneha_kuriakose_ecu -f /home/sneha_kuriakose/EcoCleanUp/populate_database.sql
   ```

4. **Install requirements** in Bash console:
   ```bash
   pip install --user -r requirements.txt
   ```

5. **Configure Web App** in PythonAnywhere:
   - Source code: `/home/sneha_kuriakose/EcoCleanUp`
   - Working directory: `/home/sneha_kuriakose/EcoCleanUp`
   - WSGI file: point to `app.py`, set `application = app`

6. **Set teacher:** Go to Account → Education → enter `lincolnmac`.

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin_sarah` | `Admin1Pass!` |
| Admin | `admin_james` | `Admin2Pass!` |
| Event Leader | `leader_emma` | `Leader1Pass!` |
| Event Leader | `leader_david` | `Leader2Pass!` |
| Event Leader | `leader_nadia` | `Leader3Pass!` |
| Event Leader | `leader_tom` | `Leader4Pass!` |
| Event Leader | `leader_priya` | `Leader5Pass!` |
| Volunteer | `v_liam` | `EcoPass1!` |
| Volunteer | `v_chloe` | `EcoPass2!` |
| Volunteer | `v_noah` | `EcoPass3!` |
| Volunteer | `v_ava` | `EcoPass4!` |
| Volunteer | `v_ethan` | `EcoPass5!` |
| Volunteer | `v_zoe` | `EcoPass20!` |

*(20 volunteers total — v_liam through v_zoe with passwords EcoPass1! to EcoPass20!)*

---

## User Roles & Features

### Volunteer
- Register for an account (auto-assigned volunteer role)
- Login/logout
- Browse and filter cleanup events by date, location, type
- Register for events (with conflict detection)
- View participation history and attendance
- Submit star rating and comments feedback for attended events
- Receive login popup notifications for upcoming registered events
- View and edit profile including profile image
- Change password

### Event Leader
- All volunteer browsing features
- Create new cleanup events with all required details
- Manage (edit/cancel) own events
- View registered volunteers per event
- Remove volunteers from events
- Track volunteer attendance
- Record event outcomes (attendees, bags collected, recyclables sorted)
- Send reminder notifications to registered volunteers
- Review volunteer feedback
- View participation history across managed events
- Generate event reports

### Admin
- All event browsing features
- View, search, and filter all users
- View individual user profiles and participation history
- Activate/deactivate any user account
- View and manage all events (edit/cancel)
- Access platform-wide statistics dashboard
- Generate event reports for all events

---

## Password Policy
- Minimum 8 characters
- Must contain: uppercase letter, lowercase letter, digit, special character
- Passwords are hashed using Werkzeug (scrypt) — never stored in plain text
- Current password cannot be reused when changing password

---

## GenAI Acknowledgement

The following GenAI tools were used in this assessment:

| Tool | Usage | Prompts Used |
|------|-------|--------------|
| **Claude (Anthropic) & Gemini** | Generating realistic test data for `populate_database.sql`; structuring Bootstrap navbar with role-based links; reviewing SQL schema compatibility with PostgreSQL | "Generate 20 realistic NZ volunteer profiles for a community cleanup web app database including name, address, email, contact number, and environmental interests"; "Help structure a Bootstrap 5 navbar with role-based dropdown menus using Flask session" |


All GenAI-generated content was reviewed, tested, and adapted to fit the specific requirements of this project. The logical structure, database design, Flask route architecture, and overall code organisation were developed independently.

This acknowledgement complies with Lincoln University's GenAI usage policy as outlined on Te Kete Wānaka's Referencing page.

---

## Notes

- Profile images are stored as static files; filenames are saved in the database
- The `connect.py` file is excluded from version control (see `.gitignore`)
- Do NOT commit database credentials to GitHub
- The ERD from the assignment brief is implemented in `create_database.sql`, with an additional `notifications` table for event reminders
