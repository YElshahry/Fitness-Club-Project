-- Health and Fitness Club Management System
-- DML (Data Manipulation Language)
-- Sample Data Insertion (at least 3-5 records per table)

-- Insert Members
INSERT INTO Member (first_name, last_name, email, phone, date_of_birth, gender, registration_date) VALUES
('John', 'Smith', 'john.smith@email.com', '555-0101', '1990-05-15', 'Male', '2024-01-10'),
('Emily', 'Johnson', 'emily.j@email.com', '555-0102', '1988-08-22', 'Female', '2024-01-15'),
('Michael', 'Brown', 'michael.b@email.com', '555-0103', '1995-03-10', 'Male', '2024-02-01'),
('Sarah', 'Davis', 'sarah.davis@email.com', '555-0104', '1992-11-30', 'Female', '2024-02-10'),
('David', 'Wilson', 'david.w@email.com', '555-0105', '1985-07-18', 'Male', '2024-03-01');

-- Insert Trainers
INSERT INTO Trainer (first_name, last_name, email, phone, specialization, hire_date) VALUES
('Alex', 'Martinez', 'alex.martinez@fitclub.com', '555-0201', 'Strength Training', '2023-06-01'),
('Jessica', 'Taylor', 'jessica.t@fitclub.com', '555-0202', 'Yoga & Flexibility', '2023-07-15'),
('Chris', 'Anderson', 'chris.a@fitclub.com', '555-0203', 'Cardio & HIIT', '2023-08-01'),
('Maria', 'Garcia', 'maria.g@fitclub.com', '555-0204', 'Nutrition & Weight Loss', '2023-09-01');

-- Insert Admins
INSERT INTO Admin (first_name, last_name, email, phone, role) VALUES
('Robert', 'Johnson', 'robert.j@fitclub.com', '555-0301', 'General Manager'),
('Linda', 'White', 'linda.w@fitclub.com', '555-0302', 'Operations Manager'),
('James', 'Miller', 'james.m@fitclub.com', '555-0303', 'Facility Coordinator');

-- Insert Rooms
INSERT INTO Room (room_name, room_type, capacity, status) VALUES
('Studio A', 'studio', 25, 'available'),
('Studio B', 'studio', 20, 'available'),
('Training Room 1', 'training_room', 1, 'available'),
('Training Room 2', 'training_room', 1, 'available'),
('Main Gym Floor', 'gym_floor', 50, 'available'),
('Cardio Zone', 'cardio_area', 30, 'available');

-- Insert Fitness Goals
INSERT INTO FitnessGoal (member_id, goal_type, target_value, current_value, target_date, status) VALUES
(1, 'weight_loss', 180.0, 200.0, '2025-06-01', 'active'),
(1, 'muscle_gain', 15.0, 12.0, '2025-08-01', 'active'),
(2, 'endurance', 5.0, 3.0, '2025-05-01', 'active'),
(3, 'weight_loss', 170.0, 185.0, '2025-07-01', 'active'),
(4, 'flexibility', 90.0, 60.0, '2025-04-01', 'active'),
(5, 'general_fitness', 100.0, 75.0, '2025-12-01', 'active');

-- Insert Health Metrics
INSERT INTO HealthMetric (member_id, recorded_date, weight, height, heart_rate, body_fat_percentage, notes) VALUES
(1, '2024-01-10 09:00:00', 200.0, 72.0, 75, 25.5, 'Initial assessment'),
(1, '2024-02-10 09:00:00', 195.0, 72.0, 72, 24.0, 'Good progress'),
(1, '2024-03-10 09:00:00', 192.0, 72.0, 70, 23.0, 'Continuing well'),
(2, '2024-01-15 10:00:00', 135.0, 65.0, 68, 22.0, 'Baseline metrics'),
(2, '2024-02-15 10:00:00', 133.0, 65.0, 65, 21.0, 'Improved cardio'),
(3, '2024-02-01 11:00:00', 185.0, 70.0, 80, 28.0, 'Starting point'),
(4, '2024-02-10 14:00:00', 128.0, 64.0, 70, 20.0, 'Good health'),
(5, '2024-03-01 08:00:00', 175.0, 69.0, 78, 26.0, 'Regular checkup');

-- Insert Personal Training Sessions
INSERT INTO PersonalTrainingSession (member_id, trainer_id, room_id, session_date, start_time, end_time, status) VALUES
(1, 1, 3, '2025-11-20', '09:00:00', '10:00:00', 'scheduled'),
(1, 1, 3, '2025-11-22', '09:00:00', '10:00:00', 'scheduled'),
(2, 2, 4, '2025-11-21', '14:00:00', '15:00:00', 'scheduled'),
(3, 1, 3, '2025-11-23', '10:00:00', '11:00:00', 'scheduled'),
(4, 3, 4, '2025-11-24', '16:00:00', '17:00:00', 'scheduled'),
(5, 4, 3, '2025-11-25', '11:00:00', '12:00:00', 'scheduled');

-- Insert Group Classes
INSERT INTO GroupClass (class_name, trainer_id, room_id, class_date, start_time, end_time, capacity, status) VALUES
('Morning Yoga', 2, 1, '2025-11-20', '07:00:00', '08:00:00', 20, 'scheduled'),
('HIIT Bootcamp', 3, 2, '2025-11-20', '18:00:00', '19:00:00', 15, 'scheduled'),
('Strength Training 101', 1, 1, '2025-11-21', '17:00:00', '18:00:00', 12, 'scheduled'),
('Evening Yoga', 2, 1, '2025-11-22', '19:00:00', '20:00:00', 20, 'scheduled'),
('Cardio Blast', 3, 2, '2025-11-23', '06:00:00', '07:00:00', 15, 'scheduled');

