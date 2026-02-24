-- EcoCleanUp Hub - Database Creation Script
-- COMP639 S1 2026
-- PostgreSQL

-- Drop tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS eventoutcomes CASCADE;
DROP TABLE IF EXISTS eventregistrations CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contact_number VARCHAR(20),
    home_address VARCHAR(255),
    profile_image VARCHAR(255),
    environmental_interests VARCHAR(255),
    role VARCHAR(20) NOT NULL DEFAULT 'volunteer' CHECK (role IN ('volunteer', 'event_leader', 'admin')),
    status VARCHAR(10) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    event_leader_id INTEGER NOT NULL REFERENCES users(user_id),
    location VARCHAR(255) NOT NULL,
    event_type VARCHAR(50),
    event_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    duration INTEGER,
    description TEXT,
    supplies TEXT,
    safety_instructions TEXT,
    status VARCHAR(20) DEFAULT 'upcoming' CHECK (status IN ('upcoming', 'ongoing', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event Registrations table
CREATE TABLE eventregistrations (
    registration_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    volunteer_id INTEGER NOT NULL REFERENCES users(user_id),
    attendance VARCHAR(20) DEFAULT 'registered' CHECK (attendance IN ('registered', 'attended', 'absent', 'cancelled')),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event Outcomes table
CREATE TABLE eventoutcomes (
    outcome_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    num_attendees INTEGER DEFAULT 0,
    bags_collected INTEGER DEFAULT 0,
    recyclables_sorted INTEGER DEFAULT 0,
    other_achievements TEXT,
    recorded_by INTEGER NOT NULL REFERENCES users(user_id),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Feedback table
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(event_id) ON DELETE CASCADE,
    volunteer_id INTEGER NOT NULL REFERENCES users(user_id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications table (for event reminders)
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    event_id INTEGER REFERENCES events(event_id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_leader ON events(event_leader_id);
CREATE INDEX idx_eventregistrations_event ON eventregistrations(event_id);
CREATE INDEX idx_eventregistrations_volunteer ON eventregistrations(volunteer_id);
CREATE INDEX idx_feedback_event ON feedback(event_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
