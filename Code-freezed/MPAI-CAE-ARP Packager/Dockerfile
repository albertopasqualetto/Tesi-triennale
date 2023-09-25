FROM matteospanio/poetry:latest

LABEL maintainer="Matteo Spanio"

WORKDIR /app

COPY . ./

RUN poetry install --no-cache --only main

VOLUME [ "/data" ]

CMD ["poetry", "run", "python", "src/packager/server.py"]