# Overview
The Music Data Collator is a CLI for retrieving music data from multiple open APIs, collating that data, and writing it to a given directory or database.
# Getting Started
This project uses [PDM](https://pdm-project.org/latest/#installation) to manage dependencies and entry points.
## Installing and Using PDM
Follow the directions [here](https://pdm-project.org/latest/) to install PDM on your machine if you have not done so.

Run `pdm sync` within the repository directory to download all dependencies.

## Running Locally for Development
```
pdm run app
```

## Testing
To run the test suite, execute the following command:
```
pdm run pytest
```

## Building and Running with Docker

### Building the Image
`docker build -t crate_digger .`

### Running the Image
`docker run -p 8000:8000 crate_digger`
