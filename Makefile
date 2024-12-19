install: .env
	poetry install
.PHONY: install

services-up:
	docker compose up -d --build=true

services-down:
	docker compose down --remove-orphans

serve: install
	poetry run serve
.PHONY: serve

curl:
	while [ true ]; do curl http://0.0.0.0:8080/; sleep 0.01; done;
.PHONY: curl

.env: .env.sample
	cp .env.sample .env
