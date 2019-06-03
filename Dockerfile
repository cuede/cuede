# Use an official Postgres runtime as a parent image
FROM postgres:latest

# Expose port used by postgresql
EXPOSE 5432

# Define environment variables
ENV POSTGRES_DB=qed
ENV POSTGRES_USER=qed_user
ENV POSTGRES_PASSWORD="PWD-.,"
ENV PGDATA=/data

