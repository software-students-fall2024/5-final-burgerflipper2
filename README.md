# BookKeeper README

[MongoDB CI/CD](https://github.com/software-students-fall2024/5-final-burgerflipper2/actions/workflows/mongodb-workflow.yml)

[Webapp CI/CD](https://github.com/software-students-fall2024/5-final-burgerflipper2/actions/workflows/webapp-workflow.yml)

# Project Description

BookKeeper is a book-matching service that tracks users’ inventory and wishlists, and offers potential matches and exchanges, allowing users to circulate books between each other.

# Links to DockerHub Images

1. MongoDB
2. Webapp

# Prerequisites

- Python 3.x
- Git
- Docker, Docker Compose

# Configuration Instructions

Please create a .env file located in the root directory with two values, MONGO_URI and DB_NAME.

```
MONGO_URI=mongodb://localhost:27017/bookkeeping
DB_NAME=bookkeeping
```

# Running the Project

## To run

1. First, clone the repository from GitHub on your terminal and navigate to the directory.
    
    ```markdown
    git clone https://github.com/software-students-fall2024/5-final-burgerflipper2.git
    cd 5-final-burgerflipper2
    ```
    
2. Create a .env file in the root directory.

```markdown
MONGO_URI=mongodb://localhost:27017/bookkeeping
DB_NAME=bookkeeping
```

1. Build and start the containers.

```markdown
docker-compose up --build
```

1. Access the application.
    1. Web application: http://localhost:3000
    MongoDB: localhost:27017
2. Use the following default account information to log in.
    1. Email: maddy@example.com
    Password: password123
    
    2. Email: john@example.com
    Password: password123
3. To stop the containers:

```markdown
docker-compose down
```

## Testing

```markdown
# Webapp tests
pytest test/test_webapp.py --cov=app

# Mongodb tests
pytest test/test_mongodb.py --cov=mongodb
```

# Contributors

[Julie Chen](https://github.com/Julie-Chen)

[Christopher Li](https://github.com/christopherlii)

[Maddy Li](https://github.com/maddy-li)

[Aneri Shah](https://github.com/anerivs)