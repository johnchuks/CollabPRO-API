#set up python runtime environment
FROM  python:3.6.2
ENV PYTHONUNBUFFERED 1

# setup the working directory to /collabpro
WORKDIR /collapro

# Add the current directory to the /collabpro directory
ADD . /collabpro

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#
