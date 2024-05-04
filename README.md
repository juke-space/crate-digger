# Overview
The Music Data Collator is a CLI for retrieving music data from multiple open APIs, collating that data, and writing it to a given directory or database.
# Getting Started
This project uses [PDM](https://pdm-project.org/latest/) to manage dependencies and entry points.
## Installing and Using PDM
Follow the directions [here](https://pdm-project.org/latest/) to install PDM on your machine if you have not done so.

Run `pdm sync` within the repository directory to download all dependencies.

## Testing
To run the test suite, execute the following command:
```
pdm run pytest
```

## Deploying
Build the docker image with:
```
docker build -t crate_digger .
```

Run a container with the image:
```
docker run crate_digger
```

Run a container with the image interactively (ideal for debugging):
```
docker run -it crate_digger
```
