# Dockerfile for the container holding CSV data
FROM alpine:latest
COPY titanic.csv /data/titanic.csv
