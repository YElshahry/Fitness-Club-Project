# Demo Video Script
## Health and Fitness Club Management System

**Total Duration**: ~12-15 minutes  
**Team Members**: [Your names here]

---

## Introduction (1 minute)

**[Show title slide]**

"Hello! Today we're presenting our Health and Fitness Club Management System, a comprehensive database application designed for COMP 3005. This project demonstrates a complete solution for managing the daily operations of a modern fitness center, supporting members, trainers, and administrative staff."

---

## Section 1: ER Model (2-3 minutes)

**[Show ER Diagram - ERD.png]**

"Let's start with our Entity-Relationship model. Our system includes 12 entities, which exceeds the requirement of 8 for a team of 2."

### Key Entities to Highlight:

1. **Member, Trainer, Admin** - "These represent our three user roles with distinct privileges."

2. **FitnessGoal and HealthMetric** - "These entities enable members to track their fitness journey over time with time-stamped records."

3. **PersonalTrainingSession and GroupClass** - "These manage the core services offered by the fitness club."

4. **Room and Equipment** - "These support facility management and resource allocation."

5. **ClassEnrollment** - "This junction table implements the many-to-many relationship between members and group classes."

### Relationships to Highlight:

"We have 11 relationships in our model, including:
- One-to-many relationships like Member HAS FitnessGoal
- A many-to-many relationship between Member and GroupClass, implemented through ClassEnrollment
- Room HOSTS both PersonalTrainingSession and GroupClass, enabling proper resource allocation"

### Design Assumptions:

"Key assumptions we made:
- Each personal training session involves exactly one member and one trainer
- Group classes can have multiple members but only one trainer
- Rooms can be used for multiple purposes but cannot be double-booked
- Health metrics are never overwritten - they're stored historically for trend analysis"

---

## Section 2: ER to Relational Mapping (2 minutes)

**[Show DDL.sql file or schema diagram]**

"Now let's see how we translated our ER model into relational tables."

### Show Key Tables:

**[Scroll through DDL.sql, highlighting:]**

1. **Member table**: "Notice how we use SERIAL for auto-incrementing IDs, UNIQUE constraint on email, and CHECK constraint for email format validation."

2. **PersonalTrainingSession table**: "This table has three foreign keys - member_id, trainer_id, and room_id - representing the relationships in our ER model. We also have a CHECK constraint ensuring end_time is after start_time."

3. **ClassEnrollment table**: "This junction table implements our many-to-many relationship with a UNIQUE constraint on (member_id, class_id) to prevent duplicate enrollments."

---

## Section 3: Database Definition (2-3 minutes)

**[Show DDL.sql file]**

### Part A: If NOT using ORM

"Let's look at our DDL.sql file, which contains all CREATE TABLE statements."

**[Scroll through and highlight:]**

1. **Tables**: "We have 12 tables with proper constraints - primary keys, foreign keys, check constraints, and unique constraints."

2. **Sample Data**: "Our DML.sql file includes 3-5 sample records per table to demonstrate the system."

**[Show DML.sql briefly]**

"Here you can see sample members, trainers, rooms, and scheduled sessions."

---

## Section 4: Functionality Demonstration (6-8 minutes)

**[Run the application: python3 main.py]**

"Now let's demonstrate the 10 operations we've implemented across all three user roles."

### Member Operations (Show 4 operations):

**Operation 1: User Registration**
```
[Select Member Operations → Register New Member]
First Name: Alice
Last Name: Cooper
Email: alice.cooper@email.com
Phone: 555-9999
Date of Birth: 1993-04-12
Gender: Female
```
"✓ Registration successful! Member ID assigned automatically."

**Operation 2: Profile Management & Fitness Goal**
```
[Select Update Profile]
Member ID: [use the new member ID]
Add fitness goal: y
Goal Type: weight_loss
Target Value: 140.0
Current Value: 160.0
Target Date: 2025-08-01
```
"✓ Profile updated and fitness goal added."

**Operation 3: Health History**
```
[Select Record Health Metrics]
Member ID: [same member ID]
Weight: 160.0
Height: 66.0
Heart Rate: 72
Body Fat %: 28.5
Notes: Initial baseline measurement
```
"✓ Health metric recorded with timestamp."

