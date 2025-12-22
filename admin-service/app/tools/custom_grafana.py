from prometheus_client import Counter

metrics_counter = Counter(
    "app_admin_service_counter",
    "Количество взаимодействий с kafka",
    ["group", "status"],
)
