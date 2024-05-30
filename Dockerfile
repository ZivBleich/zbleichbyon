FROM ubuntu:20.04
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    python3-pip

# Mongo
RUN apt-get install -y mongodb
# Create the MongoDB data directory
RUN mkdir -p /data/db
EXPOSE 27017

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH "${PYTHONPATH}:/code/app"
ENTRYPOINT ["/entrypoint.sh"]
