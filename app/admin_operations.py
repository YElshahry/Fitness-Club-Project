"""
Admin Operations Module
Implements all administrative staff functionality for the Health and Fitness Club Management System

Required Operations (2 minimum for team of 2):
1. Room Booking
2. Equipment Maintenance
3. Class Management
4. Billing & Payment
"""

from db_connection import DatabaseConnection
from datetime import datetime


class AdminOperations:
    """Handles all administrative database operations"""
    
    @staticmethod
    def manage_room_booking(room_id, booking_type, date, start_time, end_time, 
                           trainer_id=None, member_id=None, class_name=None, capacity=None):
        """
        Operation 1: Room Booking
        Assigns rooms for sessions or classes
        Prevents double-booking through database triggers
        
        booking_type: 'pt_session' or 'group_class'
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                # Check room exists and is available
                cursor.execute("""
                    SELECT room_name, room_type, status 
                    FROM Room WHERE room_id = %s
                """, (room_id,))
                room_info = cursor.fetchone()
                
                if not room_info:
                    print(f"✗ Room not found")
                    return None
                
                if room_info[2] != 'available':
                    print(f"✗ Room is currently {room_info[2]}")
                    return None
                
                if booking_type == 'pt_session':
                    if not (trainer_id and member_id):
                        print(f"✗ Trainer ID and Member ID required for PT session")
                        return None
                    
                    query = """
                        INSERT INTO PersonalTrainingSession 
                        (member_id, trainer_id, room_id, session_date, start_time, end_time, status)
                        VALUES (%s, %s, %s, %s, %s, %s, 'scheduled')
                        RETURNING session_id;
                    """
                    cursor.execute(query, (member_id, trainer_id, room_id, date, start_time, end_time))
                    booking_id = cursor.fetchone()[0]
                    
                    print(f"✓ PT Session booked successfully!")
                    print(f"  Session ID: {booking_id}")
                    print(f"  Room: {room_info[0]} ({room_info[1]})")
                    print(f"  Date: {date} from {start_time} to {end_time}")
                    return booking_id
                
                elif booking_type == 'group_class':
                    if not (trainer_id and class_name and capacity):
                        print(f"✗ Trainer ID, class name, and capacity required for group class")
                        return None
                    
                    query = """
                        INSERT INTO GroupClass 
                        (class_name, trainer_id, room_id, class_date, start_time, end_time, capacity, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'scheduled')
                        RETURNING class_id;
                    """
                    cursor.execute(query, (class_name, trainer_id, room_id, date, 
                                         start_time, end_time, capacity))
                    booking_id = cursor.fetchone()[0]
                    
                    print(f"✓ Group Class booked successfully!")
                    print(f"  Class ID: {booking_id}")
                    print(f"  Class: {class_name}")
                    print(f"  Room: {room_info[0]} ({room_info[1]})")
                    print(f"  Date: {date} from {start_time} to {end_time}")
                    print(f"  Capacity: {capacity}")
                    return booking_id
                
                else:
                    print(f"✗ Invalid booking type. Use 'pt_session' or 'group_class'")
                    return None
                    
        except Exception as e:
            print(f"✗ Error managing room booking: {e}")
            return None
    
    @staticmethod
    def manage_equipment(equipment_id=None, action='view', **kwargs):
        """
        Operation 2: Equipment Maintenance
        Logs issues, tracks repair status, assigns repair tasks, updates maintenance records
        
        Actions: 'view', 'add', 'update_status', 'log_maintenance'
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                if action == 'view':
                    # View all equipment or specific equipment
                    if equipment_id:
                        query = """
                            SELECT e.equipment_id, e.equipment_name, r.room_name,
                                   e.purchase_date, e.status, e.last_maintenance_date
                            FROM Equipment e
                            JOIN Room r ON e.room_id = r.room_id
                            WHERE e.equipment_id = %s;
                        """
                        cursor.execute(query, (equipment_id,))
                        equipment = cursor.fetchone()
                        
                        if equipment:
                            print(f"\nEquipment ID: {equipment[0]}")
                            print(f"Name: {equipment[1]}")
                            print(f"Location: {equipment[2]}")
                            print(f"Purchase Date: {equipment[3]}")
                            print(f"Status: {equipment[4]}")
                            print(f"Last Maintenance: {equipment[5]}")
                        else:
                            print(f"✗ Equipment not found")
                    else:
                        query = """
                            SELECT e.equipment_id, e.equipment_name, r.room_name,
                                   e.status, e.last_maintenance_date
                            FROM Equipment e
                            JOIN Room r ON e.room_id = r.room_id
                            ORDER BY e.status, e.equipment_name;
                        """
                        cursor.execute(query)
                        equipment_list = cursor.fetchall()
                        
                        print("\n" + "="*70)
                        print("EQUIPMENT INVENTORY")
                        print("="*70)
                        for eq in equipment_list:
                            status_marker = "⚠" if eq[3] in ['maintenance', 'broken'] else "✓"
                            print(f"{status_marker} [{eq[0]}] {eq[1]} | Room: {eq[2]} | "
                                  f"Status: {eq[3]} | Last Maint: {eq[4]}")
                        print("="*70 + "\n")
                    
                    return True
                
                elif action == 'add':
                    # Add new equipment
                    query = """
                        INSERT INTO Equipment (equipment_name, room_id, purchase_date, status)
                        VALUES (%s, %s, %s, %s)
                        RETURNING equipment_id;
                    """
                    cursor.execute(query, (
                        kwargs.get('equipment_name'),
                        kwargs.get('room_id'),
                        kwargs.get('purchase_date', datetime.now().date()),
                        kwargs.get('status', 'operational')
                    ))
                    new_id = cursor.fetchone()[0]
                    print(f"✓ Equipment added successfully! ID: {new_id}")
                    return new_id
                
                elif action == 'update_status':
                    # Update equipment status (operational, maintenance, broken, retired)
                    query = """
                        UPDATE Equipment 
                        SET status = %s
                        WHERE equipment_id = %s
                        RETURNING equipment_name, status;
                    """
                    cursor.execute(query, (kwargs.get('status'), equipment_id))
                    result = cursor.fetchone()
                    
                    if result:
                        print(f"✓ Equipment status updated!")
                        print(f"  {result[0]} → {result[1]}")
                        return True
                    else:
                        print(f"✗ Equipment not found")
                        return False
                
                elif action == 'log_maintenance':
                    # Log maintenance activity
                    query = """
                        UPDATE Equipment 
                        SET last_maintenance_date = %s,
                            status = CASE 
                                WHEN status = 'maintenance' THEN 'operational'
                                ELSE status
                            END
                        WHERE equipment_id = %s
                        RETURNING equipment_name, status;
                    """
                    cursor.execute(query, (
                        kwargs.get('maintenance_date', datetime.now().date()),
                        equipment_id
                    ))
                    result = cursor.fetchone()
                    
                    if result:
                        print(f"✓ Maintenance logged!")
                        print(f"  {result[0]} → Status: {result[1]}")
                        return True
                    else:
                        print(f"✗ Equipment not found")
                        return False
                
                else:
                    print(f"✗ Invalid action. Use: view, add, update_status, log_maintenance")
                    return None
                    
        except Exception as e:
            print(f"✗ Error managing equipment: {e}")
            return None
    
    @staticmethod
    def manage_class_schedule(action='view', class_id=None, **kwargs):
        """
        Operation 3: Class Management
        Defines new classes, assigns trainers/rooms/time, updates schedules
        
        Actions: 'view', 'create', 'update', 'cancel'
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                if action == 'view':
                    # View all classes or specific class with enrollment details
                    if class_id:
                        query = """
                            SELECT gc.class_id, gc.class_name, 
                                   t.first_name || ' ' || t.last_name as trainer,
                                   r.room_name, gc.class_date, gc.start_time, gc.end_time,
                                   gc.capacity, gc.status,
                                   (SELECT COUNT(*) FROM ClassEnrollment 
                                    WHERE class_id = gc.class_id AND status = 'enrolled') as enrolled
                            FROM GroupClass gc
                            JOIN Trainer t ON gc.trainer_id = t.trainer_id
                            JOIN Room r ON gc.room_id = r.room_id
                            WHERE gc.class_id = %s;
                        """
                        cursor.execute(query, (class_id,))
                        cls = cursor.fetchone()
                        
                        if cls:
                            print(f"\n{'='*60}")
                            print(f"CLASS DETAILS")
                            print(f"{'='*60}")
                            print(f"Class ID: {cls[0]}")
                            print(f"Name: {cls[1]}")
                            print(f"Trainer: {cls[2]}")
                            print(f"Room: {cls[3]}")
                            print(f"Date: {cls[4]}")
                            print(f"Time: {cls[5]} - {cls[6]}")
                            print(f"Enrollment: {cls[9]}/{cls[7]}")
                            print(f"Status: {cls[8]}")
                            print(f"{'='*60}\n")
                        else:
                            print(f"✗ Class not found")
                    else:
                        query = """
                            SELECT gc.class_id, gc.class_name, gc.class_date, 
                                   gc.start_time, t.first_name || ' ' || t.last_name as trainer,
                                   (SELECT COUNT(*) FROM ClassEnrollment 
                                    WHERE class_id = gc.class_id AND status = 'enrolled') as enrolled,
                                   gc.capacity, gc.status
                            FROM GroupClass gc
                            JOIN Trainer t ON gc.trainer_id = t.trainer_id
                            WHERE gc.class_date >= CURRENT_DATE
                            ORDER BY gc.class_date, gc.start_time;
                        """
                        cursor.execute(query)
                        classes = cursor.fetchall()
                        
                        print("\n" + "="*70)
                        print("CLASS SCHEDULE")
                        print("="*70)
                        for cls in classes:
                            print(f"[{cls[0]}] {cls[1]} | {cls[2]} {cls[3]} | "
                                  f"Trainer: {cls[4]} | {cls[5]}/{cls[6]} | Status: {cls[7]}")
                        print("="*70 + "\n")
                    
                    return True
                
                elif action == 'create':
                    # Create new class
                    query = """
                        INSERT INTO GroupClass 
                        (class_name, trainer_id, room_id, class_date, start_time, end_time, capacity, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'scheduled')
                        RETURNING class_id;
                    """
                    cursor.execute(query, (
                        kwargs.get('class_name'),
                        kwargs.get('trainer_id'),
                        kwargs.get('room_id'),
                        kwargs.get('class_date'),
                        kwargs.get('start_time'),
                        kwargs.get('end_time'),
                        kwargs.get('capacity')
                    ))
                    new_id = cursor.fetchone()[0]
                    print(f"✓ Class created successfully!")
                    print(f"  Class ID: {new_id}")
                    print(f"  Name: {kwargs.get('class_name')}")
                    return new_id
                
                elif action == 'update':
                    # Update class details
                    update_fields = []
                    values = []
                    
                    for field in ['class_name', 'trainer_id', 'room_id', 'class_date', 
                                 'start_time', 'end_time', 'capacity']:
                        if field in kwargs:
                            update_fields.append(f"{field} = %s")
                            values.append(kwargs[field])
                    
                    if update_fields:
                        values.append(class_id)
                        query = f"UPDATE GroupClass SET {', '.join(update_fields)} WHERE class_id = %s"
                        cursor.execute(query, values)
                        print(f"✓ Class updated successfully!")
                        return True
                    else:
                        print(f"✗ No fields to update")
                        return False
                
                elif action == 'cancel':
                    # Cancel class
                    query = """
                        UPDATE GroupClass 
                        SET status = 'cancelled'
                        WHERE class_id = %s
                        RETURNING class_name;
                    """
                    cursor.execute(query, (class_id,))
                    result = cursor.fetchone()
                    
                    if result:
                        print(f"✓ Class cancelled: {result[0]}")
                        return True
                    else:
                        print(f"✗ Class not found")
                        return False
                
                else:
                    print(f"✗ Invalid action. Use: view, create, update, cancel")
                    return None
                    
        except Exception as e:
            print(f"✗ Error managing class schedule: {e}")
            return None
    
    @staticmethod
    def manage_billing(action='view', member_id=None, bill_id=None, **kwargs):
        """
        Operation 4: Billing & Payment
        Generates bills, adds line items, records payments (simulated)
        Updates payment status and maintains transaction records
        
        Actions: 'view', 'create_bill', 'record_payment', 'view_member_bills'
        """
        try:
            with DatabaseConnection.get_cursor(commit=True) as cursor:
                if action == 'view':
                    # View all pending bills or specific bill
                    if bill_id:
                        query = """
                            SELECT b.bill_id, m.first_name || ' ' || m.last_name as member,
                                   b.bill_date, b.amount, b.description, 
                                   b.payment_status, b.payment_date, b.payment_method
                            FROM Billing b
                            JOIN Member m ON b.member_id = m.member_id
                            WHERE b.bill_id = %s;
                        """
                        cursor.execute(query, (bill_id,))
                        bill = cursor.fetchone()
                        
                        if bill:
                            print(f"\nBill ID: {bill[0]}")
                            print(f"Member: {bill[1]}")
                            print(f"Bill Date: {bill[2]}")
                            print(f"Amount: ${bill[3]:.2f}")
                            print(f"Description: {bill[4]}")
                            print(f"Status: {bill[5]}")
                            if bill[6]:
                                print(f"Payment Date: {bill[6]}")
                                print(f"Payment Method: {bill[7]}")
                        else:
                            print(f"✗ Bill not found")
                    else:
                        query = """
                            SELECT b.bill_id, m.first_name || ' ' || m.last_name as member,
                                   b.bill_date, b.amount, b.payment_status
                            FROM Billing b
                            JOIN Member m ON b.member_id = m.member_id
                            ORDER BY b.payment_status, b.bill_date DESC;
                        """
                        cursor.execute(query)
                        bills = cursor.fetchall()
                        
                        print("\n" + "="*70)
                        print("BILLING OVERVIEW")
                        print("="*70)
                        for bill in bills:
                            status_marker = "⚠" if bill[4] == 'pending' else "✓"
                            print(f"{status_marker} [{bill[0]}] {bill[1]} | "
                                  f"Date: {bill[2]} | Amount: ${bill[3]:.2f} | Status: {bill[4]}")
                        print("="*70 + "\n")
                    
                    return True
                
                elif action == 'create_bill':
                    # Create new bill for member
                    query = """
                        INSERT INTO Billing (member_id, amount, description, payment_status)
                        VALUES (%s, %s, %s, 'pending')
                        RETURNING bill_id;
                    """
                    cursor.execute(query, (
                        member_id,
                        kwargs.get('amount'),
                        kwargs.get('description')
                    ))
                    new_id = cursor.fetchone()[0]
                    print(f"✓ Bill created successfully!")
                    print(f"  Bill ID: {new_id}")
                    print(f"  Amount: ${kwargs.get('amount'):.2f}")
                    return new_id
                
                elif action == 'record_payment':
                    # Record payment for a bill (simulated)
                    query = """
                        UPDATE Billing 
                        SET payment_status = 'paid',
                            payment_date = %s,
                            payment_method = %s
                        WHERE bill_id = %s
                        RETURNING member_id, amount;
                    """
                    cursor.execute(query, (
                        kwargs.get('payment_date', datetime.now().date()),
                        kwargs.get('payment_method', 'Cash'),
                        bill_id
                    ))
                    result = cursor.fetchone()
                    
                    if result:
                        print(f"✓ Payment recorded successfully!")
                        print(f"  Bill ID: {bill_id}")
                        print(f"  Amount: ${result[1]:.2f}")
                        print(f"  Method: {kwargs.get('payment_method', 'Cash')}")
                        return True
                    else:
                        print(f"✗ Bill not found")
                        return False
                
                elif action == 'view_member_bills':
                    # View all bills for a specific member
                    query = """
                        SELECT bill_id, bill_date, amount, description, payment_status
                        FROM Billing
                        WHERE member_id = %s
                        ORDER BY bill_date DESC;
                    """
                    cursor.execute(query, (member_id,))
                    bills = cursor.fetchall()
                    
                    print(f"\n{'='*60}")
                    print(f"BILLING HISTORY - Member ID: {member_id}")
                    print(f"{'='*60}")
                    total = 0
                    for bill in bills:
                        print(f"[{bill[0]}] {bill[1]} | ${bill[2]:.2f} | {bill[3]} | {bill[4]}")
                        if bill[4] == 'pending':
                            total += bill[2]
                    print(f"{'='*60}")
                    print(f"Total Outstanding: ${total:.2f}")
                    print(f"{'='*60}\n")
                    
                    return bills
                
                else:
                    print(f"✗ Invalid action. Use: view, create_bill, record_payment, view_member_bills")
                    return None
                    
        except Exception as e:
            print(f"✗ Error managing billing: {e}")
            return None


# Demo functions for testing
def demo_admin_operations():
    """Demonstrates all admin operations"""
    print("\n" + "="*60)
    print("ADMIN OPERATIONS DEMO")
    print("="*60 + "\n")
    
    # Operation 1: Room booking
    print("1. MANAGING ROOM BOOKINGS")
    print("-" * 40)
    AdminOperations.manage_room_booking(
        room_id=4,
        booking_type='pt_session',
        date='2025-11-27',
        start_time='15:00:00',
        end_time='16:00:00',
        trainer_id=2,
        member_id=1
    )
    
    # Operation 2: Equipment maintenance
    print("\n2. MANAGING EQUIPMENT")
    print("-" * 40)
    AdminOperations.manage_equipment(action='view')
    AdminOperations.manage_equipment(
        equipment_id=4,
        action='update_status',
        status='operational'
    )
    
    # Operation 3: Class management
    print("\n3. MANAGING CLASS SCHEDULE")
    print("-" * 40)
    AdminOperations.manage_class_schedule(action='view')
    
    # Operation 4: Billing
    print("\n4. MANAGING BILLING & PAYMENTS")
    print("-" * 40)
    AdminOperations.manage_billing(action='view')
    bill_id = AdminOperations.manage_billing(
        action='create_bill',
        member_id=1,
        amount=75.00,
        description='Personal Training Session Package (5 sessions)'
    )
    if bill_id:
        AdminOperations.manage_billing(
            action='record_payment',
            bill_id=bill_id,
            payment_method='Credit Card'
        )


if __name__ == "__main__":
    from db_connection import get_db_config
    
    # Initialize database connection
    config = get_db_config()
    DatabaseConnection.initialize_pool(**config)
    
    try:
        demo_admin_operations()
    finally:
        DatabaseConnection.close_all_connections()
