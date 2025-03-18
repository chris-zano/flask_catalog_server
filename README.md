### **My Learnings from Building a Catalog Server**  

## **1. Introduction**  

When I started this project, I had no prior experience with Flask, PostgreSQL, Nginx, catalog servers, or systemd services. Every tool and technology I used was completely new to me, making this an exciting and challenging learning experience.  

The goal of this project was to build a **catalog server**—a system that stores and serves structured data about products. This required setting up a backend API, managing a database, configuring a web server, and ensuring everything runs smoothly in a production environment.

This report documents my journey, breaking down what I learned step by step—from setting up the development environment to deploying and automating my application.


### **2. Understanding the Concept of a Catalog Server**  

Before starting this project, I had no idea what a **catalog server** was. Through research and implementation, I learned that a catalog server is a specialized backend system designed to store and serve structured data—typically information about products, services, or metadata that can be queried by clients.  

#### **2.1 What is a Catalog Server?**  
A catalog server is essentially a database-driven API that allows users or applications to retrieve and manage product information efficiently. It is commonly used in:  
- **E-commerce platforms** (storing product details, prices, and availability)  
- **Library systems** (managing books, authors, and categories)  
- **Media streaming services** (organizing movies, genres, and recommendations)  
- **Inventory management** (tracking stock levels and suppliers)  

In my project, I implemented a simple **product catalog server** where the backend stores product details such as name, description, price, and creation date. Clients can query the catalog via an API to fetch product data.

---

#### **2.2 My Implementation of a Catalog Server**  
To build my catalog server, I needed three key components:  
1. **A database** to store product data  
2. **A Flask API** to expose endpoints for retrieving catalog information  
3. **A reverse proxy (Nginx)** to manage incoming requests and forward them to the API  

Here’s the architecture I followed:  

```
Client → Nginx (Reverse Proxy) → Flask API → PostgreSQL Database
```

- **Flask** serves as the backend framework, handling requests and fetching data.  
- **PostgreSQL** acts as the database, storing product information in a structured format.  
- **Nginx** is used as a reverse proxy to handle incoming traffic and forward it to Flask.  

This structure provides a clean separation of concerns, ensuring that the system is modular and scalable.

### **3. Setting Up the Development Environment**  

Before I could start writing any code, I needed to set up my development environment. This step was crucial because having the right tools and dependencies properly installed ensured a smooth workflow throughout the project. Since this was my first time working with Flask, PostgreSQL, and Nginx, I had to learn how to install, configure, and manage them from scratch.  

---

### **3.1 Installing Python and Setting Up a Virtual Environment**  
I started by installing Python and setting up a **virtual environment** to keep my project dependencies isolated from the system’s global packages. This prevents conflicts and makes it easier to manage dependencies.  

#### **Steps I Took:**  
1. **Installed Python & Pip:**  
   ```bash
   sudo apt install python3 python3-pip -y
   ```
2. **Created a virtual environment inside my project folder:**  
   ```bash
   python3 -m venv .venv
   ```
3. **Activated the virtual environment:**  
   ```bash
   source .venv/bin/activate
   ```
4. **Installed Flask and required dependencies:**  
   ```bash
   pip install flask flask-sqlalchemy psycopg2-binary gunicorn
   ```

🔹 *Lesson learned:* Virtual environments are a must-have for Python projects. They help keep dependencies clean and organized, making deployments much easier.

---

### **3.2 Setting Up PostgreSQL**  
Since my catalog server required a database, I needed to install and configure **PostgreSQL**.  

#### **Steps I Took:**  
1. **Installed PostgreSQL:**  
   ```bash
   sudo apt install postgresql postgresql-contrib -y
   ```
2. **Switch to the PostgreSQL User**
   ```bash
   sudo -i -u postgres
   ```
3. **Created a new database and user for the project:**  
   ```sql
   CREATE DATABASE catalog;
   CREATE USER catalog_user WITH ENCRYPTED PASSWORD 'catalog_pass';
   GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog_user;
   ```
