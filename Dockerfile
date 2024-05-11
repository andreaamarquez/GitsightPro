FROM debian:bullseye

# RUN apt-get update && apt-get install -y nodejs npm node-libnpx

# Install postgresql and psql client
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y python3.9-venv
RUN pip install jose

# EXPOSE 3000

# RUN /bin/bash -c "python3 -m venv /venv && source /venv/bin/activate && pip install psycopg2==2.9.5 pydantic==1.7.3 uvicorn==0.12.3 databases==0.8.0 fastapi==0.62.0 SQLAlchemy==1.4.49 httpx aiofiles jinja2==3.0.3 python-multipart==0.0.6 requests pandas"
RUN /bin/bash -c "python3 -m venv /venv && source /venv/bin/activate && pip install psycopg2-binary==2.9.5 pydantic==1.7.3 uvicorn==0.12.3 databases==0.8.0 fastapi==0.62.0 SQLAlchemy==1.4.49 httpx aiofiles jinja2==3.0.3 python-multipart==0.0.6 requests pandas"

# Set environment variables for PostgreSQL connection

RUN /etc/init.d/postgresql start && \
    su -c "psql --command=\"ALTER USER postgres PASSWORD '1234';\"" -s /bin/bash postgres && \
    su -c "createdb datamining_db;" -s /bin/bash postgres && \
    su -c "psql --dbname=datamining_db --command=\"CREATE SCHEMA IF NOT EXISTS PUBLIC;\"" -s /bin/bash postgres && \
    /etc/init.d/postgresql stop

ENV PGHOST=localhost
ENV PGPORT=5432
ENV PGUSER=postgres
ENV PGPASSWORD=1234

ENV PORT 8000
# # set hostname to localhost
# ENV HOSTNAME "0.0.0.0"

# CMD ["node"]
CMD ["sh", "-c", "while true; do sleep 3600; done"]

