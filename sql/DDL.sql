-- Health and Fitness Club Management System
-- DDL (Data Definition Language)
-- Database Schema Creation

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS Billing CASCADE;
DROP TABLE IF EXISTS Equipment CASCADE;
DROP TABLE IF EXISTS TrainerAvailability CASCADE;
DROP TABLE IF EXISTS ClassEnrollment CASCADE;
DROP TABLE IF EXISTS GroupClass CASCADE;
DROP TABLE IF EXISTS PersonalTrainingSession CASCADE;
DROP TABLE IF EXISTS HealthMetric CASCADE;
DROP TABLE IF EXISTS FitnessGoal CASCADE;
DROP TABLE IF EXISTS Room CASCADE;
DROP TABLE IF EXISTS Trainer CASCADE;
DROP TABLE IF EXISTS Member CASCADE;
DROP TABLE IF EXISTS Admin CASCADE;

-- Create Member table
CREATE TABLE Member (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other', 'Prefer not to say')),
    registration_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT member_email_format CHECK (email LIKE '%@%')
);

-- Create Trainer table
CREATE TABLE Trainer (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    specialization VARCHAR(100),
    hire_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT trainer_email_format CHECK (email LIKE '%@%')
);

-- Create Admin table
CREATE TABLE Admin (
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'Administrator',
    CONSTRAINT admin_email_format CHECK (email LIKE '%@%')
);

-- Create Room table
CREATE TABLE Room (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50) NOT NULL UNIQUE,
    room_type VARCHAR(50) CHECK (room_type IN ('studio', 'training_room', 'gym_floor', 'cardio_area')),
    capacity INTEGER CHECK (capacity > 0),
    status VARCHAR(20) DEFAULT 'available' CHECK (status IN ('available', 'maintenance', 'reserved'))
);

-- Create FitnessGoal table
CREATE TABLE FitnessGoal (
    goal_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    goal_type VARCHAR(50) CHECK (goal_type IN ('weight_loss', 'muscle_gain', 'endurance', 'flexibility', 'general_fitness')),
    target_value DECIMAL(10, 2),
    current_value DECIMAL(10, 2),
    target_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    created_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE CASCADE
);

-- Create HealthMetric table
CREATE TABLE HealthMetric (
    metric_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    weight DECIMAL(5, 2) CHECK (weight > 0),
    height DECIMAL(5, 2) CHECK (height > 0),
    heart_rate INTEGER CHECK (heart_rate > 0 AND heart_rate < 300),
    body_fat_percentage DECIMAL(5, 2) CHECK (body_fat_percentage >= 0 AND body_fat_percentage <= 100),
    notes TEXT,
    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE CASCADE
);

-- Create PersonalTrainingSession table
CREATE TABLE PersonalTrainingSession (
    session_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    trainer_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no_show')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE CASCADE,
    CONSTRAINT valid_session_time CHECK (end_time > start_time)
);

-- Create GroupClass table
CREATE TABLE GroupClass (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    trainer_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    class_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    capacity INTEGER CHECK (capacity > 0),
    status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE CASCADE,
    CONSTRAINT valid_class_time CHECK (end_time > start_time)
);

-- Create ClassEnrollment table (Junction table for Member-GroupClass M:N relationship)
CREATE TABLE ClassEnrollment (
    enrollment_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'enrolled' CHECK (status IN ('enrolled', 'attended', 'cancelled', 'no_show')),
    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES GroupClass(class_id) ON DELETE CASCADE,
    CONSTRAINT unique_enrollment UNIQUE (member_id, class_id)
);

-- Create TrainerAvailability table
CREATE TABLE TrainerAvailability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INTEGER NOT NULL,
    day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sunday, 6=Saturday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id) ON DELETE CASCADE,
    CONSTRAINT valid_availability_time CHECK (end_time > start_time)
);

-- Create Equipment table
CREATE TABLE Equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    room_id INTEGER NOT NULL,
    purchase_date DATE,
    status VARCHAR(20) DEFAULT 'operational' CHECK (status IN ('operational', 'maintenance', 'broken', 'retired')),
    last_maintenance_date DATE,
    FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE CASCADE
);

-- Create Billing table
CREATE TABLE Billing (
    bill_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    bill_date DATE DEFAULT CURRENT_DATE,
    amount DECIMAL(10, 2) CHECK (amount >= 0),
    description TEXT,
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'overdue', 'cancelled')),
    payment_date DATE,
    payment_method VARCHAR(50),
    FOREIGN KEY (member_id) REFERENCES Member(member_id) ON DELETE CASCADE
);

-- Create VIEW: Member Dashboard Summary
CREATE OR REPLACE VIEW MemberDashboard AS
SELECT 
    m.member_id,
    m.first_name,
    m.last_name,
    m.email,
    COUNT(DISTINCT fg.goal_id) AS active_goals,
    COUNT(DISTINCT pts.session_id) AS upcoming_pt_sessions,
    COUNT(DISTINCT ce.enrollment_id) AS enrolled_classes,
    MAX(hm.recorded_date) AS last_metric_date,
    MAX(hm.weight) AS latest_weight,
    MAX(hm.heart_rate) AS latest_heart_rate
