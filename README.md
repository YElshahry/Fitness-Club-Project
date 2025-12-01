# Fitness Club Management System

Project made by: Soliman Elkhouli, and Yousuf Elshahry

This project is a command-line application that manages core operations for a fitness club, including members, trainers, classes, personal training sessions, and basic billing.

The system uses Python for the interface and PostgreSQL as the database.

The goal was to design a clean database structure and connect it to a working CLI, and support the main features required in a real fitness club setting.

## Video Demonstration
https://youtu.be/lyJYgCf9qsc

# Main Features

## Member Features
- Register as a new member
- Track fitness goals
- Log health metrics
- Enroll in group classes
- Book personal training sessions


## Trainer Features
- View assigned classes
- Manage personal training sessions
- See availability schedule

## Admin Features
- Manage rooms and equipment
- Add trainers
- View member and trainer data
- Oversee class scheduling and billing

### All actions run through the CLI menus in main.py

# How to Run the Project
1. Install PostgreSQL and create a database (any name, ex: `fitness_club`).
2. Update your database settings in `db_connection.py`.
3. Run both SQL scripts (`DDL.sql` and `DML.sql`) to create tables and insert sample data.
4. Install Python dependencies:
```pip install psycopg2```
5. Start the program:
```python main.py```
    
# Database Design

### The database is fully normalized and includes:
- Clear entity relationships
- Many-to-many handling through `ClassEnrollment`
- Triggers for preventing overlapping sessions
- A view for simple dashboard output
- Indexes to improve query performance


# Folder Structure

```
- app/
    main.py
    admin_operations.py
    trainer_operations.py
    member_operations.py
    db_connection.py
    
- sql/
    DDL.sql
    DML.sql
    
- docs/
    ERD.pdf
    ERD_Design.pdf
    Project_Report.pdf
    
README.md
```