#set up python runtime environment
FROM  python:3.6.2-slim
ENV PYTHONUNBUFFERED 1

# Run apt for new debian source
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

# Install native dependencies
RUN apt-get update -qq && apt-get install -y -qq \
    git \
    gdal-bin \
    libgdal1-dev \
    libgeos-dev
#upgrade pip version
RUN pip install --upgrade pip

# setup the working directory to /collabpro
WORKDIR /collabpro

# copy dependencies to new working directory
COPY /requirements.txt /collabpro

# Install any needed packages specified in requirements.txt
RUN pip install -r /collabpro/requirements.txt

# Add the current directory to the /collabpro directory
COPY . /collabpro


COPY ./docker/server/start.sh /start.sh
COPY ./docker/server/setup.sh /setup.sh

RUN chmod +x /setup.sh
RUN chmod +x /start.sh

#set entrypoint for the container
ENTRYPOINT "/setup.sh" && /bin/bash
