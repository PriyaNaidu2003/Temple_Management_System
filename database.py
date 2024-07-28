import mysql.connector
class TempleDatabase:
    def __init__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()

    def connect_to_database(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Lakshmi@2023",
            port='3306',
            database="temple",
            autocommit=True  # Enable auto-commit 
        )

    def view_temple_details(self):
        li=[]
        self.cursor.execute("SELECT * FROM Temple")
        records = self.cursor.fetchall()
        for record in records:
            print(record)
            li.append(record)
        return li
    def view_Visitor_details(self):
        li=[]
        self.cursor.execute("SELECT * FROM Visitor")
        records = self.cursor.fetchall()
        for record in records:
            print(record)
            li.append(record)
        return li

    def view_donation_details(self):
        l=[]
        self.cursor.execute("SELECT * FROM Donation")
        records = self.cursor.fetchall()
        for record in records:
            print(record)
            l.append(record)
        return(l)

    def view_visits(self):
        l1=[]
        self.cursor.execute("SELECT * FROM Visit")
        records = self.cursor.fetchall()
        for record in records:
            print(record)
            l1.append(record)
        return(l1)
        

    def temple_most_visits(self):
        self.cursor.execute("""
            SELECT t.*, IFNULL(visit_count, 0) AS visit_count, IFNULL(visit_rank, 0) AS visit_rank
            FROM Temple t
            LEFT JOIN (
                SELECT TempleID, COUNT(*) AS visit_count, RANK() OVER (ORDER BY COUNT(*) DESC) AS visit_rank
                FROM Visit
                GROUP BY TempleID
            ) AS visit_counts_ranks ON t.TempleID = visit_counts_ranks.TempleID
            ORDER BY visit_rank ASC
        """)
        temple_details = self.cursor.fetchall()
       
        print("Temple with the most visits:")
        print(temple_details)
        return(temple_details)

    def visitor_most_visits_each_temple(self):
        l2=[]
        query = """
           SELECT TempleName, VisitorName, visit_count
            FROM (
                SELECT 
                    t.TempleName,
                    CONCAT(vv.FirstName, ' ', vv.LastName) AS VisitorName,
                    COUNT(*) AS visit_count,
                    RANK() OVER (PARTITION BY t.TempleID ORDER BY COUNT(*) DESC) AS visit_rank
                FROM Visit v
                JOIN Temple t ON v.TempleID = t.TempleID
                JOIN Visitor vv ON v.VisitorID = vv.VisitorID
                GROUP BY t.TempleID, vv.VisitorID
            ) AS ranked_visits
            WHERE visit_rank = 1;

        """

        self.cursor.execute(query)
        records = self.cursor.fetchall()

        print("Visitor who visited each temple the highest number of times:")
        for record in records:
            print(record)
            l2.append(record)
        return(l2)

    def view_visitors_based_on_purpose(self):
        l3=[]
        query = """
            SELECT Purpose, COUNT(*) AS visitor_count
            FROM Visit
            GROUP BY Purpose
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        print("Visitors grouped by purpose:")
        for record in records:
            print(record)
            l3.append(record)
        return(l3)

    def view_visitors_based_on_gender(self):
        l4=[]
        query = """
            SELECT Gender, COUNT(*) AS visitor_count
            FROM Visitor
            GROUP BY Gender
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        print("Visitors grouped by gender:")
        for record in records:
            print(record)
            l4.append(record)
        return(l4)

    def highest_donations(self):
        l=[]
        self.cursor.execute("""
            SELECT v.VisitorID, CONCAT(v.FirstName, ' ', v.LastName) AS VisitorName, 
                   SUM(d.DonationAmount) AS total_donation 
            FROM Donation d
            JOIN Visitor v ON d.VisitorID = v.VisitorID
            GROUP BY v.VisitorID, VisitorName
            ORDER BY total_donation DESC
        """)
        records = self.cursor.fetchall()
        print("Visitors who made the highest donations in descending order:")
        for record in records:
            visitor_id = record[0]
            visitor_name = record[1]
            total_donation = float(record[2]) 
            l.append(record) # Convert to float
            print(visitor_id, visitor_name, total_donation)
        return(l)
    # database.py

    def column_mod(self, table_name):
        columns=[]
        if table_name == "Temple":
            columns = ["TempleName", "Location", "YearBuilt", "ArchitecturalStyle"]
        elif table_name == "Visitor":
            columns = ["FirstName", "LastName", "Gender", "Age", "Address", "Phone"]
        elif table_name == "Visit":
            columns = ["VisitID","VisitorID", "TempleID", "VisitDate", "VisitTime", "Purpose"]
        elif table_name == "Donation":
            columns = ["VisitorID", "TempleID", "DonationAmount", "DonationDate", "PaymentMethod"]
        return columns

        
    def column(self,table_name):
        if table_name == "Temple":
            columns = ["TempleID","TempleName", "Location", "YearBuilt", "ArchitecturalStyle"]
        elif table_name == "Visitor":
            columns = ["VisitorID","FirstName", "LastName", "Gender", "Age", "Address", "Phone"]
        elif table_name == "Visit":
            columns = ["VisitID","VisitorID", "TempleID", "VisitDate", "VisitTime", "Purpose"]
        elif table_name == "Donation":
            columns = ["DonationID","VisitorID", "TempleID", "DonationAmount", "DonationDate", "PaymentMethod"]
        return(columns)
    def view_details(self,table_name):
        
        
        l=[]
        self.cursor.execute(f"SELECT * FROM {table_name}")
        records = self.cursor.fetchall()
        for record in records:
            print(record)
            l.append(record)
        return(l)

    def insert_data(self,table_name,columns,values):
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(values.values()))
        print("Data inserted successfully.")
    

    def delete_row(self,table_name,column_name,column_value):
        
            query = f"DELETE FROM {table_name} WHERE {column_name} = %s"
            self.cursor.execute(query, (column_value,))
            print("Row deleted successfully.")
        

    def is_admin(self, username, password):
        self.cursor.execute("SELECT * FROM User WHERE Username = %s AND Password = %s AND UserType = 'Admin'", (username, password))
        return self.cursor.fetchone() is not None

    def is_registered(self, username, password):
        self.cursor.execute("SELECT * FROM User WHERE Username = %s AND Password = %s and UserType='User' ", (username, password))
        return self.cursor.fetchone() is not None

    def register_user(self,username,password):
        
        self.cursor.execute("INSERT INTO User (Username, Password, UserType) VALUES (%s, %s, %s)", (username, password, "User"))

    def login_user(self):
        attempts = 0
        while attempts < 3:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if self.is_registered(username, password):
                user = self.login_user_from_db(username, password)
                if user:
                    print("User login successful.")
                    # User functionalities can be added here
                    while True:
                        print("\nUser Functionalities:")
                        print("1. View Temple Details")
                        print("2. View Donation Details")
                        print("3. View Visits")
                        print("4. View Temple with Most Visits")
                        print("5. View Visitor with Most Visits to Each Temple")
                        print("6. View Visitors with Highest Donations")
                        print("7. View Number of Visitors based on purpose")
                        print("8. View Number of Visitors based on gender")
                        print("9. Back to Main Menu")
                        choice = input("Enter your choice: ")

                        if choice == "1":
                            self.view_temple_details()
                        elif choice == "2":
                            self.view_donation_details()
                        elif choice == "3":
                            self.view_visits()
                        elif choice == "4":
                            self.temple_most_visits()
                        elif choice == "5":
                            self.visitor_most_visits_each_temple()
                        elif choice == "6":
                            print(self.highest_donations())
                        elif choice == "7":
                            self.view_visitors_based_on_purpose()
                        elif choice == "8":
                            self.view_visitors_based_on_gender()
                        elif choice == "9":
                            break
                        else:
                            print("Invalid choice.")
                else:
                    print("Invalid username or password for user.")
            else:
                print("User not found.")
            attempts += 1
            if attempts < 3:
                print("You have", 3 - attempts, "attempts remaining.")
            else:
                print("You have exceeded the maximum number of login attempts.")
                register_choice = input("Would you like to register? (yes/no): ").lower()
                if register_choice == "yes":
                    print("Please provide the following information to register:")
                    username = input("Username: ")
                    password = input("Password: ")
                    self.register_user(username,password)
                    print("User registered successfully. You can now login.")
                    self.login_user()
                    return
                else:
                    print("Returning to main menu.")
                    return

    def login_user_from_db(self, username, password):
        self.cursor.execute("SELECT * FROM User WHERE Username = %s AND Password = %s", (username, password))
        return self.cursor.fetchone()

    def admin_functionalities(self):
        while True:
            print("\nAdmin Functionalities:")
            print("1. View Details")
            print("2. Insert Data")
            print("3. Delete Row")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                print("Tables: Temple, Visitor, Visit, Donation")
                table_name = input("Enter the table name: ")
                self.view_details(table_name)
            elif choice == "2":
                print("Tables: Temple, Visitor, Visit, Donation")
                table_name = input("Enter the table name: ")
                columns=self.column_mod(table_name)
                #self.insert_data(table_name,columns)
            elif choice == "3":
                print("Tables: Temple, Visitor, Visit, Donation")
                table_name = input("Enter the table name: ")
                if table_name in ["Temple", "Visitor", "Visit", "Donation"]:
                    column_name = input("Enter column name: ")
                    column_value = input("Enter column value: ")
                    self.delete_row(table_name,column_name,column_value)
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def main(self):
        try:
            while True:
                print("\nWelcome to the Temple Database!")
                user_type = input("Are you an Admin or a User? (Admin/User): ").lower()

                if user_type == "admin":
                    attempts = 0
                    while attempts < 3:
                        username = input("Enter your Admin name: ")
                        password = input("Enter your password: ")
                        if self.is_admin(username, password):
                            print("Admin login successful.")
                            self.admin_functionalities()
                            break
                        else:
                            print("Invalid username or password for admin.")
                            attempts += 1
                            if attempts < 3:
                                print("You have", 3 - attempts, "attempts remaining.")
                            else:
                                print("You have exceeded the maximum number of login attempts. Returning to main menu.")
                                break
                elif user_type == "user":

                    user_choice = input("Do you want to login or register? (login/register): ").lower()

                    if user_choice == "login":
                        self.login_user()
                    elif user_choice == "register":
                        print("Please provide the following information to register:")
                        username = input("Username: ")
                        password = input("Password: ")
                        self.register_user(username,password)
                        login_choice = input("Would you like to login now? (yes/no): ").lower()
                        if login_choice == "yes":
                            self.login_user()
                    else:
                        print("Invalid choice.")





                else:
                    print("Invalid choice")

                exit_choice = input("Do you want to exit? (yes/no): ").lower()
                if exit_choice == "yes":
                    break

        except mysql.connector.Error as error:
            print("Error:", error)
        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")
    
if __name__ == "__main__":
    TempleDatabase().main()