# Drafty Backend Server

Welcome to Drafty! This is the README file for the backend server of the Drafty project, a to-do list application. This server is built using Python FastAPI, SQLAlchemy, and FormEncode.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Drafty is a to-do list application that helps you manage your tasks efficiently. The backend server is responsible for handling client requests, managing user authentication, and persisting task data in a database.

## Features

- User registration and authentication using token-based systems (JWT/OAuth)
- Create, read, update, and delete tasks
- Mark tasks as complete or incomplete
- Filter and sort tasks based on different criteria
- Pagination support for retrieving tasks
- User account management

## Technologies Used

- Python FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- SQLAlchemy: A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- FormEncode: A form validation and conversion library for Python that provides flexible data conversion, input validation, and more.
- JWT (JSON Web Tokens): A compact, URL-safe means of representing claims to be transferred between two parties.
- OAuth: A protocol that allows websites or applications to authenticate users via third-party service providers.

## Getting Started

Follow the instructions below to get started with the Drafty backend server.

### Prerequisites

- Python 3.7 or above installed on your system
- pip package manager



### Installation

1. Clone the repository:

```
git clone https://github.com/MuhammadTaneem/To-do-list.git
```

2. Change to the project directory:

```
cd To-do-list/server
```

3. Create and activate a virtual environment (optional but recommended):

```
python3 -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:

```
pip install -r requirements.txt
```
5. Configure the PostgreSQL database:
   - Ensure that PostgreSQL is installed on your system.
   - Create a database named "drafty" using the following command:
     ```bash
     createdb drafty
     ```
   - Set the database port to 5433:
     ```bash
     psql -c "ALTER SYSTEM SET port = 5433;" -U postgres
     ```
   - Set the password for the default "postgres" user to "123456":
     ```bash
     psql -c "ALTER USER postgres WITH PASSWORD '123456';" -U postgres
     ```


## Usage

To start the Drafty backend server, run the following command:

```
uvicorn main:app --reload
```

The server will start running at `http://localhost:8000`.

## API Documentation

The API documentation for the Drafty backend server is available at `http://localhost:8000/docs` after starting the server. It provides detailed information about the available endpoints, request/response structures, and authentication requirements.

## Contributing

Contributions to the Drafty project are welcome! If you find any bugs, want to add new features, or improve the code, feel free to submit a pull request.

Before making a contribution, please read the CONTRIBUTING.md file for guidelines.

## License

The Drafty backend server is open-source software released under the [MIT License](https://opensource.org/licenses/MIT). You can find more details in the LICENSE file.