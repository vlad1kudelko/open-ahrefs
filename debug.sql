SELECT * FROM urls;
SELECT * FROM responses;
SELECT * FROM links;

SELECT * FROM
(SELECT COUNT(*) as urls FROM urls) CROSS JOIN
(SELECT COUNT(*) as resp FROM responses) CROSS JOIN
(SELECT COUNT(*) as links FROM links);

SELECT domain, path, COUNT(*) as c
FROM urls JOIN links on urls.url_id = links.target_url_id
GROUP BY domain, path
ORDER BY c DESC;

--UPDATE urls SET last_pars = NULL WHERE scheme = 'https';

SELECT domain, COUNT(*) FROM urls GROUP BY domain ORDER BY count DESC;

CREATE INDEX ix_url_full_address 
ON urls (scheme, domain, port, path, param, anchor);
