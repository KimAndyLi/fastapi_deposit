# fastapi_deposit
Deposit Calculation API

### Project Setup and Running:

1. **Install Docker:**
   - Make sure Docker is installed on your machine. You can download and install Docker from [here](https://www.docker.com/products/docker-desktop).

2. **Run the MySQL container:**
   - Start the MySQL container if it's not running:
     ```bash
     docker exec -it mysql_db bash
     ```

3. **Create the `log` table in the MySQL database:**
   - Inside the MySQL container, connect to the database and create the `log` table:
     ```sql
     CREATE TABLE log (
         id INT AUTO_INCREMENT PRIMARY KEY,
         request_date VARCHAR(50),
         periods INT,
         amount DECIMAL(10, 2),
         rate DECIMAL(5, 2),
         results TEXT
     );
     ```

4. **Run the application:**
   - Start the project using Docker Compose:
     ```bash
     docker-compose up --build
     ```

---

The API will now be running on `http://localhost:8000`.