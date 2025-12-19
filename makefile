stop_admin:
	docker compose -f docker-compose.admin.yml down

start_admin:
	docker compose -f docker-compose.admin.yml up --build -d

logs_admin:
	docker compose -f docker-compose.admin.yml logs -f

restart_admin: stop_admin start_admin logs_admin

#--------------------------------------------------------------------

stop_grafana:
	docker compose -f docker-compose.grafana.yml down

start_grafana:
	docker compose -f docker-compose.grafana.yml up --build -d

logs_grafana:
	docker compose -f docker-compose.grafana.yml logs -f

restart_grafana: stop_grafana start_grafana logs_grafana

#--------------------------------------------------------------------

stop_scraper:
	docker compose -f docker-compose.scraper.yml down

start_scraper:
	docker compose -f docker-compose.scraper.yml up --build -d

logs_scraper:
	docker compose -f docker-compose.scraper.yml logs -f

restart_scraper: stop_scraper start_scraper logs_scraper
