# Handyman Services Application (HSA)
Authors:

- Alex Guo
- Tan Nguyen
- Stewart Sankey
- Mike Zeng

This application was built as part of the course **[CS:5830:0001 Software Engineering Project](https://myui.uiowa.edu/my-ui/courses/details.page?ci=150179&id=1030268)** taken during the Spring 2025 semester at The University of Iowa.

The original repository can be found ![here](https://github.com/uiowaSEP2025/sep2025-project-team_003).

## Introduction

The Handyman Services Application (HSA) is a web-based, field-service app designed to assist handyman businesses. The app is an all-in-one solution for a handyman to manage everyday tasks such as customer management, job tracking, invoicing, and bookings.

## Background

A handyman is a person who provides maintenance or "fix-me-up" type of work for households. Typical services include work such as cleaning gutters, window washing, pressure washing, painting, furniture assembly, lighting, and remodeling. While they are typically a generalist, some may have additional expertise in areas such as HVAC, landscaping, electrical, and plumbing.

## Problem Statement

A [recent study](https://www.salesforce.com/news/stories/small-business-productivity-trends-2024/) by Slack found that small business owners are losing on average 96 minutes per day in productivity from context switching between different apps for managing their business. This amounts to over 3 work weeks of loss productivity annually. Handyman businesses are no exception to this.

An independent handyman business can have a lot of overhead in their day-to-day operations. To run their business, a handyman needs to be able to track their customers, jobs, materials, and other costs. They also need to manage their schedules, generate quotes, dispatch subcontractors, track invoices, and many other tasks. As their business grows, the time spent having to manage overhead grows with it.

## Application Overview

The Handyman Services App consists of 6 primary features and a secondary customer-facing feature. HSA is organized into three primary systems: The CRM system, the Jobs system, and the Bookings system.

### Key Features

#### Primary Features

- **Customer Relations Manager (CRM)**: Manage customer information and interactions
- **Invoicing**: Generate and track invoices for completed jobs
- **Quotes**: Create and send quotes to potential customers
- **Bookings**: Schedule and manage appointments
- **Dispatching**: Assign jobs to team members or subcontractors
- **Jobs, services, and materials management**: Track job details, services provided, and materials used

## Technical Stack

The Handyman Services Application is built using the following technologies:

- **Frontend**: Angular 19 with Angular Material and Tailwind CSS
- **Backend**: Django 5 with Django REST Framework
- **Database**: PostgreSQL
- **Deployment**: Docker and Kubernetes support

## Installation Instructions

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.10 or higher)
- PostgreSQL (v14 or higher)
- Docker (optional, for containerized deployment)

### Frontend Setup (Angular)

1. Navigate to the frontend directory:
   ```bash
   cd HSA-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The application will be available at http://localhost:4200

### Backend Setup (Django)

1. Navigate to the backend directory:
   ```bash
   cd HSA-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database
   - Configure the database connection in your environment variables:
     ```
     DATABASE_NAME=your_db_name
     DATABASE_IP=localhost
     DATABASE_USERNAME=your_db_user
     DATABASE_PASSWORD=your_db_password
     ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```
   The API will be available at http://localhost:8000

### Docker Deployment

The application can also be deployed using Docker:

1. Build the Docker image:
   ```bash
   ./environment.sh build
   ```

2. Set the required environment variables:
   ```bash
   export DATABASE_NAME=your_db_name
   export DATABASE_IP=your_db_host
   export DATABASE_USERNAME=your_db_user
   export DATABASE_PASSWORD=your_db_password
   ```

3. Run the Docker container:
   ```bash
   ./environment.sh run
   ```
   The application will be available at http://localhost:8000

## Contributing

Please see [Contributing.md](Contributing.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the terms of the LICENSE file included in the repository.
