FROM python:3.7-alpine as base

# Build the app
FROM base as build
RUN mkdir -p /install/lib/python3.7/site-packages/ /build-temp
COPY . /build-temp
WORKDIR /build-temp
RUN PYTHONPATH=/install/lib/python3.7/site-packages/ python setup.py install --prefix=/install

# Copy files from build container into place
FROM base
RUN apk add --update \
  rsync \
  && rm -rf /var/cache/apk/*
COPY --from=build /install /usr/local

CMD ["dsmusbbackup"]
