
# Django E-Commerce web application

This Django E-Commerce web application is a fully functional and customizable online store platform. It provides a robust foundation for 
building and managing an e-commerce website, allowing you to purchase products online with ease.

![](https://github.com/shashank026/zenatix-assignment/blob/main/readmeImage/Admin_Dashboard.gif)




## Features

- **User Registration and Authentication:** Users can create accounts, log in, and manage their profiles.
- **Product Catalog:** Display and categorize the products with detailed information such as title, description, price, and images.
- **Shopping Cart:** Users can add products to their cart, and proceed to checkout.
- **Order Management:** Administrators can manage and process orders, including order status updates and tracking information.
- **Admin Dashboard:** A comprehensive admin dashboard provides administrators with full control over the application, including managing products, orders, users, and more.
- **Responsive Design:** The application is built with a responsive design to ensure a seamless experience across different devices.


## Installation

Follow these steps to set up the Django E-Commerce web application on your local machine:

- Clone the repository:
```bash
  git clone https://github.com/shashank026/zenatix-assignment.git
```
- Navigate to the project directory:
```bash
  cd zenatix-assignment
```
- Install the required dependencies:
```bash
  pip install -r requirements.txt
```
- Start the development server:
```bash
  python3 manage.py runserver
```
- Access the application in your web browser at `http://localhost:8000`
## Docker Deployment

To deploy the Django E-Commerce web application using [Docker](https://docs.docker.com/engine/install/), make sure you have Docker Compose installed and follow these steps:

- Build the Docker image:
```bash
  docker build -t zenatix_assignment .
```
- Run the Docker container:
```bash
  docker run -p 8000:8000 zenatix_assignment
```
- Access the application in your web browser at `http://localhost:8000`

**To stop the application running from docker, do run the following commands:**
```bash
  docker ps
```
- Output of tha above command is:
```bash
CONTAINER ID   IMAGE                 COMMAND                  CREATED       STATUS       PORTS                    NAMES
a3870a20f781v   django-docker:0.0.1   "python manage.py ru…"   1 minutes ago   Up 1 minutes   0.0.0.0:8000->8000/tcp   zenatix_assignment-django-1
```
- Copy the **CONTAINER ID** from the above output, and run the command:
```bash
docker stop <CONTAINER ID>
```

## Docker Compose

To deploy the Django E-Commerce web application using [Docker Compose](https://docs.docker.com/compose/), make sure you have Docker installed and follow these steps:

- Build the Docker Compose
```bash
  docker-compose up -d --build
```
- Access the application in your web browser at `http://localhost:8000`
To stop the application running from docker, do run the following commands:
```bash
docker-compose down
```

## Admin Dashboard Access

The admin dashboard provides administrative access to manage various aspects of the Django E-Commerce web application. With the admin dashboard, the admin can perform the following actions:

- Change the image, price, quantity and name of a product.
- Modify the status of an order.
- Block or unblock user accounts.

To access the admin dashboard, follow these steps:

- Open your web browser and navigate to the admin login page: `/accounts/admin-login`
- Enter the following demo admin account credentials:
   - Username: `admin@admin.com`
   - Password: `admin123`
- Click the __"Login"__ button to log in.

Once logged in, you will have access to the admin dashboard and its features.

__Please note that the provided demo admin account is for testing purposes only. In a production environment, it is essential to create a secure and unique admin account with a strong password.__

![](https://github.com/shashank026/zenatix-assignment/blob/main/readmeImage/Admin-Dashboard-main.png)

![](https://github.com/shashank026/zenatix-assignment/blob/main/readmeImage/Admin-Dashboard-OrderHistory-Dark.png)
