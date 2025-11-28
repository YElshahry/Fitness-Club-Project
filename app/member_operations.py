"""
Member Operations Module
Implements all member-related functionality for the Health and Fitness Club Management System

Required Operations (4 minimum for team of 2):
1. User Registration
2. Profile Management
3. Health History
4. Dashboard
5. PT Session Scheduling
6. Group Class Registration
"""

from db_connection import DatabaseConnection
from datetime import datetime, date


class MemberOperations:
    """Handles all member-related database operations"""
    
    @staticmethod
    def register_member(first_name, last_name, email, phone, date_of_birth, gender):
        """
        Operation 1: User Registration
        Creates a new member account with unique email and basic profile info
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO Member (first_name, last_name, email, phone, date_of_birth, gender)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING member_id, registration_date;
                """
                cursor.execute(query, (first_name, last_name, email, phone, date_of_birth, gender))
                result = cursor.fetchone()
                
                print(f"✓ Member registered successfully!")
                print(f"  Member ID: {result[0]}")
                print(f"  Registration Date: {result[1]}")
                return result[0]
                
        except Exception as e:
            print(f"✗ Error registering member: {e}")
            return None
    
    @staticmethod
    def update_profile(member_id, **kwargs):
        """
        Operation 2: Profile Management
        Updates member personal details and fitness goals
        Supports updating: phone, email, fitness goal
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                # Update basic profile info
                update_fields = []
                values = []
                
                if 'phone' in kwargs:
                    update_fields.append("phone = %s")
                    values.append(kwargs['phone'])
                
                if 'email' in kwargs:
                    update_fields.append("email = %s")
                    values.append(kwargs['email'])
                
                if update_fields:
                    values.append(member_id)
                    query = f"UPDATE Member SET {', '.join(update_fields)} WHERE member_id = %s"
                    cursor.execute(query, values)
                    print(f"✓ Profile updated successfully for Member ID: {member_id}")
                
                # Add or update fitness goal if provided
                if 'goal_type' in kwargs and 'target_value' in kwargs:
                    goal_query = """
                        INSERT INTO FitnessGoal (member_id, goal_type, target_value, current_value, target_date, status)
                        VALUES (%s, %s, %s, %s, %s, 'active')
                    """
                    cursor.execute(goal_query, (
                        member_id,
                        kwargs['goal_type'],
                        kwargs['target_value'],
                        kwargs.get('current_value', 0),
                        kwargs.get('target_date', None)
                    ))
                    print(f"✓ Fitness goal added: {kwargs['goal_type']}")
                
                return True
                
        except Exception as e:
            print(f"✗ Error updating profile: {e}")
            return False
    
    @staticmethod
    def add_health_metric(member_id, weight=None, height=None, heart_rate=None, 
                         body_fat_percentage=None, notes=None):
        """
        Operation 3: Health History
        Logs multiple metric entries with timestamps (does not overwrite previous entries)
        Supports time-stamped health tracking
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO HealthMetric 
                    (member_id, weight, height, heart_rate, body_fat_percentage, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING metric_id, recorded_date;
                """
                cursor.execute(query, (member_id, weight, height, heart_rate, 
                                     body_fat_percentage, notes))
                result = cursor.fetchone()
                
                print(f"✓ Health metric recorded!")
                print(f"  Metric ID: {result[0]}")
                print(f"  Recorded: {result[1]}")
                return result[0]
                
        except Exception as e:
            print(f"✗ Error recording health metric: {e}")
            return None
    
    @staticmethod
    def view_dashboard(member_id):
        """
        Operation 4: Dashboard
        Shows latest health stats, active goals, past class count, upcoming sessions
        Uses the MemberDashboard VIEW created in DDL
        """
        try:
            with DatabaseConnection.get_cursor() as cursor:
                # Use the VIEW for dashboard summary
                query = """
                    SELECT * FROM MemberDashboard
                    WHERE member_id = %s;
                """
                cursor.execute(query, (member_id,))
                dashboard = cursor.fetchone()
                
                if not dashboard:
                    print(f"✗ No data found for Member ID: {member_id}")
                    return None
                
                print("\n" + "="*60)
                print(f"MEMBER DASHBOARD - {dashboard[1]} {dashboard[2]}")
                print("="*60)
                print(f"Email: {dashboard[3]}")
                print(f"Active Goals: {dashboard[4]}")
                print(f"Upcoming PT Sessions: {dashboard[5]}")
                print(f"Enrolled Classes: {dashboard[6]}")
                print(f"Last Metric Date: {dashboard[7]}")
                print(f"Latest Weight: {dashboard[8]} lbs" if dashboard[8] else "Latest Weight: N/A")
                print(f"Latest Heart Rate: {dashboard[9]} bpm" if dashboard[9] else "Latest Heart Rate: N/A")
                print("="*60 + "\n")
                
                return dashboard
                
        except Exception as e:
            print(f"✗ Error viewing dashboard: {e}")
            return None
    
    @staticmethod
    def schedule_pt_session(member_id, trainer_id, room_id, session_date, start_time, end_time):
        """
        Operation 5: PT Session Scheduling
        Books or reschedules training with a trainer
        Validates availability and room conflicts using TRIGGER
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                # First check trainer availability
                day_of_week = datetime.strptime(session_date, '%Y-%m-%d').weekday()
                # Convert Python weekday (0=Monday) to our format (0=Sunday)
                day_of_week = (day_of_week + 1) % 7
                
                avail_query = """
                    SELECT availability_id FROM TrainerAvailability
                    WHERE trainer_id = %s 
                    AND day_of_week = %s
                    AND %s >= start_time 
                    AND %s <= end_time
                    AND is_available = TRUE;
                """
                cursor.execute(avail_query, (trainer_id, day_of_week, start_time, end_time))
                
                if not cursor.fetchone():
                    print(f"✗ Trainer is not available at the requested time")
                    return None
                
                # Insert session (trigger will check room conflicts)
                query = """
                    INSERT INTO PersonalTrainingSession 
                    (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'scheduled')
                    RETURNING session_id;
                """
                cursor.execute(query, (member_id, trainer_id, room_id, session_date, 
                                     start_time, end_time))
                session_id = cursor.fetchone()[0]
                
                print(f"✓ PT Session scheduled successfully!")
                print(f"  Session ID: {session_id}")
                print(f"  Date: {session_date} from {start_time} to {end_time}")
                return session_id
                
        except Exception as e:
            print(f"✗ Error scheduling PT session: {e}")
            return None
    
    @staticmethod
    def register_for_class(member_id, class_id):
        """
        Operation 6: Group Class Registration
        Registers for scheduled classes if capacity permits
        Uses TRIGGER to prevent overbooking
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                # Check if class exists and get details
                class_query = """
                    SELECT class_name, class_date, start_time, capacity,
                           (SELECT COUNT(*) FROM ClassEnrollment 
                            WHERE class_id = %s AND status = 'enrolled') as current_enrollment
                    FROM GroupClass
                    WHERE class_id = %s AND status = 'scheduled';
                """
                cursor.execute(class_query, (class_id, class_id))
                class_info = cursor.fetchone()
                
                if not class_info:
                    print(f"✗ Class not found or not available")
                    return None
                
                # Insert enrollment (trigger will check capacity)
                query = """
                    INSERT INTO ClassEnrollment (member_id, class_id, status)
                    VALUES (%s, %s, 'enrolled')
                    RETURNING enrollment_id;
                """
                cursor.execute(query, (member_id, class_id))
                enrollment_id = cursor.fetchone()[0]
                
                print(f"✓ Successfully enrolled in class!")
                print(f"  Enrollment ID: {enrollment_id}")
                print(f"  Class: {class_info[0]}")
                print(f"  Date: {class_info[1]} at {class_info[2]}")
                print(f"  Spots filled: {class_info[4] + 1}/{class_info[3]}")
                return enrollment_id
                
        except Exception as e:
            print(f"✗ Error registering for class: {e}")
            return None
    
    @staticmethod
    def get_member_info(member_id):
        """Helper function to retrieve member information"""
        try:
            with DatabaseConnection.get_cursor() as cursor:
                query = """
                    SELECT member_id, first_name, last_name, email, phone, 
                           date_of_birth, gender, registration_date
                    FROM Member
                    WHERE member_id = %s;
                """
                cursor.execute(query, (member_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"✗ Error retrieving member info: {e}")
            return None


# Demo functions for testing
def demo_member_operations():
    """Demonstrates all member operations"""
    print("\n" + "="*60)
    print("MEMBER OPERATIONS DEMO")
    print("="*60 + "\n")
    
    # Operation 1: Register new member
    print("1. REGISTERING NEW MEMBER")
    print("-" * 40)
    member_id = MemberOperations.register_member(
        "Alice", "Cooper", "alice.cooper@email.com", "555-9999",
        "1993-04-12", "Female"
    )
    
    if member_id:
        # Operation 2: Update profile and add goal
        print("\n2. UPDATING PROFILE AND ADDING FITNESS GOAL")
        print("-" * 40)
        MemberOperations.update_profile(
            member_id,
            phone="555-8888",
            goal_type="weight_loss",
            target_value=140.0,
            current_value=160.0,
            target_date="2025-08-01"
        )
        
        # Operation 3: Add health metrics
        print("\n3. RECORDING HEALTH METRICS")
        print("-" * 40)
        MemberOperations.add_health_metric(
            member_id,
            weight=160.0,
            height=66.0,
            heart_rate=72,
            body_fat_percentage=28.5,
            notes="Initial baseline measurement"
        )
        
        # Operation 4: View dashboard
        print("\n4. VIEWING MEMBER DASHBOARD")
        print("-" * 40)
        MemberOperations.view_dashboard(member_id)
        
        # Operation 5: Schedule PT session (using existing trainer and room)
        print("\n5. SCHEDULING PERSONAL TRAINING SESSION")
        print("-" * 40)
        MemberOperations.schedule_pt_session(
            member_id, 1, 3, "2025-11-26", "14:00:00", "15:00:00"
        )
        
        # Operation 6: Register for group class
        print("\n6. REGISTERING FOR GROUP CLASS")
        print("-" * 40)
        MemberOperations.register_for_class(member_id, 1)


if __name__ == "__main__":
    from db_connection import get_db_config
    
    # Initialize database connection
    config = get_db_config()
    DatabaseConnection.initialize_pool(**config)
    
    try:
        demo_member_operations()
    finally:
        DatabaseConnection.close_all_connections()