FROM Member m
LEFT JOIN FitnessGoal fg ON m.member_id = fg.member_id AND fg.status = 'active'
LEFT JOIN PersonalTrainingSession pts ON m.member_id = pts.member_id 
    AND pts.session_date >= CURRENT_DATE AND pts.status = 'scheduled'
LEFT JOIN ClassEnrollment ce ON m.member_id = ce.member_id AND ce.status = 'enrolled'
LEFT JOIN HealthMetric hm ON m.member_id = hm.member_id 
    AND hm.recorded_date = (SELECT MAX(recorded_date) FROM HealthMetric WHERE member_id = m.member_id)
GROUP BY m.member_id, m.first_name, m.last_name, m.email;

-- Create INDEX: Improve query performance on frequently searched columns
CREATE INDEX idx_member_email ON Member(email);
CREATE INDEX idx_trainer_email ON Trainer(email);
CREATE INDEX idx_pt_session_date ON PersonalTrainingSession(session_date, trainer_id);
CREATE INDEX idx_class_date ON GroupClass(class_date);
CREATE INDEX idx_health_metric_date ON HealthMetric(member_id, recorded_date DESC);

-- Create TRIGGER: Prevent double-booking of rooms for Personal Training Sessions
CREATE OR REPLACE FUNCTION check_room_availability_pt()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if room is already booked for a PT session at the same time
    IF EXISTS (
        SELECT 1 FROM PersonalTrainingSession
        WHERE room_id = NEW.room_id
        AND session_date = NEW.session_date
        AND status != 'cancelled'
        AND session_id != COALESCE(NEW.session_id, -1)
        AND (
            (NEW.start_time >= start_time AND NEW.start_time < end_time)
            OR (NEW.end_time > start_time AND NEW.end_time <= end_time)
            OR (NEW.start_time <= start_time AND NEW.end_time >= end_time)
        )
    ) THEN
        RAISE EXCEPTION 'Room % is already booked for a personal training session at this time', NEW.room_id;
    END IF;
    
    -- Check if room is already booked for a group class at the same time
    IF EXISTS (
        SELECT 1 FROM GroupClass
        WHERE room_id = NEW.room_id
        AND class_date = NEW.session_date
        AND status != 'cancelled'
        AND (
            (NEW.start_time >= start_time AND NEW.start_time < end_time)
            OR (NEW.end_time > start_time AND NEW.end_time <= end_time)
            OR (NEW.start_time <= start_time AND NEW.end_time >= end_time)
        )
    ) THEN
        RAISE EXCEPTION 'Room % is already booked for a group class at this time', NEW.room_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_room_availability_pt
BEFORE INSERT OR UPDATE ON PersonalTrainingSession
FOR EACH ROW
EXECUTE FUNCTION check_room_availability_pt();

-- Create TRIGGER: Prevent overbooking of group classes
CREATE OR REPLACE FUNCTION check_class_capacity()
RETURNS TRIGGER AS $$
DECLARE
    current_enrollment INTEGER;
    class_capacity INTEGER;
BEGIN
    -- Get current enrollment count and class capacity
    SELECT COUNT(*), gc.capacity
    INTO current_enrollment, class_capacity
    FROM ClassEnrollment ce
    JOIN GroupClass gc ON ce.class_id = gc.class_id
    WHERE ce.class_id = NEW.class_id
    AND ce.status = 'enrolled'
    GROUP BY gc.capacity;
    
    -- If no enrollment yet, get just the capacity
    IF current_enrollment IS NULL THEN
        SELECT capacity INTO class_capacity
        FROM GroupClass
        WHERE class_id = NEW.class_id;
        current_enrollment := 0;
    END IF;
    
    -- Check if adding this enrollment would exceed capacity
    IF current_enrollment >= class_capacity THEN
        RAISE EXCEPTION 'Class is full. Current enrollment: %, Capacity: %', current_enrollment, class_capacity;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_class_capacity
BEFORE INSERT ON ClassEnrollment
FOR EACH ROW
EXECUTE FUNCTION check_class_capacity();

-- Comments for documentation
COMMENT ON TABLE Member IS 'Stores member information and profile data';
COMMENT ON TABLE Trainer IS 'Stores trainer information and specializations';
COMMENT ON TABLE Admin IS 'Stores administrative staff information';
COMMENT ON TABLE Room IS 'Stores facility room information';
COMMENT ON TABLE FitnessGoal IS 'Tracks member fitness goals and progress';
COMMENT ON TABLE HealthMetric IS 'Records member health metrics over time';
COMMENT ON TABLE PersonalTrainingSession IS 'Manages one-on-one training sessions';
COMMENT ON TABLE GroupClass IS 'Manages group fitness classes';
COMMENT ON TABLE ClassEnrollment IS 'Tracks member enrollment in group classes';
COMMENT ON TABLE TrainerAvailability IS 'Defines trainer working hours and availability';
COMMENT ON TABLE Equipment IS 'Tracks gym equipment and maintenance';
COMMENT ON TABLE Billing IS 'Manages member billing and payments';
