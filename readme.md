
# Django E-Commerce web application

This Django E-Commerce web application is a fully functional and customizable online store platform. It provides a robust foundation for building and managing an e-commerce website, allowing you to sell products or services online with ease.




## Features

- **User Registration and Authentication:** Users can create accounts, log in, and manage their profiles.
- **Product Catalog:** Display and categorize your products with detailed information such as title, description, price, and images.
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
  python manage.py runserver
```
- Access the application in your web browser at `http://localhost:8000`
## Docker Deployment

To deploy the Django E-Commerce web application using [Docker](https://docs.docker.com/engine/install/), make sure you have Docker installed and follow these steps:

- Build the Docker image:
```bash
  docker build -t zenatix_assignment .
```
- Run the Docker container:
```bash
  docker run -p 8000:8000 zenatix_assignment
```
- Access the application in your web browser at `http://localhost:8000`

To stop the application running from docker, do run the following commands:
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