# Runbook: High CPU Usage in Microservice

## Severity
P2 - High

## Symptoms
- CPU utilization exceeds 90% for more than 5 minutes on one or more pods.
- Response latency (p99) increases significantly, often exceeding SLO thresholds.
- Kubernetes HPA triggers autoscaling but new pods also saturate quickly.
- Upstream services report increased timeouts when calling the affected microservice.
- Thread pool exhaustion warnings appear in application logs.

## Diagnosis Steps
1. Identify the affected pods: `kubectl top pods -n <namespace> --sort-by=cpu`.
2. Check if the spike correlates with a recent deployment: `kubectl rollout history deployment/<service>`.
3. Capture a CPU profile: for Go services use `pprof`, for Java use `async-profiler` or `jstack`.
4. Review recent code changes for algorithmic regressions: `git log --since="2 days ago" --oneline`.
5. Check for runaway queries or hot loops in the application logs.
6. Verify external dependency latency: a slow downstream call can cause thread buildup and high CPU from context switching.
7. Check for garbage collection pressure (JVM): `kubectl exec <pod> -- jstat -gcutil <pid> 1000`.

## Resolution Steps
1. If caused by a bad deployment, roll back: `kubectl rollout undo deployment/<service>`.
2. If caused by a traffic spike, scale horizontally: `kubectl scale deployment/<service> --replicas=<N>`.
3. If caused by an expensive query or hot loop, apply the code fix and deploy.
4. If GC pressure is the root cause, tune JVM heap settings (`-Xmx`, `-XX:MaxGCPauseMillis`).
5. If a downstream dependency is slow, enable or tighten circuit breakers to shed load.
6. After mitigation, verify CPU returns to baseline on the Grafana dashboard.

## Prevention / Monitoring
- Set CPU alerts at 80% sustained for 3 minutes to catch issues before user impact.
- Require load testing for any code change that modifies hot paths or data processing logic.
- Include CPU profiling in the CI pipeline for performance-critical services.
- Configure Kubernetes resource requests and limits to prevent noisy-neighbor issues.
- Maintain baseline CPU metrics per service to detect regressions early.
