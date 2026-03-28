# Runbook: Redis Cache Eviction Policy

## Severity

P2 - High

## Symptoms

- Redis `evicted_keys` metric is increasing steadily, visible via `INFO stats`.
- Cache hit ratio drops below acceptable thresholds (typically below 90%).
- Application latency increases as more requests fall through to the origin database.
- Redis `used_memory` is at or near the configured `maxmemory` limit.
- Logs show increased database query volume from cache misses.

## Diagnosis Steps

1. Check current memory usage and eviction policy: `redis-cli INFO memory` and `CONFIG GET maxmemory-policy`.
2. Review the eviction policy in use. Common policies:
   - `allkeys-lru`: Evicts least recently used keys across all keys (recommended for caches).
   - `volatile-lru`: Evicts LRU keys only among those with a TTL set.
   - `noeviction`: Returns errors when memory is full (not suitable for caches).
3. Identify large keys consuming disproportionate memory: `redis-cli --bigkeys`.
4. Check if TTLs are set appropriately: `redis-cli DEBUG OBJECT <key>` or sample keys with `SCAN` and `TTL`.
5. Review whether a recent traffic increase or new feature is writing more data to Redis.
6. Check for key namespace bloat: `redis-cli DBSIZE` and compare to historical values.

## Resolution Steps

1. If the eviction policy is `noeviction` or `volatile-lru` for a general cache, switch to `allkeys-lru`: `CONFIG SET maxmemory-policy allkeys-lru`.
2. If memory is genuinely undersized, increase `maxmemory` or scale the Redis instance.
3. If large keys are the issue, refactor application code to use more granular key structures instead of large hashes or lists.
4. If TTLs are missing, add expiration to all cache keys in the application layer: `SET key value EX 3600`.
5. If a specific key namespace is bloated, purge stale entries: `SCAN` + `UNLINK` for the affected prefix.
6. Persist the configuration change: update `redis.conf` or the Helm values so it survives restarts.

## Prevention / Monitoring

- Alert when `evicted_keys` rate exceeds a threshold (e.g., more than 100 evictions per minute).
- Monitor `used_memory` vs `maxmemory` and alert at 85% utilization.
- Track cache hit ratio (`keyspace_hits / (keyspace_hits + keyspace_misses)`) and alert below 90%.
- Enforce TTLs on all cache writes via application-level middleware or a wrapper library.
- Document the chosen eviction policy and its rationale in the service's architecture decision records.
- Conduct periodic Redis memory audits using `--bigkeys` and `MEMORY DOCTOR`.
