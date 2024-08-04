# Run the Project

## Project Setup
The project is dockerized so just need to build and run the docker container, it will take care of all the DB setup and such.

(Optional) Install Docker Desktop for easy GUI on windows. Clone the project and open a terminal.
```bash
$ docker-compose up --build
```
This will build the container and once completed, the container will be running and visible in the container section of the Docker Desktop.
Even if the terminal is closed, the container can be started/stopped from the GUI.

This container will run all the resources (redis, celery, etc) for the project.
<br>We can now access the server at http://localhost:8000/.

### Database Setup
**This step is only if not using Docker, the DB is already setup through the Dockerfile.**

To build the database tables, we need to run the migrate command.
- In the terminal run
```
$ python manage.py migrate
```
### Superuser/Admin Setup
We need to run the `createsuperuser` command to create a admin/super user.
- In the integrated terminal of `web` container or the terminal of your window in case not using docker.
```
$ python manage.py createsuperuser
```
- You can also run the migrate command from the terminal of docker build in the following way
```
$ docker-compose up -d
docker-compose exec web python manage.py createsuperuser
```

- Or access the bash of the container using the container id, like
```bash
$ docker exec -it {{container_id}} bash
```

- In the terminal type the `createsuperuser` command.

We can now access the admin panel of our project at [http://localhost:8000/admin/](http://localhost:8000/admin/) with the credentials provided while executing the `createsuperuser` command.

### Running the Project

- Our project can be run using the docker container and accessing the server.
- In other case, access it by typing:
```bash
$ python manage.py runserver
```

The project is now running at http://localhost:8000 and the endpoints can be accessed now.

**For the Endpoints User, please check - [API Endpoints](Endpoints.md)**