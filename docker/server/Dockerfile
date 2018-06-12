#set up python runtime environment
FROM  python:3.6.2-slim
ENV PYTHONUNBUFFERED 1

#upgrade pip version
RUN pip install --upgrade pip

# setup the working directory to /collabpro
WORKDIR /collabpro

# Add the current directory to the /collabpro directory
COPY . /collabpro

#Add requirements.txt to the collapro directory

COPY requirements.txt /tmp

# Install any needed packages specified in requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./start.sh /start.sh
COPY ./setup.sh /setup.sh

RUN chmod +x /setup.sh
RUN chmod +x /start.sh

# Expose the port out of the container
EXPOSE 9000

#set entrypoint for the container
ENTRYPOINT "/setup.sh" && /bin/bash

