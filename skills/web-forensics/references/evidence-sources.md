# Web evidence sources

## Configuration

Common sources include reverse-proxy and server configuration, application `.env`
files, framework settings, deployment manifests, container metadata, and secret
references. A configured upstream, route, or feature flag is not proof that it was
used; corroborate it with logs or deployment evidence when the claim requires it.

## Logs

Record the source path, collection interval, time zone, log format, and parser limit.
Reverse proxies can change client-address semantics, so use forwarded headers only
when the proxy configuration establishes their meaning.

## Correlation

Use stable joins such as a request ID, timestamp plus URI, virtual host, container ID,
or release identifier. Do not equate a nearby configuration value with a request,
account, or external exposure without a supporting join.
