# Performance and production diagnostics

Use this reference when a changed path has credible responsiveness, memory, energy, build-time, size
or diagnostic consequences. A performance finding needs an affected workload and a concrete causal
path or suitable measurement. Do not demand every instrument, a new monitoring SDK, or universal
latency/memory thresholds.

## Match the symptom to evidence

| Changed risk | Useful inspection or evidence |
|---|---|
| Launch delay / CPU work / UI blocking | Startup dependency path, Time Profiler, Hangs, relevant signposts or focused performance tests |
| Retained objects / repeated lifetime growth | Ownership graph, Memory Graph, Allocations/Leaks and repeat/open-close workload |
| Transient memory peak / jetsam | Buffer/copy/cache path, Allocations or memory metrics, relevant device jetsam report |
| Scroll / layout / animation hitches | Identity/invalidation/render path, relevant Core Animation/hitch trace and affected UI flow |
| Network churn / disk or battery cost | Request/retry/cancellation trace, Network/energy/disk evidence and realistic workload |
| Crash / watchdog / production hang | Correct build and symbols, relevant stack/diagnostic, affected lifecycle and regression evidence |
| Compile-time regression | Comparable clean/incremental builds, type-checker/macro diagnostics and module dependency graph |
| App size / resource delivery | Comparable archive/app/dependency sizes, asset catalog/duplicate resource inspection and delivery-path evidence |

## Review the actual workload

- Trace launch initialization, synchronous storage/network waits, expensive decoding/formatting,
  actor or queue contention, repeated work and cancellation. Offloading CPU work must preserve
  thread/executor contracts; an async function can still occupy the main actor.
- Distinguish a persistent leak from a cache with a defined bound, and both from transient
  copies/decoded images/autoreleased objects. Check memory-pressure response and process/extension
  budgets where affected; jetsam is not one fixed limit across all hardware.
- For battery/thermal work, inspect polling, timers, background loops, sensor/radio usage, excessive
  transfers and repeated rendering. Low Power Mode, thermal state and background eligibility can
  change behavior; test only the changed supported obligation.
- For comparable traces record reviewed SHA/build, optimization/configuration, device/OS,
  workload/data volume and relevant conditions. Simulator measurements, debug builds, different data
  sets or a generic green performance suite may not support an asserted device regression. Static
  causal evidence can establish an obvious blocking operation without an arbitrary benchmark quota.
- For type-checker/build cost, inspect changed complex expressions, generic specialization,
  builders/macros, generated code and dependency invalidation. Clean versus incremental builds
  answer different questions; a slow developer machine alone does not establish a PR regression.
- For size/assets/on-demand resources, inspect duplicate products, oversized or unnecessarily
  decoded assets, changed binary dependencies, caching and unavailable-resource recovery. Resource
  membership correctness alone does not prove efficient delivery.

## Diagnose crashes, hangs and production behavior

- Match application version/build UUID and dSYM/symbol provenance to the reported binary before
  using a symbolicated stack. Distinguish crash, watchdog/hang, jetsam, startup/linkage failure and
  third-party reporting artifacts. Jetsam reports describe memory conditions and lack ordinary
  thread backtraces; missing a crash SDK event does not prove no termination occurred.
- Use relevant Organizer, MetricKit, device logs or existing crash/performance tooling when
  accessible. Verify the reported OS/device, workload and target relation; production diagnostics
  from an older release can establish intent/history but cannot alone prove the reviewed fix.
- For changed os_log/signposts/analytics, check useful identifiers and interval boundaries,
  structured event meaning, cancellation/error correlation, data volume/overhead and
  privacy/redaction. Every app need not adopt signposts or MetricKit; the question is whether
  required diagnostics remain truthful and useful.
- For crash/hang repairs, connect the observed failing path to the changed code and focused
  regression evidence where feasible. Runtime tracing is not a prerequisite for every statically
  proven defect. Hardware, production telemetry or symbol access limits remain named evidence gaps
  under the existing rubric, not invented code faults.

## Primary guidance

- [Improving
  responsiveness](https://developer.apple.com/documentation/xcode/improving-app-responsiveness).
- [Memory, thread and crash
  diagnostics](https://developer.apple.com/documentation/xcode/diagnosing-memory-thread-and-crash-issues-early).
- [Crash reports and device
  logs](https://developer.apple.com/documentation/xcode/diagnosing-issues-using-crash-reports-and-device-logs).
- [Jetsam
  reports](https://developer.apple.com/documentation/xcode/identifying-high-memory-use-with-jetsam-event-reports).
- [MetricKit](https://developer.apple.com/documentation/metrickit).
