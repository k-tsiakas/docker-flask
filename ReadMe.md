# Simple Dockerized Flask app
This is a simple flask application deployed in docker container which displays
host and client ip
```bash
# create the python/flask image
sh docker-images/create_flask_image.sh
# run with
docker-compose up --build --remove-orphans
# terminate with
docker-compose down
```
#### Step 1: Create a docker bridge network with name main_network

#### Step 2: Create a python-alpine image with flask installed
- open docker-images dir and build the image by running the script

#### Step 3: Run flask application
- build and run the flask application with docker-compose
