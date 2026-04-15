setup:
	python3 scripts/prepare-local.py

dev: setup
	docker compose up -d
	@echo "Dashboard available at http://localhost:3000"

clean:
	docker compose down
	rm -rf local-dev/config/*.yaml
	rm -rf local-dev/config/*.css
	rm -rf local-dev/config/*.js

.PHONY: setup dev clean
