# CrossPath Backend

This repository is dedicated to the backend of the CrossPath application. It uses FastAPI, Docker, and MongoAtlas to provide a robust and scalable API.

## Features

- **FastAPI**: Leverages the power of FastAPI for building robust and high-performance APIs.
- **Docker**: Containerizes the application for easy deployment and scalability.
- **MongoAtlas**: Utilizes MongoAtlas for a scalable and flexible NoSQL database solution.
- **Python 3.6+**: Utilizes the latest features of Python for better performance and readability.
- **Asynchronous**: Supports asynchronous programming for handling multiple requests efficiently.

## Getting Started

To start the API, ensure you have Docker installed and run the following command:

```sh
docker-compose up --build
```

### How to Upload New Code

Clone the repository locally:
```sh
git clone https://github.com/alejandrorecarte/BE_WASP
```

Create a new branch:
```sh
git checkout -b <branch-name>
```

Type the new amazing code you want to upload and run:
```sh
pre-commit run --all-files
```

Then commit and push your changes. **NEVER PUSH YOUR CODE TO MAIN OR DEVELOP DIRECTLY**:
```sh
git commit -m "your commit message"
git push origin <branch-name>
```

Finally, create a new Pull Request on GitHub and wait for it to be approved.