4. **Restart PostgreSQL service:**  
   ```bash
   sudo systemctl restart postgresql
   ```
5. **Verified that PostgreSQL was running:**  
   ```bash
   sudo systemctl status postgresql
   ```

🔹 *Lesson learned:* PostgreSQL has strict user authentication rules. I had to edit the `pg_hba.conf` file to allow my application to connect.

---

### **3.3 Setting Up Flask for API Development**  
After installing Flask, I wrote a basic API to test if my setup was working. My `app.py` file looked like this:  

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Catalog Server is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

I ran my Flask app with:  
```bash
python app.py
```
Then, I checked if it was accessible in my browser at `http://127.0.0.1:8000/`.

🔹 *Lesson learned:* Running Flask locally was straightforward, but I knew I needed to configure **Gunicorn** and **Nginx** later for a production-ready deployment.

---

### **3.4 Setting Up Git for Version Control**  
To track my progress and ensure my work was backed up, I initialized a Git repository and pushed it to GitHub:  

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:chris-zano/flask_catalog_server.git
git push -u origin main
```

🔹 *Lesson learned:* Regular commits helped me keep track of changes and roll back if something broke.  

---

### **3.5 Setting Up Nginx (Preparation for Deployment)**  
Since my final setup would use **Nginx as a reverse proxy**, I installed it early:  

```bash
sudo apt install nginx -y
```

I didn’t configure it at this stage, but I verified that it was running:  
```bash
sudo systemctl status nginx
```

🔹 *Lesson learned:* Nginx will be useful later for handling incoming requests efficiently and improving security.

### **4. Learning Flask: Building the API Backend**

In this project, I dove headfirst into Flask to build the core of my catalog server. I learned how to create API endpoints, handle HTTP requests, and interact with a database—all by building a real, working application. Below, I detail my journey with Flask, including insights gained from working with the GitHub code.

#### **4.1 The Core of My Flask Application**

The heart of my project is the main Flask file (available in my [GitHub repository](https://github.com/chris-zano/flask_catalog_server)). This file not only defines the routes for the API endpoints but also sets up the database models and configuration. Here’s a brief overview of the structure:

- **Environment Setup:**  
  I used the `dotenv` package to load environment variables, making my application more secure and configurable. This allowed me to store sensitive information like the database URL outside of the code.

- **API Endpoints:**  
  I defined multiple endpoints to handle CRUD operations for products and users, as well as authentication and search functionality. For example:
  - The `/products` endpoint supports both GET (to retrieve all products) and POST (to add a new product).
  - Authentication endpoints (`/auth/login` and `/auth/register`) help manage user sessions.
  - The `/search` endpoint uses SQLAlchemy’s querying capabilities to perform case-insensitive searches on product names and descriptions.

- **Database Models:**  
  Using Flask-SQLAlchemy, I defined two models: `Products` and `Users`. These models encapsulate the structure of the database tables and include helpful methods like `__repr__` for debugging.

- **Cross-Origin Resource Sharing (CORS):**  
  I integrated CORS support to allow the API to be accessed from different domains, which is especially useful when the front end and back end are hosted on separate servers.

Below is a snippet of the key sections of my Flask code:

```python
# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define model for products
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    
    def __repr__(self):
        return f"<Product {self.name}>"

# ... Additional code for users and routes ...

if __name__ == "__main__":
    app.run(debug=True, port=8000)
