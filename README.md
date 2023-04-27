# WEIRD Platform

Welcome to WEIRD Platform! This is a web application to annotate papers to measure the WEIRDness of a paper/conference/journal. To get started, follow the instructions below.

## Installation

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/aliakbars/facct-tutorial.git
```

Install Poetry, a dependency manager for Python:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Alternatively, you can install Poetry using pip:
```bash
pip install poetry
```

Navigate to the project directory and use Poetry to install the required dependencies:
```bash
poetry install
```

## Configuration

Before running the app, you may need to adjust some settings in the `config.yml` file. This file is located in the root directory and contains configuration settings for the app. Check the file and adjust any settings as necessary. By default, this app is configured for collecting data with [Prolific](https://www.prolific.co/), but you can change the `redirect_url` if needed.

## Usage

To run the app, use Uvicorn, a lightning-fast ASGI server for Python:
```bash
poetry run uvicorn main:app --reload
```

This will start the app on `http://localhost:8000/`. Navigate to this URL in your web browser to see the app in action!

To add papers to your database, run:
```bash
poetry run python utils.py add-papers
```
after changing the `papers_file` argument in the `config.yml` file.

## Contributing

If you'd like to contribute to WEIRD Platform, fork the repository and make your changes. Then, create a pull request to merge your changes back into the main branch.

## License

WEIRD Platform is licensed under the MIT License.