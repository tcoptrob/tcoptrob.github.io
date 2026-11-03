docker run --rm -it --net=host -e DISPLAY -v ${HOME}/.Xauthority:/home/robot/.Xauthority -v "$(pwd)":/home/tcoptrob/src --entrypoint /bin/bash tcopt
