"""
Health and Fitness Club Management System
Main Application Entry Point

This application demonstrates all required functionality for a team of 2:
- 8 Entities in ER Model
- 8 Relationships
- 10 Total Operations (6 Member + 2 Trainer + 2 Admin)
- 1 View (MemberDashboard)
- 1 Trigger (check_room_availability_pt)
- 1 Index (idx_member_email and others)
"""

import sys
from db_connection import DatabaseConnection, get_db_config
from member_operations import MemberOperations
from trainer_operations import TrainerOperations
from admin_operations import AdminOperations


def print_header():
    """Print application header"""
    print("\n" + "="*70)
    print(" " * 10 + "HEALTH AND FITNESS CLUB MANAGEMENT SYSTEM")
    print("="*70)


def member_menu():
    """Member operations menu"""
    while True:
        print("\n" + "-"*70)
        print("MEMBER OPERATIONS")
        print("-"*70)
        print("1. Register New Member")
        print("2. Update Profile & Add Fitness Goal")
        print("3. Record Health Metrics")
        print("4. View Dashboard")
        print("5. Schedule Personal Training Session")
        print("6. Register for Group Class")
        print("0. Back to Main Menu")
        print("-"*70)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print("\n--- Register New Member ---")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            gender = input("Gender (Male/Female/Other): ").strip()
            
            member_id = MemberOperations.register_member(
                first_name, last_name, email, phone, dob, gender
            )
            if member_id:
                print(f"\n✓ Registration successful! Your Member ID is: {member_id}")
        
        elif choice == '2':
            print("\n--- Update Profile ---")
            member_id = int(input("Member ID: ").strip())
            phone = input("New Phone (or press Enter to skip): ").strip()
            email = input("New Email (or press Enter to skip): ").strip()
            
            add_goal = input("Add fitness goal? (y/n): ").strip().lower()
            
            kwargs = {}
            if phone:
                kwargs['phone'] = phone
            if email:
                kwargs['email'] = email
            
            if add_goal == 'y':
                print("Goal Types: weight_loss, muscle_gain, endurance, flexibility, general_fitness")
                kwargs['goal_type'] = input("Goal Type: ").strip()
                kwargs['target_value'] = float(input("Target Value: ").strip())
                kwargs['current_value'] = float(input("Current Value: ").strip())
                kwargs['target_date'] = input("Target Date (YYYY-MM-DD): ").strip()
            
            MemberOperations.update_profile(member_id, **kwargs)
        
        elif choice == '3':
            print("\n--- Record Health Metrics ---")
            member_id = int(input("Member ID: ").strip())
            weight = input("Weight (lbs, or press Enter to skip): ").strip()
            height = input("Height (inches, or press Enter to skip): ").strip()
            heart_rate = input("Heart Rate (bpm, or press Enter to skip): ").strip()
            body_fat = input("Body Fat % (or press Enter to skip): ").strip()
            notes = input("Notes: ").strip()
            
            MemberOperations.add_health_metric(
                member_id,
                weight=float(weight) if weight else None,
                height=float(height) if height else None,
                heart_rate=int(heart_rate) if heart_rate else None,
                body_fat_percentage=float(body_fat) if body_fat else None,
                notes=notes if notes else None
            )
        
        elif choice == '4':
            print("\n--- View Dashboard ---")
            member_id = int(input("Member ID: ").strip())
            MemberOperations.view_dashboard(member_id)
        
        elif choice == '5':
            print("\n--- Schedule PT Session ---")
            member_id = int(input("Member ID: ").strip())
            trainer_id = int(input("Trainer ID: ").strip())
            room_id = int(input("Room ID: ").strip())
            session_date = input("Session Date (YYYY-MM-DD): ").strip()
            start_time = input("Start Time (HH:MM:SS): ").strip()
            end_time = input("End Time (HH:MM:SS): ").strip()
            
            MemberOperations.schedule_pt_session(
                member_id, trainer_id, room_id, session_date, start_time, end_time
            )
        
        elif choice == '6':
            print("\n--- Register for Group Class ---")
            member_id = int(input("Member ID: ").strip())
            class_id = int(input("Class ID: ").strip())
            
            MemberOperations.register_for_class(member_id, class_id)
        
        elif choice == '0':
            break
        
        else:
            print("✗ Invalid choice. Please try again.")


