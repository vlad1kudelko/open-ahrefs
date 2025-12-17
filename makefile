stop_admin:
	docker compose -f docker-compose.admin.yml down

start_admin:
	docker compose -f docker-compose.admin.yml up --build -d

logs_admin:
	docker compose -f docker-compose.admin.yml logs -f

restart_admin: stop_admin start_admin logs_admin

stop_scraper:
	docker compose -f docker-compose.scraper.yml down

start_scraper:
	docker compose -f docker-compose.scraper.yml up --build -d

logs_scraper:
	docker compose -f docker-compose.scraper.yml logs -f

restart_scraper: stop_scraper start_scraper logs_scraper
