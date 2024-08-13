from backend_engineer_interview.models import Employee, LeaveApplication
import logging as logger


logger = logger.getLogger('db.py')

class SQLDatabaseManager:
    def __init__(self, db_session, per_page_count=10):
        self.db_session = db_session
        self.per_page_count = per_page_count
    
    
    def get_employee_by_id(self, user_id, exclude_fields=None):
        with self.db_session() as session:
            query = session.query(Employee)
            employee = query.filter(Employee.id == user_id).first()
            if employee:
                employee = employee.as_dict()
                del employee['secret']
                return employee
        return None


    def get_all_employees(self):
        with self.db_session() as session:
            employees = session.query(Employee).all()
            if employees:
                return [employee.as_dict() for employee in employees]
        return []


    def update_employee(self, user_id, first_name=None, last_name=None, **kwargs):
        try:
            with self.db_session() as session:
                employee = session.query(Employee).filter(Employee.id == user_id).first()
                if employee:
                    if first_name:
                        employee.first_name = first_name 
                    if last_name:
                         employee.last_name = last_name 
                            
                    date_of_birth = kwargs.get("date_of_birth")
                    if date_of_birth:
                        employee.date_of_birth = date_of_birth 
            
                    logger.info(f"Email updated for user {user_id}") 
                else:
                    logger.error("Employee not found")
        except Exception as e:
            logger.error(f"error: {e}")
        return self.get_employee_by_id(user_id)


    def create_leave_application(self, employee_id=None, leave_start_date=None, leave_end_date=None):
        if employee_id and leave_start_date and leave_end_date:
            with self.db_session() as session:
                new_application = LeaveApplication(
                                    employee_id=employee_id, 
                                    leave_start_date=leave_start_date, 
                                    leave_end_date=leave_end_date
                                )
                session.add(new_application)
                logger.info(f"LeaveApplication {employee_id} created successfully.")
                return self.get_leave_application(employee_id=employee_id)
        return None
        
            
    def get_leave_application(self, employee_id=None, first_name=None, last_name=None):
        with self.db_session() as session:
            query = session.query(LeaveApplication)
            leave_application = query.filter(LeaveApplication.employee_id == employee_id).first()
            if leave_application:
                leave_application_dict = leave_application.as_dict()
                employee = self.get_employee_by_id(employee_id)
                if leave_application_dict.get('employee_id'):
                    del leave_application_dict['employee_id']
                if employee:
                    leave_application_dict['employee'] = employee
                return leave_application_dict
        return None
    
    
    def search_leave_applications(self, employee_id=None, first_name=None, last_name=None, page=None):
        with self.db_session() as session:
            query = session.query(LeaveApplication)
            # Apply filters
            if employee_id:
                query = query.filter(LeaveApplication.employee_id == employee_id == employee_id)
            # if first_name:
            #     query = query.filter(LeaveApplication.employee.first_name == first_name)
            # if last_name:
            #     query = query.filter(LeaveApplication.first_name.last_name == last_name)
            if page:
                query = query.limit(self.per_page_count).offset((int(page) - 1) * self.per_page_count)
                
            applications = query.all()
            if applications:
                return [application.as_dict() for application in applications]
        return []
    