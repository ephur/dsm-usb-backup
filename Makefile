.PHONY: default

ifeq ($(VERSION),)
VERSION := $(shell git describe --all --dirty | cut -d / -f2,3,4)
endif

default: docker-build

docker-build:
	docker build -t ephur/dsmusbbackup:latest .

docker-push:
	docker tag ephur/dsmusbbackup:latest ephur/dsmusbbackup:$(VERSION)
	docker push ephur/dsmusbbackup:$(VERSION)
	docker push ephur/dsmusbbackup:latest
