TAG ?= python3
DOCKER_REGISTRY := dineshkarthik
DOCKER_REPOSITORY :=  ${DOCKER_REGISTRY}/whatsapp-analyzer
TEST_ARTIFACTS ?= /tmp/coverage


.PHONY: requirements deps install build push docker_hub_login run

requirements:
	pip3 install --upgrade pip setuptools
	pip3 install -r requirements.txt

install: requirements
	pip3 install -e .

deps: install
	pip3 install -r dev-requirements.txt

run:
	wapp-analyzer run

build:
	docker build -t ${DOCKER_REPOSITORY}:${TAG} .

docker_hub_login:
	docker login -u ${DOCKER_HUB_USER} -p ${DOCKER_HUB_PASSWORD}

push:
	docker push ${DOCKER_REPOSITORY}:${TAG}

test: deps
	py.test --cov wapp --doctest-modules \
		--cov-report term-missing \
		--cov-report html:${TEST_ARTIFACTS} \
		--junit-xml=${TEST_ARTIFACTS}/whatsapp-analyzer.xml \
		tests/ wapp/