FROM python:3.11-slim
ARG VERSION

LABEL maintainer="Zauberzeug GmbH <info@zauberzeug.com>"

RUN python -m pip install nicegui==$VERSION

WORKDIR /app

COPY main.py reference.py README.md ./ 
ADD examples ./examples

EXPOSE 8080

CMD python3 main.py