```

#### **4.2 Key Learnings and Challenges**

- **Routing and Endpoints:**  
  I learned how to create dynamic endpoints that can handle various HTTP methods (GET, POST) and return JSON responses. This was crucial for building a RESTful API that clients can interact with.

- **Database Integration:**  
  Integrating SQLAlchemy with Flask helped me abstract away many of the complexities of direct SQL queries. I learned how to create models, query data, and handle database sessions efficiently.

- **Error Handling:**  
  Throughout the development process, I added error handling in my endpoints to gracefully manage and debug issues. This made my API more robust and easier to troubleshoot during testing.

- **Security Considerations:**  
  Using environment variables to store sensitive configuration details, such as the database URL, reinforced best practices in securing my application.

- **CORS and Cross-Domain Communication:**  
  Enabling CORS was an eye-opener in understanding how modern web applications often separate their front-end and back-end services. This experience highlighted the importance of ensuring smooth communication between different parts of an application.

#### **4.3 Reflecting on the Experience**

Building the Flask API backend was both challenging and immensely rewarding. It pushed me to understand how web servers work, how to design RESTful APIs, and how to integrate a relational database seamlessly into a Python web application. I now appreciate the elegance and simplicity that Flask offers, as well as the power it gives developers to build scalable, secure, and maintainable applications.

Overall, my journey with Flask transformed theoretical concepts into practical skills, setting a solid foundation for future projects. This learning experience has opened new horizons for me in backend development, and I look forward to exploring even more advanced topics in the future.

---

This concludes the section on Flask API development. Next, I’ll move on to discussing how I managed the database and integrated it with my application using PostgreSQL.

### **5. Database Management with PostgreSQL**

In this phase of the project, I dove into the world of relational databases by choosing PostgreSQL as my database management system. This was a whole new territory for me, and I quickly learned the importance of a well-configured database when it comes to handling real-world applications.

#### **5.1 Installing and Configuring PostgreSQL**

I started by installing PostgreSQL on my system:

```bash
sudo apt install postgresql postgresql-contrib -y
```

Once installed, I ensured that the PostgreSQL service was running by checking its status with:

```bash
sudo systemctl status postgresql
```

During this stage, I discovered that PostgreSQL has its own set of configuration files (like `postgresql.conf` and `pg_hba.conf`) that I needed to tweak to allow my application to connect. This was particularly enlightening, as I learned how user authentication and connection permissions are managed at a system level.

#### **5.2 Setting Up a Dedicated Database and User**

To keep things organized and secure, I created a dedicated database and a user for my catalog server. This approach minimizes security risks and isolates my application data from other systems. Here’s what I did:

1. Switched to the PostgreSQL user:
   ```bash
   sudo -i -u postgres
   ```
2. Created a new database called `catalog`:
   ```sql
   CREATE DATABASE catalog;
   ```
3. Created a new user, `catalog_user`, with a secure password:
   ```sql
   CREATE USER catalog_user WITH ENCRYPTED PASSWORD 'catalog_pass';
   ```
4. Granted all privileges on the `catalog` database to the new user:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog_user;
   ```

This not only gave me hands-on experience with SQL commands but also instilled best practices for database security and user management.

#### **5.3 Integrating PostgreSQL with Flask**

