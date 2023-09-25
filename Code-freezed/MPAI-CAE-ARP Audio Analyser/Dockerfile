FROM matteospanio/poetry:latest AS poetry

WORKDIR /app

COPY . ./

RUN apt update && apt install ffmpeg -y

RUN poetry install --no-cache --only main

VOLUME [ "/data" ]

CMD ["poetry", "run", "python", "src/audio_analyzer/server.py"]