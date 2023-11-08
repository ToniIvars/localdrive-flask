# Localdrive

Clone of cloud storages like Google Drive or OneDrive made with Flask.

## Installation

First of all, you will have to clone the repository: `git clone https://github.com/ToniIvars/localdrive-flask.git`

### Docker (recommended)

This is the recommended way of installing Localdrive because of its ease and its resistance to human errors. A docker-compose file is provided, and you will only need to update the volumes paths and the `LOCALDRIVE_SECRET_KEY` environment variable:

```yml
services:
  localdrive:
    build: .
    container_name: localdrive-docker
    volumes:
      - /path/to/storage:/storage
      - /path/to/instance:/localdrive/instance
    ports:
      - 80:5000
    environment:
      - LOCALDRIVE_SECRET_KEY=db8081c8aa7790949026ebb004d04efb
      - LOCALDRIVE_SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite
      - LOCALDRIVE_STORAGE_PATH=/storage
    restart: unless-stopped
```

### Python

In order to use localdrive with your system's python, you will have to install the required modules like that:

```bash
pip install -r requirements.txt
```

Then, it is recommended to create a `.env` file in the `drive` directory with the following environment variables (even thouh you could also define the in the environment before you serve the application):

```bash
LOCALDRIVE_SECRET_KEY='override'
LOCALDRIVE_SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite
LOCALDRIVE_STORAGE_PATH='full path to the storage path'
```

After this setup, to run the application (using Gunicorn), you must run the following command in the `localdrive` directory (replacing **ip** and **port** by the wanted):

```bash
gunicorn drive:create_app() -b 'ip:port'
```