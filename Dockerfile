FROM registry.gitlab.com/janw/python-poetry:3.7-alpine as requirements

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src
COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt

FROM python:3.7
RUN apt-get update && apt-get install -y youtube-dl ffmpeg && apt-get clean

WORKDIR /app
COPY --from=requirements /src/requirements.txt ./
COPY defaults.toml ./
COPY stream_vcr ./stream_vcr

VOLUME [ "/config" ]

ENV IN_DOCKER 1

ENTRYPOINT [ "python" ]
CMD [ "-m", "stream_vcr" ]