**Operation 4: Dashboard**
```
[Select View Dashboard]
Member ID: [same member ID]
```
"✓ Dashboard shows active goals, upcoming sessions, enrolled classes, and latest health metrics using our MemberDashboard VIEW."

**[Optional: Show Operation 5 or 6 if time permits]**

### Trainer Operations (Show 2 operations):

**Operation 1: Set Availability**
```
[Select Trainer Operations → Set Availability]
Trainer ID: 1
Day of Week: 6 (Saturday)
Start Time: 09:00:00
End Time: 13:00:00
```
"✓ Availability set. The system prevents overlapping time slots for the same trainer."

**Operation 2: Schedule View**
```
[Select View Schedule]
Trainer ID: 1
Start Date: 2025-11-20
End Date: 2025-11-30
```
"✓ Shows all PT sessions and group classes assigned to this trainer."

**[Optional: Show Member Lookup]**

### Admin Operations (Show 2 operations):

**Operation 1: Room Booking**
```
[Select Admin Operations → Manage Room Booking]
Booking Type: pt_session
Room ID: 4
Date: 2025-11-27
Start Time: 15:00:00
End Time: 16:00:00
Trainer ID: 2
Member ID: 1
```
"✓ Room booked successfully. Our TRIGGER prevents double-booking."

**[Demonstrate failure case:]**
"Now let's try to book the same room at an overlapping time..."
```
[Try to book Room 4 at 15:30-16:30 on same date]
```
"✗ Error! The trigger detected the conflict and prevented the double-booking."

**Operation 2: Equipment Maintenance**
```
[Select Manage Equipment → view]
```
"✓ Shows all equipment with status. We can update status and log maintenance."

**[Optional: Show Class Management or Billing if time permits]**

---

## Section 5: Code Structure (1 minute)

**[Show project folder structure]**

"Our code is organized as follows:
- `/sql` folder contains DDL.sql and DML.sql
- `/app` folder contains Python application code
  - `db_connection.py` - Database connection pooling
  - `member_operations.py` - All member functions
  - `trainer_operations.py` - All trainer functions
  - `admin_operations.py` - All admin functions
  - `main.py` - CLI interface
- `/docs` folder contains ER diagram and documentation"

---

## Section 6: Interface & User Flow (1 minute)

**[Show main menu and navigation]**

"The application uses a simple CLI interface with role-based menus. Users select their role (Member, Trainer, or Admin) and then access operations specific to their role. Each operation includes:
- Input validation
- Success/failure feedback
- Clear error messages
- Proper transaction handling"

---

## Conclusion (30 seconds)

"To summarize, our Health and Fitness Club Management System includes:
- 12 entities and 11 relationships (exceeding requirements)
- 10+ operations across all user roles
- 1 VIEW (MemberDashboard), 1 TRIGGER (room conflict prevention), and multiple INDEXES
- Fully normalized schema in 3NF
- Complete SQL implementation with constraints and sample data
- Working Python application with role-based access

Thank you for watching! We're happy to answer any questions."

---

## Tips for Recording:

1. **Test everything before recording** - Make sure all operations work correctly
2. **Speak clearly and at a moderate pace** - Don't rush through the demo
3. **Show both success and failure cases** - Especially for the trigger demonstration
4. **Keep it under 15 minutes** - Practice timing beforehand
5. **Both team members should participate** - Split the presentation sections
6. **Use screen recording software** - OBS Studio, Zoom, or similar
7. **Ensure text is readable** - Use appropriate font sizes and contrast
8. **Upload as unlisted** - YouTube or Vimeo, accessible without sign-in

---

## Checklist Before Recording:

- [ ] Database is set up with sample data
- [ ] Application runs without errors
- [ ] All 10 operations are functional
- [ ] ER diagram is clear and visible
- [ ] SQL files are properly formatted
- [ ] Screen resolution is set appropriately
- [ ] Audio is clear and without background noise
- [ ] Both team members know their sections
- [ ] Timing has been practiced (12-15 minutes total)