def trainer_menu():
    """Trainer operations menu"""
    while True:
        print("\n" + "-"*70)
        print("TRAINER OPERATIONS")
        print("-"*70)
        print("1. Set Availability")
        print("2. View Schedule")
        print("3. Look Up Member")
        print("0. Back to Main Menu")
        print("-"*70)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print("\n--- Set Availability ---")
            trainer_id = int(input("Trainer ID: ").strip())
            print("Day of Week: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday")
            day_of_week = int(input("Day of Week (0-6): ").strip())
            start_time = input("Start Time (HH:MM:SS): ").strip()
            end_time = input("End Time (HH:MM:SS): ").strip()
            
            TrainerOperations.set_availability(trainer_id, day_of_week, start_time, end_time)
        
        elif choice == '2':
            print("\n--- View Schedule ---")
            trainer_id = int(input("Trainer ID: ").strip())
            start_date = input("Start Date (YYYY-MM-DD, or press Enter for all): ").strip()
            end_date = input("End Date (YYYY-MM-DD, or press Enter for all): ").strip()
            
            TrainerOperations.view_schedule(
                trainer_id,
                start_date if start_date else None,
                end_date if end_date else None
            )
        
        elif choice == '3':
            print("\n--- Look Up Member ---")
            trainer_id = int(input("Trainer ID: ").strip())
            member_name = input("Member Name (first or last): ").strip()
            
            TrainerOperations.lookup_member(trainer_id, member_name)
        
        elif choice == '0':
            break
        
        else:
            print("✗ Invalid choice. Please try again.")


