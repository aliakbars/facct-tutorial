# WEIRD Platform

Welcome to WEIRD Platform! This is a web application to annotate papers to measure the WEIRDness of a paper/conference/journal. To get started, follow the instructions below.

## Installation

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/aliakbars/facct-tutorial.git
```

Install Poetry, a dependency manager for Python:
```bash
pip install poetry
```

Alternatively, you can install Poetry from git:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Navigate to the project directory and use Poetry to install the required dependencies:
```bash
poetry install
```

## Configuration

> [!NOTE]
> Before running the app, you may need to adjust some settings in the `config.yml` file. This file is located in the root directory and contains configuration settings for the app. Check the file and adjust any settings as necessary. By default, this app is configured for collecting data with [Prolific](https://www.prolific.co/), but you can change the `redirect_url` if needed.

## Usage

To run the app, use Uvicorn, a lightning-fast ASGI server for Python:
```bash
poetry run uvicorn main:app --reload
```

This will start the app on `http://localhost:8000/`, but you may see a landing page saying that there are no papers to annotate at this stage.

To add papers to your database, run:
```bash
poetry run python utils.py add-papers
```
after changing the `papers_file` argument in the `config.yml` file.

Rerun the app again and go to `http://localhost:8000/?PROLIFIC_PID=1&SESSION_ID=1&STUDY_ID=1` to test the app. You should see the page to annotate a set of 5 papers.

## Putting Into Production

1. Install `supervisor` on your machine, e.g.
```bash
sudo apt install supervisor
```
1. Identify your virtual environment folder by running:
```bash
poetry shell
```
1. Change the `DIR` path to the directory of your app and change the `VENV` path to the virtual environment you got from the previous step.
1. Update the `configs/weird.conf` file by changing the path for `command` and `stdout_logfile`, ensuring the correct absolute path, i.e. not using `~/`.
1. Update the `configs/wlock.conf` file by changing the path for `command` to the Python path in your virtual environment (changing the `.../activate` you got from step 2 to `.../python`)
1. Copy the `configs/weird.conf` and `configs/wlock.conf` files to `/etc/supervisor/conf.d`. You need `sudo` access for this.
1. Restart `supervisor`, e.g. `sudo service supervisor restart`.
1. Setup NGINX by following the steps described in this [blog post](https://dylancastillo.co/fastapi-nginx-gunicorn/#step-5-configure-nginx). Make sure you change the paths to your app.

The `weird.conf` file is for the main app, whereas the `wlock.conf` file is for releasing the locks of the papers to avoid double entries. Make sure you only set 1 worker to avoid multiple submissions for the same set of papers.

## Contributing

If you'd like to contribute to WEIRD Platform, fork the repository and make your changes. Then, create a pull request to merge your changes back into the main branch.

## License

WEIRD Platform is licensed under the MIT License.