With PostgreSQL set up, I needed to connect it with my Flask application. Using SQLAlchemy as the ORM (Object Relational Mapper) made this integration seamless. I configured my Flask app to use the PostgreSQL database by setting the connection string in my environment variables:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
```

In my `.env` file, I set:
```
DATABASE_URL=postgresql://catalog_user:catalog_pass@localhost/catalog
```

This connection string tells Flask how to access my PostgreSQL database, allowing my application to execute queries and manage data effectively.

#### **5.4 Key Learnings and Challenges**

- **Understanding Database Architecture:**  
  I gained insights into how PostgreSQL manages connections, authentication, and data integrity. Configuring PostgreSQL was a significant step forward in understanding the backend of web applications.

- **SQL Proficiency:**  
  Writing SQL commands to create databases, tables, and users was both challenging and rewarding. I learned to appreciate the precision and structure that SQL brings to data management.

- **Security Best Practices:**  
  Managing users and permissions in PostgreSQL taught me the importance of limiting access and ensuring that only authorized applications can interact with the database.

- **Seamless Integration with Flask:**  
  By using SQLAlchemy, I discovered how to abstract the complexities of direct SQL interactions, allowing me to focus on writing clean, efficient Python code to interact with the database.

#### **5.5 Reflecting on the Experience**

Managing PostgreSQL was a turning point in my project. The challenges I faced in configuring and securing the database made me realize how critical database management is for any web application. Through this process, I learned to troubleshoot connection issues, adjust configurations, and ensure that my data is safely stored and easily accessible to my Flask API.

Overall, working with PostgreSQL was an invaluable part of my journey, reinforcing the importance of robust database management in building scalable and secure applications.

---

Next up, I'll discuss how I set up Nginx as a reverse proxy to route traffic efficiently to my Flask API.

### **6. Deploying with Nginx as a Reverse Proxy**  

After setting up my Flask API and PostgreSQL database, I needed a way to manage incoming requests efficiently. This is where **Nginx** came into play. I had never used Nginx before, so learning how to configure it as a reverse proxy was both exciting and challenging.  

#### **6.1 Why Use Nginx?**  
Initially, I was running my Flask app directly using:  
```bash
python app.py
```
or  
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
While this worked fine for development, it wasn’t suitable for production because:  
Flask’s built-in server is **not efficient** for handling multiple requests in production.  
I needed a way to **securely expose my API** to external users without directly exposing Flask.  
**Load balancing** and request handling were important considerations for scalability.  

Nginx acted as a **reverse proxy**, forwarding requests from clients to my Flask API running on port 8000.

---

#### **6.2 Installing and Configuring Nginx**  
First, I installed Nginx:  
```bash
sudo apt install nginx -y
```
After installation, I verified that Nginx was running:  
```bash
sudo systemctl status nginx
```
Then, I created a configuration file for my catalog server:  
```bash
sudo nano /etc/nginx/sites-available/catalog
```
Inside the file, I added the following configuration:  

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

This configuration does the following:  
- Listens for requests on **port 80** (default HTTP port).  
- Forwards all incoming traffic to Flask running on **port 8000**.  
- Passes along important headers like `X-Real-IP` to preserve client details.  

After saving the file, I enabled the configuration:  
```bash
sudo ln -s /etc/nginx/sites-available/catalog /etc/nginx/sites-enabled/
```
Then, I tested the configuration to ensure there were no syntax errors:  
```bash
sudo nginx -t
```
Finally, I restarted Nginx to apply the changes:  
```bash
sudo systemctl restart nginx
```

---

#### **6.3 Testing the Reverse Proxy**  
At this point, my Flask API was running on **port 8000**, and Nginx was forwarding requests from **port 80** to it. To test, I used:  
```bash
curl http://localhost/
```
If everything was set up correctly, I should receive a response from my Flask API.

---

#### **6.4 Key Learnings and Challenges**  
- **Understanding Reverse Proxies:**  
  Before this project, I didn’t fully understand the role of a reverse proxy. Now, I see how it acts as an intermediary between users and backend services, improving security and scalability.  

- **Debugging Nginx Issues:**  
  Initially, my configuration didn’t work due to permission issues and missing headers. Checking logs using `sudo journalctl -u nginx --no-pager | tail -50` helped me identify and fix these errors.  

- **Performance Gains:**  
  Running Flask behind Nginx made my API more efficient. Nginx handles requests faster, reducing the load on my application server.  

- **Security Considerations:**  
  Using Nginx means my Flask app **isn't directly exposed to the internet**, adding an extra layer of security. In a real-world scenario, I would also configure **HTTPS with Let’s Encrypt** for encrypted communication.  

---

#### **6.5 Reflecting on the Experience**  
Setting up Nginx was a game-changer. Before this project, I thought web servers were just for serving static websites, but now I understand their crucial role in API deployments. This knowledge will definitely help me in future projects when dealing with high-traffic applications.  

---

### **7. Automating with systemd Services**  

At this point, my Flask API was working, my database was set up, and Nginx was handling requests efficiently. However, there was one problem—whenever the server restarted, I had to manually start my Flask application.  

To fix this, I learned how to use **systemd** to run my Flask app as a background service that starts automatically on boot. This was my first experience with systemd, and setting it up was both challenging and rewarding.  

---

### **7.1 Why Use systemd?**  
Running `python app.py` or even `gunicorn` manually was not a sustainable solution.  
Using **systemd** provided:  
✅ **Automatic startup**—The app restarts on reboot.  
✅ **Process management**—If the app crashes, systemd restarts it.  
✅ **Background execution**—No need to keep a terminal open.  

---

### **7.2 Creating a systemd Service for Flask**  

#### **Step 1: Create the Service File**
I created a systemd service file:  
```bash
sudo nano /etc/systemd/system/catalog.service
```

#### **Step 2: Define the Service Configuration**  
Inside the file, I added:

```ini
[Unit]
Description=Catalog API Server
After=network.target

