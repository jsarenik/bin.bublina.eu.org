FROM gitpod/workspace-full

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/

# Install custom tools, runtime, etc.
RUN sudo apt-get update && sudo apt-get install -y busybox && sudo rm -rf /var/lib/apt/lists/*
RUN sudo mkdir /busybox
RUN sudo /bin/busybox --install /busybox
