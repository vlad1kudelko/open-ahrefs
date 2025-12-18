SELECT * FROM urls;
SELECT * FROM responses;
SELECT * FROM links;

SELECT * FROM urls WHERE url_id = 58606;
SELECT * FROM responses WHERE url_id = 60024;
SELECT * FROM links WHERE source_url_id = 58606;

-- общая статистика по таблицам
SELECT * FROM
(SELECT COUNT(*) as urls FROM urls) CROSS JOIN
(SELECT COUNT(*) as resp FROM responses) CROSS JOIN
(SELECT COUNT(*) as links FROM links);
--

-- рейтинг ссылок по количеству входящих
SELECT domain, path, COUNT(*) FROM urls JOIN links on urls.url_id = links.target_url_id
WHERE domain not in ('github.com')
GROUP BY domain, path
ORDER BY count DESC;
--

-- все домены (и количество ссылок с ними)
SELECT domain, COUNT(*) FROM urls
GROUP BY domain
ORDER BY count DESC;
--

-- недоступные домены с количеством запросов к ним
SELECT domain, COUNT(*) FROM urls JOIN responses USING(url_id)
WHERE status_code = 999
GROUP BY domain
ORDER BY count DESC;
--

-- количество ссылок, которые отправлены в kafka, но еще не спаршены
SELECT COUNT(*) FROM urls LEFT JOIN responses USING(url_id)
WHERE urls.last_pars IS NOT NULL AND responses.url_id IS NULL;
--
