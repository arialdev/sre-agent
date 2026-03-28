# Runbook: Database Connection Refused

## Severity
P1 - Critical

## Symptoms
- Application logs show `ECONNREFUSED` or `Connection refused` errors targeting the database host/port.
- Health check endpoints return 503 Service Unavailable.
- Dependent microservices begin cascading failures due to missing data layer.
- Monitoring dashboards show zero active database connections.

## Diagnosis Steps
1. Verify the database process is running: `systemctl status postgresql` or `docker ps | grep postgres`.
2. Check if the database port (default 5432) is listening: `ss -tlnp | grep 5432`.
3. Verify network connectivity from the application host: `telnet db-host 5432`.
4. Check database max_connections vs current connections: `SELECT count(*) FROM pg_stat_activity;`.
5. Review database logs for OOM kills or crash recovery: `journalctl -u postgresql --since "1 hour ago"`.
6. Check firewall or security group rules between application and database subnets.
7. Verify DNS resolution of the database hostname: `dig db-host`.

## Resolution Steps
1. If the database process is down, restart it: `systemctl restart postgresql`.
2. If max_connections is exhausted, identify and terminate idle connections: `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND query_start < now() - interval '10 minutes';`.
3. If firewall rules changed, revert the security group or iptables change.
4. If disk is full, free space and restart: check with `df -h /var/lib/postgresql`.
5. If the instance was OOM-killed, increase memory or tune `shared_buffers` and `work_mem`.
6. Verify recovery by checking application logs for successful connections.

## Prevention / Monitoring
- Alert on `pg_stat_activity` connection count exceeding 80% of `max_connections`.
- Set up synthetic health checks that test actual database connectivity, not just TCP port availability.
- Use connection pooling (PgBouncer) to prevent connection exhaustion.
- Monitor disk usage on the database volume with a 75% threshold alert.
- Maintain a runbook link in the PagerDuty service configuration for fast access during incidents.
