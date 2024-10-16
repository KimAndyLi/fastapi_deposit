# fastapi_deposit
Deposit Calculation API

### Project Setup and Running:

1. **Install Docker:**
   - Make sure Docker is installed on your machine. You can download and install Docker from [here](https://www.docker.com/products/docker-desktop).

2. **Automatic Table Creation:**
   - The `log` table is automatically created in the MySQL database using the `init.sql` script during container initialization. No need to manually create the table.

3. **Run the application:**
   - Start the project using Docker Compose:
     ```bash
     docker-compose up --build
     ```

---

The API will now be running on `http://localhost:8000`.