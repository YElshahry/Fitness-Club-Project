# Fitness Club Management System

This project is a command-line application that manages core operations for a fitness club, including members, trainers, classes, personal training sessions, and basic billing.

The system uses Python for the interface and PostgreSQL as the database.

The goal was to design a clean database structure and connect it to a working CLI, and support the main features required in a real fitness club setting.

# Main Features

## Member Features
    - Register as a new member
    - Track fitness goals
    - Log health metrics
    - Enroll in group classes
    - Book personal training sessions

## Trainer Features
    - View assigned classes
    - Managed personal training sessions
    - See availablity schedule

## Admin Features
    - Manage rooms and equipment
    - Add trainers
    - View member and trainer data
    - Oversee class scheduling and billing

### All actions run through the CLI menus in main.py

# How to Run the Project
    - Install PostgreSQL and create a database (name it anything such as: fitness_club)
    - Update your database settings in db_connection.py
    - Run both SQL scripts; DDl.sql and DML.sql
    - Install Python dependencies:
        pip install psycopg2
    - Start the program:
        python main.py
    