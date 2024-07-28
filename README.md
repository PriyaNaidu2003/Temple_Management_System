Temple Management System


The Temple Management System is a web application designed to manage temple-related data and functionalities. It allows users to register, login, and view various details related to temples, visitors, donations, and visits. Administrators have additional functionalities to view, insert, and delete data from the database.

Features


1.User Registration and Login: Users can register and login to access their account.


2.Role Selection: Users can choose between different roles (User or Admin) to access relevant functionalities.


3.Admin Functionalities:

  ->View details of temples, visitors, donations, and visits.
  
  ->Insert new data into the database.
  
  ->Delete rows from the database.

  
4.User Functionalities:

  ->View temple details.
  
  ->View donation details.
  
  ->View visit details.
  
  ->View temple with the most visits.
  
  ->View visitor with the most visits to each temple.
  
  ->View visitors based on purpose and gender.
  
  ->View highest donations.

  
5.Session Management: User sessions are managed to ensure secure access to functionalities.


6.Database Integration: MySQL is used to store and retrieve data.

7.Requirements

  ->Python 3.x
  
  ->Flask
  
  ->MySQL Connector for Python

  
8.Usage

  ->Register as a new user:
  
      Navigate to the register page and provide a valid username and password.
      
      Follow the password requirements: at least 8 characters, including alphabets, numbers, and special 
      characters.

      
  ->Login as a user or admin:
  
      Navigate to the login page and provide your credentials.
      
      Admins have access to additional functionalities such as viewing, inserting, and deleting data.
      

      
  ->Navigate through the functionalities:
  
      Use the navigation links to access different functionalities based on your role.

      
  ->Logout:
  
      Click on the logout button to end your session and return to the main page.