[Service]
User=niico
WorkingDirectory=/home/niico/catalog_server
ExecStart=/home/niico/catalog_server/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

##### **Explanation of the Configuration:**
- `Description=Catalog API Server` → Describes what this service does.  
- `After=network.target` → Ensures that the service starts **after** the network is available.  
- `User=niico` → Runs the service as my user instead of root (better security).  
- `WorkingDirectory=/home/niico/catalog_server` → The directory where my app is located.  
- `ExecStart` → Runs Gunicorn with **4 worker processes**, binding to port **8000**.  
- `Restart=always` → Ensures the service **automatically restarts** if it crashes.  
- `WantedBy=multi-user.target` → Starts the service at system boot.

---

### **7.3 Enabling and Starting the Service**  

After saving the file, I ran the following commands:  

#### **Step 1: Reload systemd**
```bash
sudo systemctl daemon-reload
```

#### **Step 2: Start the service**
```bash
sudo systemctl start catalog
```

#### **Step 3: Enable the service to start on boot**
```bash
sudo systemctl enable catalog
```

#### **Step 4: Check the Service Status**
```bash
sudo systemctl status catalog
```
If everything was configured correctly, I saw output similar to:

```
● catalog.service - Catalog API Server
   Loaded: loaded (/etc/systemd/system/catalog.service; enabled)
   Active: active (running) since Mon 2025-03-18 10:00:00 UTC; 30s ago
```

This confirmed that my Flask application was running in the background and would restart automatically if the server rebooted.

---

### **7.4 Debugging systemd Issues**  
Since this was my first time working with systemd, I ran into a few problems:  

**Incorrect Working Directory** → My service failed with `CHDIR` errors because I initially set the wrong path in `WorkingDirectory`. Fixing it solved the issue.  

**Gunicorn Not Found** → I had to make sure I was using the correct path inside my virtual environment:  
```bash
/home/niico/catalog_server/venv/bin/gunicorn
```
  
**Checking Logs for Errors** → To debug systemd issues, I used:  
```bash
journalctl -u catalog --no-pager --since "10 minutes ago"
```
This helped me identify why my service failed and fix it quickly.

---

### **7.5 Key Learnings and Takeaways**  
**systemd simplifies application management**—Now, my Flask app runs like a proper background service.  
**Understanding service dependencies**—Ensuring that my service starts **after the network is up** prevents failures.  
**Logging and troubleshooting**—Using `journalctl` to check logs was an important skill to learn.  
**Better process management**—My app now **automatically restarts** if it crashes, improving reliability.  

---

### **7.6 Reflecting on the Experience**  
Learning systemd was a **game-changer**. Before this, I didn’t know how Linux services worked, and I would have relied on manually restarting my app every time the server rebooted. Now, I have a fully automated and production-ready deployment.  

With systemd in place, my **entire stack (Flask, PostgreSQL, Nginx, and systemd) was now fully integrated and self-sustaining**.  

## Author

**Christian Solomon**  
📧 Email: [cncs.chris@gmail.com](mailto:cncs.chris@gmail.com)  
🔗 GitHub: [chris-zano](https://github.com/chris-zano)  
💼 LinkedIn: [Christian Solomon](https://www.linkedin.com/in/christianniisolomon/)  