stop_admin:
	docker compose -f docker-compose.admin.yml down

start_admin:
	docker compose -f docker-compose.admin.yml up --build -d

logs_admin:
	docker compose -f docker-compose.admin.yml logs -f

restart_admin: stop_admin start_admin logs_admin
