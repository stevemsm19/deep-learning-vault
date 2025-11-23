# Deep Learning Vault

The required _Python_ version for this project is _3.12.x._

## About me

Hello, my name is *Oscar*, I am 26 years old, and I am from Bogotá, Colombia. My experience in the world of software development is what I acquired during my time at university. This degree has been quite challenging for me because I also work at Airbnb in customer service, which is why I speak Portuguese and have an intermediate level of English. The reason I chose this career is because I love automating processes and really enjoy analyzing data on a small scale. I'm not the best at math, but I believe that with practice and study, anything is possible.

    ## Setup environment

As usual setup your virtual environment:

```
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip setuptools
$ pip install -r requirements-dev.txt
$ pip install -e .
```

> Or you can use `make setup` if you have a Linux environment and then `source venv/bin/activate` to activate the virtual environment.

## Basic code compliance

```
$ black .
All done! ✨ 🍰 ✨
X files left unchanged.
$ mypy .
Success: no issues found in X source files
```

## About the CI/CD pipeline

This `monorepo` comes with a pre-configured CI/CD pipeline that is triggered every time a push is made to a **merge request** or when a **merge request** is integrated into the **main** branch.

The pipeline is configured to:

- Execute **code compliance** checks.
- Generate documentation.

> You may add more stages or jobs to the pipeline, but make sure you **do not remove the existing ones**. In addition, make sure you do your best to **keep the pipeline green** at all times.

## Running the App

Before starting the project, remember to complete the **Setup environment** step if you are going to run the application locally.

### Running the Backend

Currently, you can start the backend directly from the terminal, below are the recommended commands depending on your environment.

#### Running Locally

**Windows**

Run the backend using Uvicorn:

```bash
uvicorn src.app.backend.main:app
```

**Linux**

Use the provided Makefile:

```bash
make run-backend
```

Once the backend is running, you can access it at:
- **Backend Server:** [http://localhost:8000](http://localhost:8000)

### API Documentation

The backend includes automatic interactive documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

These pages allow you to explore all available endpoints, payloads, and responses.