# R1. Identification of the problem you are trying to solve by building this particular app.

The app I built is a dental practice online booking system. I was talking with my friends and some of them are dentists, they said most dental practices in Australia still rely on phone call systems for booking appointments. Cause most of the practice is only 1-3 dentists, implementing an online booking system can require additional investment and staff training. This may not be feasible for smaller dental practices or those with limited resources.

# R2. Why is it a problem that needs solving?

There are lots of benefits of transferring from a phone call booking system to an online booking system for dental practices, even a small one.

Firstly, an online booking system allows patients to book appointments at any time, even outside of office hours. This convenience can increase patient satisfaction and attract new patients. It also can reduce the workload for reception staff, freeing up their time to focus on other tasks. Cause most of time, the reception staff also work as a dental assistent in some practice. This can lead to increased efficiency and productivity within the practice.

Patients can select from available time slots in real-time, ensuring accuracy and avoiding scheduling conflicts with the online booking system. Beside that, it can provide valuable data insights for dental practices, such as appointment history and patient demographics. This information can be used to improve patient experience and inform marketing strategies.

Finally, an online booking system can enhance communication between the practice and patients. Reminders and notifications can be automated, reducing no-shows and improving patient engagement.

Overall, transferring from a phone call booking system to an online booking system can provide numerous benefits for dental practices, including increased convenience, efficiency, accuracy, data insights, and patient engagement.

# R3. Why have you chosen this database system. What are the drawbacks compared to others?

I choose PostgreSQL database system for this project because it is an open source relational database management system. Since this project is about to build an API websever, I probably need to deal with a lots of JSON data. Because PostgreSQL allows JSON data to be stored as a native data type, which allows for efficient storage and retrieval of JSON data. It also provides a range of JSON fucntions and operators that allow for complex queries and manipulation of JSON data within the database. Beside that, PostgreSQL has strong security features, including SSL support, granular access controls, and encryption options. This makes it a good choice that handle sensitive data cause the booking system will have username and password.

The main drawbacks of PostgreSQL database system is it's complexity. It is a complex system that can be challenging for beginners. That means it has a steeper learning curve and may require more time and resources to set up and manage. PostgreSQL may perfor worse than others in some scenarios, like read-heavy workloads. The other drawback could be lack of third party tools and applications that are compatible with. For example, MySQL is more widely used and it easier to integrate into an existing technology stack.


ref: https://developer.okta.com/blog/2019/07/19/mysql-vs-postgres

# R4. Identify and discuss the key functionalities and benefits of an ORM

An ORM (Object-Relational Mapping) is a technique in programming that enables developers to establish a link between a relational database and an object-oriented programming language. By introducing a layer of abstraction between the application and the database, an ORM tool facilitates the manipulation of objects instead of tables and SQL queries.

Here are some key functionalities of ORM

1. Mapping between database tables and object-oriented classes:
- This allows developers to work with objects that represent database records, rather than dealing directly with the tables and records in the database. For example, in this project I have a table "users" in PostgreSQL database that stores information about users can be mapped to a User class in python.

2. Automatic generation of SQL queries.
- ORM tools can generate SQL queries automatically to perform database operations. Still use my project as example 

    ```py
    user = User.query.filter_by(username=user_name).first()
    user.f_name = "Eddy"
    db.session.commit()
    ```
    The ORM tool will automatically generate the SQL query to update the f_name of the user with the username = user_name based on the User Model, it saves developers time and effort.

3. Provides transaction management:
- In a transaction, all operations must either succeed or fail as a whole. If any operation in the transaction fails, the entire transaction is rolled back, and the database is left in its original state before the transaction began. This helps prevent data inconsistencies and ensure the data integrity. For example, if you have an e-commerce website. When a user purchases a product, the database must be updated to reflect the transaction. This involves subtracting the price of the product from the user's account balance, updating the inventory of the product, and recording the transaction in the order history. If any of these operations fail, the entire transaction must be rolled back, so the user's account balance is not incorrectly updated, the product inventory is not incorrectly reduced, and the order history is not incorrectly recorded. 

4. Provides security features.
- ORM tools provide security features such as parameterized queries, input validation, and protection against SQL injection attacks. This helps ensure that the application is secure and that data is protected from unauthorized access. For example, in this project, we define an ORM model for users table using SQLalchemy. If we try to find specific user, we use 
   ```
   user = User.query.filter_by(username=user_name).first()
   ```

   this is equal to 
   ```sql
   SELECT * FROM users WHERE username = :user_name LIMIT 1
   ```
   The username parameter is automatically escaped and sanitized by SQLAlchemy, preventing any attempt to inject malicious SQL code.

5. Provides support for database schema generation and migration.
- ORM tools can generate and update database schema automatically based on changes in the object model, making it easier to manage changes to the database schema over time.

6. Offers database abstraction
- ORM tools provide database abstraction, which allows developers to switch between different database systems without changing the code. For example, if a developer is using an ORM tool to interact with a MySQL database, they can switch to a PostgreSQL database by changing the database connection string without changing the code that interacts with the database.


# R5. Document all endpoints for your API


# R6. An ERD for your app

The original ERD when submit on the discord

![original](/docs/dental_original.jpg)

After discuss, the final ERD more focus on the core functions

![final](/docs/dental_final.jpg)