def admin_menu():
    """Admin operations menu"""
    while True:
        print("\n" + "-"*70)
        print("ADMIN OPERATIONS")
        print("-"*70)
        print("1. Manage Room Booking")
        print("2. Manage Equipment")
        print("3. Manage Class Schedule")
        print("4. Manage Billing & Payments")
        print("0. Back to Main Menu")
        print("-"*70)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            print("\n--- Manage Room Booking ---")
            print("Booking Type: pt_session or group_class")
            booking_type = input("Booking Type: ").strip()
            room_id = int(input("Room ID: ").strip())
            date = input("Date (YYYY-MM-DD): ").strip()
            start_time = input("Start Time (HH:MM:SS): ").strip()
            end_time = input("End Time (HH:MM:SS): ").strip()
            trainer_id = int(input("Trainer ID: ").strip())
            
            if booking_type == 'pt_session':
                member_id = int(input("Member ID: ").strip())
                AdminOperations.manage_room_booking(
                    room_id, booking_type, date, start_time, end_time,
                    trainer_id=trainer_id, member_id=member_id
                )
            else:
                class_name = input("Class Name: ").strip()
                capacity = int(input("Capacity: ").strip())
                AdminOperations.manage_room_booking(
                    room_id, booking_type, date, start_time, end_time,
                    trainer_id=trainer_id, class_name=class_name, capacity=capacity
                )
        
        elif choice == '2':
            print("\n--- Manage Equipment ---")
            print("Actions: view, add, update_status, log_maintenance")
            action = input("Action: ").strip()
            
            if action == 'view':
                eq_id = input("Equipment ID (or press Enter for all): ").strip()
                AdminOperations.manage_equipment(
                    equipment_id=int(eq_id) if eq_id else None,
                    action='view'
                )
            elif action == 'add':
                name = input("Equipment Name: ").strip()
                room_id = int(input("Room ID: ").strip())
                AdminOperations.manage_equipment(
                    action='add',
                    equipment_name=name,
                    room_id=room_id
                )
            elif action == 'update_status':
                eq_id = int(input("Equipment ID: ").strip())
                print("Status: operational, maintenance, broken, retired")
                status = input("New Status: ").strip()
                AdminOperations.manage_equipment(
                    equipment_id=eq_id,
                    action='update_status',
                    status=status
                )
            elif action == 'log_maintenance':
                eq_id = int(input("Equipment ID: ").strip())
                AdminOperations.manage_equipment(
                    equipment_id=eq_id,
                    action='log_maintenance'
                )
        
        elif choice == '3':
            print("\n--- Manage Class Schedule ---")
            print("Actions: view, create, update, cancel")
            action = input("Action: ").strip()
            
            if action == 'view':
                class_id = input("Class ID (or press Enter for all): ").strip()
                AdminOperations.manage_class_schedule(
                    action='view',
                    class_id=int(class_id) if class_id else None
                )
            elif action == 'create':
                name = input("Class Name: ").strip()
                trainer_id = int(input("Trainer ID: ").strip())
                room_id = int(input("Room ID: ").strip())
                date = input("Date (YYYY-MM-DD): ").strip()
                start_time = input("Start Time (HH:MM:SS): ").strip()
                end_time = input("End Time (HH:MM:SS): ").strip()
                capacity = int(input("Capacity: ").strip())
                
                AdminOperations.manage_class_schedule(
                    action='create',
                    class_name=name,
                    trainer_id=trainer_id,
                    room_id=room_id,
                    class_date=date,
                    start_time=start_time,
                    end_time=end_time,
                    capacity=capacity
                )
            elif action == 'cancel':
                class_id = int(input("Class ID: ").strip())
                AdminOperations.manage_class_schedule(action='cancel', class_id=class_id)
        
        elif choice == '4':
            print("\n--- Manage Billing & Payments ---")
            print("Actions: view, create_bill, record_payment, view_member_bills")
            action = input("Action: ").strip()
            
            if action == 'view':
                bill_id = input("Bill ID (or press Enter for all): ").strip()
                AdminOperations.manage_billing(
                    action='view',
                    bill_id=int(bill_id) if bill_id else None
                )
            elif action == 'create_bill':
                member_id = int(input("Member ID: ").strip())
                amount = float(input("Amount: ").strip())
                description = input("Description: ").strip()
                
                AdminOperations.manage_billing(
                    action='create_bill',
                    member_id=member_id,
                    amount=amount,
                    description=description
                )
            elif action == 'record_payment':
                bill_id = int(input("Bill ID: ").strip())
                print("Payment Methods: Cash, Credit Card, Debit Card, Bank Transfer")
                method = input("Payment Method: ").strip()
                
                AdminOperations.manage_billing(
                    action='record_payment',
                    bill_id=bill_id,
                    payment_method=method
                )
            elif action == 'view_member_bills':
                member_id = int(input("Member ID: ").strip())
                AdminOperations.manage_billing(
                    action='view_member_bills',
                    member_id=member_id
                )
        
        elif choice == '0':
            break
        
        else:
            print("✗ Invalid choice. Please try again.")


def main_menu():
    """Main application menu"""
    while True:
        print_header()
        print("\nMAIN MENU")
        print("-"*70)
        print("1. Member Operations")
        print("2. Trainer Operations")
        print("3. Admin Operations")
        print("0. Exit")
        print("-"*70)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            member_menu()
        elif choice == '2':
            trainer_menu()
        elif choice == '3':
            admin_menu()
        elif choice == '0':
            print("\n✓ Thank you for using the Health and Fitness Club Management System!")
            print("="*70 + "\n")
            break
        else:
            print("✗ Invalid choice. Please try again.")


def main():
    """Main application entry point"""
    try:
        # Initialize database connection
        print("Initializing database connection...")
        config = get_db_config()
        DatabaseConnection.initialize_pool(**config)
        print("✓ Connected to database successfully!\n")
        
        # Run main menu
        main_menu()
        
    except Exception as e:
        print(f"\n✗ Application error: {e}")
        sys.exit(1)
    
    finally:
        # Clean up database connections
        DatabaseConnection.close_all_connections()


if __name__ == "__main__":
    main()