-- Insert Class Enrollments
INSERT INTO ClassEnrollment (member_id, class_id, status) VALUES
(1, 1, 'enrolled'),
(1, 2, 'enrolled'),
(2, 1, 'enrolled'),
(2, 4, 'enrolled'),
(3, 2, 'enrolled'),
(3, 3, 'enrolled'),
(4, 1, 'enrolled'),
(4, 4, 'enrolled'),
(5, 3, 'enrolled'),
(5, 5, 'enrolled');

-- Insert Trainer Availability
INSERT INTO TrainerAvailability (trainer_id, day_of_week, start_time, end_time, is_available) VALUES
-- Alex Martinez (Trainer 1) - Monday to Friday
(1, 1, '08:00:00', '17:00:00', TRUE), -- Monday
(1, 2, '08:00:00', '17:00:00', TRUE), -- Tuesday
(1, 3, '08:00:00', '17:00:00', TRUE), -- Wednesday
(1, 4, '08:00:00', '17:00:00', TRUE), -- Thursday
(1, 5, '08:00:00', '17:00:00', TRUE), -- Friday
-- Jessica Taylor (Trainer 2) - All week
(2, 1, '06:00:00', '20:00:00', TRUE),
(2, 2, '06:00:00', '20:00:00', TRUE),
(2, 3, '06:00:00', '20:00:00', TRUE),
(2, 4, '06:00:00', '20:00:00', TRUE),
(2, 5, '06:00:00', '20:00:00', TRUE),
(2, 6, '08:00:00', '16:00:00', TRUE), -- Saturday
-- Chris Anderson (Trainer 3) - Early mornings and evenings
(3, 1, '05:00:00', '10:00:00', TRUE),
(3, 1, '17:00:00', '21:00:00', TRUE),
(3, 3, '05:00:00', '10:00:00', TRUE),
(3, 3, '17:00:00', '21:00:00', TRUE),
(3, 5, '05:00:00', '10:00:00', TRUE);

-- Insert Equipment
INSERT INTO Equipment (equipment_name, room_id, purchase_date, status, last_maintenance_date) VALUES
('Treadmill #1', 6, '2023-01-15', 'operational', '2024-10-01'),
('Treadmill #2', 6, '2023-01-15', 'operational', '2024-10-01'),
('Elliptical #1', 6, '2023-02-20', 'operational', '2024-09-15'),
('Stationary Bike #1', 6, '2023-03-10', 'maintenance', '2024-11-01'),
('Yoga Mats (Set of 25)', 1, '2023-05-01', 'operational', '2024-08-01'),
('Weight Bench', 3, '2023-01-20', 'operational', '2024-10-15'),
('Dumbbells Set', 5, '2023-01-25', 'operational', '2024-09-20');

-- Insert Billing Records
INSERT INTO Billing (member_id, bill_date, amount, description, payment_status, payment_date, payment_method) VALUES
(1, '2024-01-10', 150.00, 'Monthly Membership - January 2024', 'paid', '2024-01-10', 'Credit Card'),
(1, '2024-02-10', 150.00, 'Monthly Membership - February 2024', 'paid', '2024-02-10', 'Credit Card'),
(1, '2024-03-10', 150.00, 'Monthly Membership - March 2024', 'paid', '2024-03-10', 'Credit Card'),
(2, '2024-01-15', 200.00, 'Monthly Membership + PT Package', 'paid', '2024-01-15', 'Debit Card'),
(2, '2024-02-15', 200.00, 'Monthly Membership + PT Package', 'paid', '2024-02-15', 'Debit Card'),
(3, '2024-02-01', 150.00, 'Monthly Membership - February 2024', 'paid', '2024-02-05', 'Cash'),
(3, '2024-03-01', 150.00, 'Monthly Membership - March 2024', 'pending', NULL, NULL),
(4, '2024-02-10', 180.00, 'Monthly Membership + Group Classes', 'paid', '2024-02-10', 'Credit Card'),
(5, '2024-03-01', 150.00, 'Monthly Membership - March 2024', 'paid', '2024-03-01', 'Bank Transfer');

-- Verify data insertion with counts
SELECT 'Members' AS table_name, COUNT(*) AS record_count FROM Member
UNION ALL
SELECT 'Trainers', COUNT(*) FROM Trainer
UNION ALL
SELECT 'Admins', COUNT(*) FROM Admin
UNION ALL
SELECT 'Rooms', COUNT(*) FROM Room
UNION ALL
SELECT 'FitnessGoals', COUNT(*) FROM FitnessGoal
UNION ALL
SELECT 'HealthMetrics', COUNT(*) FROM HealthMetric
UNION ALL
SELECT 'PersonalTrainingSessions', COUNT(*) FROM PersonalTrainingSession
UNION ALL
SELECT 'GroupClasses', COUNT(*) FROM GroupClass
UNION ALL
SELECT 'ClassEnrollments', COUNT(*) FROM ClassEnrollment
UNION ALL
SELECT 'TrainerAvailability', COUNT(*) FROM TrainerAvailability
UNION ALL
SELECT 'Equipment', COUNT(*) FROM Equipment
UNION ALL
SELECT 'Billing', COUNT(*) FROM Billing;
