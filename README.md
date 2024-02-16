# IEEE RAS TC on Model-based Optimization for Robotics Website

## Installing Dependencies

- `pip install pymdown-extensions==9.9.2`
- `pip install py-markdown-table==0.3.3`
- `pip install mkdocs==1.4.2`
- `pip install mkdocs-material==9.0.9`
- `pip install mkdocs-pymdownx-material-extras==2.4.2`
- `pip install mkdocs-blogging-plugin==2.2.2`

## Quickly Testing Website

- `git clone https://github.com/tcoptrob/tcoptrob.github.io.git`
- `cd tcoptrob.github.io`
- `mkdocs serve`
- Open browser and go to `http://127.0.0.1:8000/`

## Testing through Docker

First **build the image**:

- `cd .ci`
- `docker build -t tcopt .`

Then from the root of the repo:

- `docker run --rm -it --net=host -e DISPLAY -v ${HOME}/.Xauthority:/home/robot/.Xauthority -v "$(pwd)":/home/tcoptrob/src --entrypoint /bin/bash tcopt`
- *Inside the docker container:*
    - `cd src`
    - `mkdocs serve`
- Open browser and go to `http://127.0.0.1:8000/`
