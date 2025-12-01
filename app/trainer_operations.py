"""
Trainer Operations Module
Implements all trainer-related functionality for the Health and Fitness Club Management System

Required Operations:
1. Set Availability
2. Schedule View
3. Member Lookup
"""

from db_connection import DatabaseConnection


class TrainerOperations:
    """Handles all trainer-related database operations"""
    
    @staticmethod
    def set_availability(trainer_id, day_of_week, start_time, end_time, is_available=True):
        """
        Operation 1: Set Availability
        Defines time windows when available for sessions or classes
        Prevents overlapping time slots for the same trainer
        
        day_of_week: 0=Sunday, 1=Monday, ..., 6=Saturday
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                # Check for overlapping availability slots
                overlap_query = """
                    SELECT availability_id FROM TrainerAvailability
                    WHERE trainer_id = %s 
                    AND day_of_week = %s
                    AND (
                        (%s >= start_time AND %s < end_time)
                        OR (%s > start_time AND %s <= end_time)
                        OR (%s <= start_time AND %s >= end_time)
                    );
                """
                cursor.execute(overlap_query, (
                    trainer_id, day_of_week,
                    start_time, start_time,
                    end_time, end_time,
                    start_time, end_time
                ))
                
                if cursor.fetchone():
                    print(f"✗ Overlapping availability slot exists for this time")
                    return None
                
                # Insert new availability
                query = """
                    INSERT INTO TrainerAvailability 
                    (trainer_id, day_of_week, start_time, end_time, is_available)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING availability_id;
                """
                cursor.execute(query, (trainer_id, day_of_week, start_time, end_time, is_available))
                avail_id = cursor.fetchone()[0]
                
                days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                print(f"✓ Availability set successfully!")
                print(f"  Availability ID: {avail_id}")
                print(f"  Day: {days[day_of_week]}")
                print(f"  Time: {start_time} - {end_time}")
                print(f"  Available: {is_available}")
                return avail_id
                
        except Exception as e:
            print(f"✗ Error setting availability: {e}")
            return None
    
    @staticmethod
    def view_schedule(trainer_id, start_date=None, end_date=None):
        """
        Operation 2: Schedule View
        Shows assigned PT sessions and classes
        Allows trainer to prepare for each session in advance
        """
        try:
            with DatabaseConnection.get_cursor() as cursor:
                # Get trainer info
                cursor.execute("""
                    SELECT first_name, last_name, specialization 
                    FROM Trainer WHERE trainer_id = %s
                """, (trainer_id,))
                trainer_info = cursor.fetchone()
                
                if not trainer_info:
                    print(f"✗ Trainer not found")
                    return None
                
                print("\n" + "="*70)
                print(f"SCHEDULE FOR: {trainer_info[0]} {trainer_info[1]} ({trainer_info[2]})")
                print("="*70)
                
                # Get PT sessions
                pt_query = """
                    SELECT pts.session_id, pts.session_date, pts.start_time, pts.end_time,
                           m.first_name, m.last_name, r.room_name, pts.status
                    FROM PersonalTrainingSession pts
                    JOIN Member m ON pts.member_id = m.member_id
                    JOIN Room r ON pts.room_id = r.room_id
                    WHERE pts.trainer_id = %s
                """
                params = [trainer_id]
                
                if start_date and end_date:
                    pt_query += " AND pts.session_date BETWEEN %s AND %s"
                    params.extend([start_date, end_date])
                
                pt_query += " ORDER BY pts.session_date, pts.start_time"
                
                cursor.execute(pt_query, params)
                pt_sessions = cursor.fetchall()
                
                print("\nPERSONAL TRAINING SESSIONS:")
                print("-" * 70)
                if pt_sessions:
                    for session in pt_sessions:
                        print(f"  [{session[0]}] {session[1]} | {session[2]}-{session[3]} | "
                              f"{session[4]} {session[5]} | Room: {session[6]} | Status: {session[7]}")
                else:
                    print("  No personal training sessions scheduled")
                
                # Get group classes
                class_query = """
                    SELECT gc.class_id, gc.class_name, gc.class_date, 
                           gc.start_time, gc.end_time, r.room_name,
                           gc.capacity,
                           (SELECT COUNT(*) FROM ClassEnrollment 
                            WHERE class_id = gc.class_id AND status = 'enrolled') as enrolled,
                           gc.status
                    FROM GroupClass gc
                    JOIN Room r ON gc.room_id = r.room_id
                    WHERE gc.trainer_id = %s
                """
                params = [trainer_id]
                
                if start_date and end_date:
                    class_query += " AND gc.class_date BETWEEN %s AND %s"
                    params.extend([start_date, end_date])
                
                class_query += " ORDER BY gc.class_date, gc.start_time"
                
                cursor.execute(class_query, params)
                classes = cursor.fetchall()
                
                print("\nGROUP CLASSES:")
                print("-" * 70)
                if classes:
                    for cls in classes:
                        print(f"  [{cls[0]}] {cls[1]} | {cls[2]} | {cls[3]}-{cls[4]} | "
                              f"Room: {cls[5]} | Enrolled: {cls[7]}/{cls[6]} | Status: {cls[8]}")
                else:
                    print("  No group classes scheduled")
                
                print("="*70 + "\n")
                
                return {'pt_sessions': pt_sessions, 'classes': classes}
                
        except Exception as e:
            print(f"✗ Error viewing schedule: {e}")
            return None
    
    @staticmethod
    def lookup_member(trainer_id, member_name):
        """
        Operation 3: Member Lookup
        Searches by name (case-insensitive) and views current goal and last metric
        Trainers can only view, not edit member data (preserves data privacy)
        """
        try:
            with DatabaseConnection.get_cursor() as cursor:
                # Search for members (case-insensitive)
                search_query = """
                    SELECT m.member_id, m.first_name, m.last_name, m.email, m.phone
                    FROM Member m
                    WHERE LOWER(m.first_name || ' ' || m.last_name) LIKE LOWER(%s)
                    ORDER BY m.last_name, m.first_name;
                """
                cursor.execute(search_query, (f"%{member_name}%",))
                members = cursor.fetchall()
                
                if not members:
                    print(f"✗ No members found matching '{member_name}'")
                    return None
                
                print("\n" + "="*70)
                print(f"MEMBER SEARCH RESULTS: '{member_name}'")
                print("="*70)
                
                for member in members:
                    member_id = member[0]
                    print(f"\nMember ID: {member_id}")
                    print(f"Name: {member[1]} {member[2]}")
                    print(f"Email: {member[3]}")
                    print(f"Phone: {member[4]}")
                    
                    # Get active goals
                    goal_query = """
                        SELECT goal_type, target_value, current_value, target_date
                        FROM FitnessGoal
                        WHERE member_id = %s AND status = 'active'
                        ORDER BY created_date DESC;
                    """
                    cursor.execute(goal_query, (member_id,))
                    goals = cursor.fetchall()
                    
                    print("\nActive Goals:")
                    if goals:
                        for goal in goals:
                            print(f"  - {goal[0]}: Current {goal[2]} → Target {goal[1]} by {goal[3]}")
                    else:
                        print("  No active goals")
                    
                    # Get latest health metric
                    metric_query = """
                        SELECT recorded_date, weight, height, heart_rate, body_fat_percentage, notes
                        FROM HealthMetric
                        WHERE member_id = %s
                        ORDER BY recorded_date DESC
                        LIMIT 1;
                    """
                    cursor.execute(metric_query, (member_id,))
                    metric = cursor.fetchone()
                    
                    print("\nLatest Health Metric:")
                    if metric:
                        print(f"  Date: {metric[0]}")
                        print(f"  Weight: {metric[1]} lbs" if metric[1] else "  Weight: N/A")
                        print(f"  Height: {metric[2]} inches" if metric[2] else "  Height: N/A")
                        print(f"  Heart Rate: {metric[3]} bpm" if metric[3] else "  Heart Rate: N/A")
                        print(f"  Body Fat: {metric[4]}%" if metric[4] else "  Body Fat: N/A")
                        if metric[5]:
                            print(f"  Notes: {metric[5]}")
                    else:
                        print("  No health metrics recorded")
                    
                    # Check if this member has sessions with this trainer
                    session_query = """
                        SELECT COUNT(*) FROM PersonalTrainingSession
                        WHERE member_id = %s AND trainer_id = %s
                    """
                    cursor.execute(session_query, (member_id, trainer_id))
                    session_count = cursor.fetchone()[0]
                    
                    print(f"\nTotal PT Sessions with you: {session_count}")
                    print("-" * 70)
                
                return members
                
        except Exception as e:
            print(f"✗ Error looking up member: {e}")
            return None
    
    @staticmethod
    def get_trainer_info(trainer_id):
        """Helper function to retrieve trainer information"""
        try:
            with DatabaseConnection.get_cursor() as cursor:
                query = """
                    SELECT trainer_id, first_name, last_name, email, phone, 
                           specialization, hire_date
                    FROM Trainer
                    WHERE trainer_id = %s;
                """
                cursor.execute(query, (trainer_id,))
                return cursor.fetchone()
        except Exception as e:
            print(f"✗ Error retrieving trainer info: {e}")
            return None


# Demo functions for testing
def demo_trainer_operations():
    """Demonstrates all trainer operations"""
    print("\n" + "="*60)
    print("TRAINER OPERATIONS DEMO")
    print("="*60 + "\n")
    
    trainer_id = 1  # Using existing trainer from sample data
    
    # Operation 1: Set availability
    print("1. SETTING TRAINER AVAILABILITY")
    print("-" * 40)
    TrainerOperations.set_availability(
        trainer_id, 6, "09:00:00", "13:00:00", True  # Saturday 9am-1pm
    )
    
    # Operation 2: View schedule
    print("\n2. VIEWING TRAINER SCHEDULE")
    print("-" * 40)
    TrainerOperations.view_schedule(trainer_id, "2025-11-20", "2025-11-30")
    
    # Operation 3: Member lookup
    print("\n3. LOOKING UP MEMBER INFORMATION")
    print("-" * 40)
    TrainerOperations.lookup_member(trainer_id, "John")


if __name__ == "__main__":
    from db_connection import get_db_config
    
    # Initialize database connection
    config = get_db_config()
    DatabaseConnection.initialize_pool(**config)
    
    try:
        demo_trainer_operations()
    finally:
        DatabaseConnection.close_all_connections()
