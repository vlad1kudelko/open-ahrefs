SELECT * FROM urls;
SELECT * FROM responses;
SELECT * FROM links;

SELECT COUNT(*) FROM urls;
SELECT COUNT(*) FROM responses;
SELECT COUNT(*) FROM links;

SELECT domain, path, COUNT(*) as c
FROM urls JOIN links on urls.url_id = links.target_url_id
GROUP BY domain, path
ORDER BY c DESC;

UPDATE urls SET last_pars = NULL WHERE scheme = 'https';
