# iOS review domains

Apply only the lenses triggered by the PR. First read project settings, architecture, and platform
targets. These checks identify questions and failure modes; they are not automatic findings.

## Select the relevant lenses

Use changed contracts and affected consumers as triggers. Include configuration,
entitlements, targets, generated code and preserved behavior. Search the headings
before reading this reference in full. Read the triggered sections and necessary
cross-boundary context; do not treat unrelated sections as a checklist.

| Changed concern | Sections to read |
|---|---|
| Product flow, process/scene ownership or ARC | Product and domain correctness; Runtime, memory, and legacy threading |
| Toolchain, project, dependencies or release configuration | Project, build, and distribution; Architecture, modules, and dependency injection |
| Swift contracts or asynchronous work | Swift and API correctness; Swift concurrency |
| UI, routes or design components | SwiftUI, navigation, and animation; UIKit and legacy integration; Reducer/state-machine architectures when used |
| Storage, migrations or sync | Persistence: general, plus the actual storage engine or CloudKit/iCloud section |
| Service/API, authentication or telemetry | Networking, APIs, and backend services; Security, privacy, and release safety |
| Tests, generated code or test infrastructure | Tests and evidence; Agentic and generated-change integrity |

Read these specialist references only when triggered:

| Trigger | Additional guidance |
|---|---|
| Push/background scheduling, links, intents, widgets, Live Activities, App Clips, iPad scenes/input, companion watch, or supported related destinations | [apple-platform-integrations.md](apple-platform-integrations.md), only the affected sections |
| Changed hot path, memory/resource budget, launch, hangs/crashes, build time, binary size, or diagnostic instrumentation | [performance-and-diagnostics.md](performance-and-diagnostics.md), only the affected sections |

Every blocking finding still needs a supported P0–P2 trigger-to-consequence trace. Domain breadth
does not require every technology, OS/device combination, profiling tool, or test framework. Apply
evidence limits through the existing scoring authority; never invent a domain-specific cap.

## Product and domain correctness

- Compare copy, constants, ordering, navigation, completion criteria, persistence, and negative
  requirements with the authoritative task.
- Trace first run, relaunch, partial completion, interruption, background/foreground, cancellation,
  permission denial, retry, offline, and partial service failure.
- Verify that work delivered for one step does not prematurely complete or bypass a later step.
- Confirm downstream consumers can obtain the state the current task promises to produce.
- For calendars, prayer times, travel, weather, and scheduling, distinguish the device time zone
  from the selected event/location time zone. Validate daylight-saving boundaries,
  significant-time-change/time-zone notifications, day rollover, background refresh, and
  calendar/locale semantics where relevant.
- Treat domain semantics as correctness: a displayed event, boundary, or status must match its real
  product meaning, not merely fit the data model.

## Project, build, and distribution

- Inspect deployment targets, Swift version/mode, strict-concurrency settings, default actor
  isolation, enabled upcoming features, package versions, target membership, and generated sources.
- Review the project representation the repository actually uses—such as `project.pbxproj`,
  `.xcproj`, or a generator manifest—and follow its declared source of truth. Verify semantic
  changes to targets, references, build phases, settings, schemes, and package links; ignore UUID
  ordering or serialization noise by itself. A format conversion must be intentional and compatible
  with the repository's pinned Xcode, CI, and generator tooling.
- With synchronized or buildable folders, do not expect one project-file entry per source. Inspect
  folder-level membership and exclusions so app sources, tests, resources, generated files, and
  configuration files enter only intended targets and are not compiled or copied twice.
- When lockfiles are versioned, align them with dependency intent. For `Package.resolved`, account
  for whether this repository is an app or a reusable package and inspect accidental
  source/revision/checksum or transitive-version drift. For `Podfile.lock`, verify changes result
  from an intended install/update and follow the repository's Pods source-control policy.
- Trace changed `.xcconfig` values through includes, base configurations, and project/target
  overrides for every affected configuration. Check missing includes, dropped `$(inherited)`,
  incorrect platform/configuration conditions, machine-local paths, and committed secrets.
- Check Info.plist usage descriptions, privacy manifests, entitlements, URL/background modes,
  signing assumptions, bundle identifiers, and capability setup for changed features.
- Audit required-reason APIs and `PrivacyInfo.xcprivacy` entries under the current SDK/App Store
  rules, including third-party manifests. Verify permission purpose strings are present and
  localized through the project's `InfoPlist.strings` strategy.
- Verify assets, fonts, localizations, JSON, database resources, previews, test files, and new
  source files belong to the intended targets.
- Watch for duplicate build products, missing resources, unsafe build scripts, or package changes
  unrelated to the feature.
- For a deployment-target or SDK/toolchain change, check oldest-supported paths, availability
  guards, extension/package alignment, removed compatibility behavior, and affected release notes. A
  newer SDK does not require adopting every new API or raising the minimum OS.
- When distribution changes, trace Debug/Release/beta configurations, bundle/team/profile and
  entitlement alignment, archive/export settings, and embedded products. A simulator build does not
  validate device signing or export; use affected archive/CI evidence when that contract is
  material. Repairing credentials or App Store settings is separate operational work.
- Inspect changed CI/Xcode Cloud/fastlane workflows for actual command failures, pinned
  toolchain/destinations, cache keys and stale inputs, parallel-test isolation, signing-secret
  exposure, and artifact-to-SHA provenance. Follow existing Tuist/XcodeGen and workspace conventions
  without prescribing a tool.
- Vet changed packages and binary SDKs for provenance/license constraints required by the project,
  supported architectures/platform slices, linkage/resources, transitive compatibility, privacy
  behavior, and credible app-size impact. SPM packaging alone does not establish dependency quality.

## Runtime, memory, and legacy threading

- Distinguish process-wide services from scene/view-owned state and effects. A scene becoming
  inactive or disappearing need not mean every scene or the process has ended. Review teardown,
  restoration, and shared-service coordination on the actual ownership path.
- Suspension pauses ordinary execution; termination can occur without a final cleanup callback.
  Check required durable checkpoints, recoverable in-flight work, and relaunch reconciliation. Do
  not rely on termination callbacks, timers, or background runtime to make a critical write happen
  eventually.
- Trace ARC ownership through escaping closures, stored tasks, delegates, timers/display links,
  observers, Combine subscriptions, and caches. Determine who releases/cancels them; a strong
  capture is defective only when the actual graph/lifetime creates harm. Verify `unowned` lifetime
  guarantees and do not blanket-replace them with `weak`.
- For memory-intensive loops or media work, inspect transient copies/decoded buffers, bounded
  caches, bridging/autorelease accumulation, and response to memory pressure. Autorelease pools help
  relevant Objective-C allocations, not every Swift allocation. Do not invent one universal jetsam
  threshold; use affected process/device evidence.
- Check synchronous dispatch/waits for queue cycles or main-thread stalls, timer/run-loop modes for
  required interaction behavior, and thread-bound legacy APIs at callback boundaries. Main-thread
  and actor/executor guarantees must come from the current contract/settings; `async` alone does not
  mean background execution.

## Swift and API correctness

- Inspect force unwraps/casts, `try!`, swallowed failures, accidental reference cycles, unstable
  `Hashable`/identity, value/reference semantic mismatches, and duplicated source of truth.
- Verify public/internal contracts, error semantics, availability, generic constraints, `Sendable`
  promises, and decoding defaults at boundaries.
- Search for an existing project abstraction before accepting duplicated clients, formatters,
  routers, storage, or domain logic.
- Do not flag older safe APIs merely because newer syntax exists. Tie modernization to a concrete
  correctness, availability, accessibility, or maintenance consequence.
- For generic/protocol API changes, inspect associated-type constraints, existential versus opaque
  return semantics, overload/conformance compatibility, and actual callers. Prefer the abstraction
  that preserves the required contract; no syntax choice is universally superior.
- Value containers can contain shared references. Check aliasing, mutating reference payloads,
  copy-on-write assumptions, and unstable equality/hash semantics. Copy/allocation costs require an
  affected workload before becoming performance findings.
- For result builders or macros, inspect the relevant expanded/control-flow behavior, generated
  API/identity, availability and build dependencies where safe. The execution trust gate still
  applies; merely seeing a macro is neither a defect nor proof that generated behavior is correct.

## SwiftUI, navigation, and animation

- Decide ownership first: local value state, parent binding, observation-owned reference, or
  injected shared dependency. Flag mirrored/derived state only when invalidation can drift.
- Keep live service work and substantial sorting/filtering/formatting/object creation out of `body`
  and repeated initializers.
- Check view identity, stable `ForEach` IDs, conditional root replacement, navigation destination
  consistency, item-vs-Boolean presentation state, and route payload size.
- Prefer lifecycle-bound `.task`/`.task(id:)` for view async work. Nested untracked tasks can
  outlive the view and require explicit ownership/cancellation.
- Ensure implicit animation names its driving value. Sequential animation should follow
  completion/state, not fragile sleeps. Re-entry should not replay an entrance unexpectedly.
- Respect Reduce Motion; large transforms should degrade to a calmer transition. Verify animation
  cancellation and inactive/offscreen work.
- For affected UI, verify proportionate accessibility and layout risks such as Dynamic Type
  truncation, semantic controls, useful labels/traits/state, focus, contrast, or localized
  expansion. Check only project-supported localizations, and check RTL only when a supported
  localization is RTL or authoritative scope requires it. Do not turn every listed accessibility
  technique into a universal test requirement.
- For performance, prioritize observation fan-out, unstable identity/list churn, main-thread render
  work, image decoding, and layout/animation complexity. Require a credible path or trace before
  blocking.
- Honor repository design tokens and shared-component contracts; verify changed variants, SF Symbol
  availability/rendering, semantic colors in supported appearance modes, and text/layout expansion.
  Do not require creating a design system to review a component.
- Check VoiceOver grouping/order/focus and Switch Control or keyboard operability where affected
  interaction depends on them; custom gestures need usable alternatives when required. Apply dark
  mode, RTL, localization and Dynamic Type checks to supported behavior proportionally.
- Trace coordinator/module routes through cold and warm launch, authentication deferral, scene
  selection, repeated delivery and restoration when affected. Keep route payload/decoding contracts
  compatible with callers; read the platform integration reference for external entry points.

## Architecture, modules, and dependency injection

- Judge MVVM, reducers/UDF/TCA, coordinators and layered designs against responsibilities,
  ownership, testability and actual change costs. Missing a preferred layer/pattern/ADR is not a
  defect; trace a concrete violated contract or coupling consequence.
- For SPM/module changes, inspect dependency direction/cycles, feature/core boundaries, interface
  versus implementation exposure, public API compatibility, resource ownership, and build-graph
  invalidation. Dedicated interface targets are optional; flag leaks or cycles only with a material
  consequence.
- Trace dependency assembly across production, previews, tests and SwiftUI environments. Check
  lifetime/scope, accidental fallback to live services, missing environment values and shared
  mutable instances. Use repository-approved DI; do not mandate a framework or protocol for every
  type.
- For staged UIKit/Objective-C or architecture migrations, verify preserved behavior at the
  coexistence boundary, adapters, target membership, ownership and a viable transition/recovery
  path. Long-term debt or roadmap work is outside a bounded PR unless explicitly required.

## Reducer/state-machine architectures

- Represent mutually exclusive destinations and phases as mutually exclusive state rather than
  drifting Boolean combinations.
- Verify child delegate/action ordering, especially when a parent clears child state. Capture needed
  child values before teardown.
- Ensure effects use injected dependencies, clocks, and schedulers; surface failures; and give
  repeated requests explicit cancellation or ordering semantics.
- Cancellation must protect against both late success and late failure. Request identity or
  generation checks may be needed when underlying APIs cannot cancel promptly.
- Test happy, denial, failure, cancellation, stale-response, repeated-action, and effect-completion
  paths deterministically.

## Swift concurrency

- Read concurrency settings for every affected target/package before assuming missing isolation.
- Inspect actor methods that read state, suspend, then act on the old assumption. Reentrancy can
  invalidate pre-`await` state.
- Prefer structured tasks. `Task {}` inside loops and stored unstructured tasks can lose error
  aggregation, awaiting, priority, and cancellation.
- Use `Task.detached` only for a demonstrated need to discard inherited context; asynchronous I/O
  alone does not require it.
- Cancellation is cooperative: long CPU loops need checks; stored tasks need teardown;
  `CancellationError` is normal lifecycle control flow, not a user failure.
- Checked continuations must resume exactly once on all paths, including cancellation. Streams need
  completion, termination cleanup, and bounded buffering when producers can outrun consumers.
- Treat `@unchecked Sendable` and `assumeIsolated` as proof obligations. Verify synchronization or
  an externally guaranteed executor.
- Do not blanket-ban GCD, locks, callbacks, Combine, or delegates. They remain valid where their
  ownership and synchronization are explicit.
- For incremental strict-concurrency migration, read each module's language mode, feature flags and
  imported annotations. Verify `@preconcurrency`, dynamic isolation and callback bridges do not
  conceal an actual violation. Executor behavior of nonisolated async functions is
  toolchain/setting-sensitive; do not infer it from spelling alone.
- For Combine changes, trace subscription retention/teardown, upstream versus downstream scheduling,
  demand/backpressure where relevant, and conversion to async cancellation/error semantics. For
  Objective-C boundaries, check nullability, bridging, selectors/visibility, KVO and documented
  callback threads without assuming imported annotations are complete.

## Persistence: general

- Honor the repository's mandated source of truth. Do not move structured domain data to
  `UserDefaults` merely for convenience.
- Persist correctness-critical state before navigation or teardown can destroy it, and surface write
  failures.
- Keep preferences, onboarding/completion markers, structured profiles, caches, and secrets in
  storage appropriate to their semantics. Secrets belong in Keychain or an approved secure store.
- Review fresh install, upgrade, migration, default, uniqueness, relationship, delete-rule,
  indexing, transaction, rollback, and concurrency behavior.
- Validate migrations with realistic old schemas/data and prove failed writes cannot leave a false
  completion marker.
- For offline sync changes, inspect durable outbox/checkpoints, replay/idempotency,
  tombstones/deletes, conflict ownership, account isolation and compatibility with older clients. A
  successful local write is not remote acknowledgment; bound recovery after partial commits or
  reconnect.

### Core Data

- Respect context confinement; pass `NSManagedObjectID` or value data across queues and re-fetch.
- Check parent/child or background-context save propagation, merge policy, unique constraints,
  delete rules, batch updates, fetched-results observation, and migration options.
- Avoid retaining managed objects across context reset or store replacement.

### SwiftData

- Do not pass `ModelContext` or model instances across actor boundaries; transfer a persistent
  identifier/value and re-fetch in the receiving context.
- A persistent identifier can remain temporary until the first successful save. Explicitly save at
  correctness boundaries instead of relying on autosave timing.
- Verify relationship inverse and delete behavior; default nullification can orphan data or violate
  a non-optional inverse.
- Property observers on persisted model properties are not a reliable persistence hook. Transient
  values need safe defaults/reset behavior.
- Keep `@Query` in views; service/store code should fetch through its owned context. Audit
  `#Predicate` features for runtime support, not just compilation.
- Apply CloudKit restrictions only after confirming a CloudKit-backed container; then check
  defaults/optionality, relationship optionality, unsupported uniqueness, and eventual consistency.

### SQLite / GRDB

- Verify ordered, idempotent migrations; foreign-key enforcement; unique/index strategy; transaction
  boundaries; busy handling; observation lifetimes; and rollback on partial failure.
- Keep SQL arguments bound, schema ownership explicit, and readers/writers coordinated through the
  chosen library.
- Test migration from every supported schema checkpoint, not only an empty database.

### CloudKit / iCloud synchronization

- First confirm the actual container/store/sync architecture. Review affected schema compatibility,
  account/availability changes, sign-out or account replacement, partial errors and eventual
  consistency; do not apply SwiftData-specific constraints to a custom CloudKit client.
- Where custom zones/change tokens/subscriptions or conflict handling change, trace invalidated
  tokens, remote deletes, retry/backoff and re-fetch/reconciliation without dropping local edits.
  Check the product's offline and recovery promise rather than requiring CloudKit for every sync
  feature.

## Networking, APIs, and backend services

- Verify transport/DTO/domain separation where the project requires it, status and decoding
  semantics, cancellation, timeout, retry/backoff, idempotency, pagination, caching, and offline
  behavior.
- Retrying a non-idempotent request or swallowing a decoding error can be a correctness defect;
  distinguish transient service failure from malformed data.
- For an affected backend SDK or custom client, inspect session/token refresh, auth-state
  transitions, query/RPC and decoding errors, pagination, remote-storage access, realtime/listener
  cleanup, and data/schema/API ownership.
- Treat the app as untrusted. Authorization belongs in server-side policy—for example Supabase Row
  Level Security or Firebase Security Rules—and privileged service/admin secrets must remain
  off-device.
- Avoid partial local/remote ownership: define conflict resolution, optimistic update rollback, and
  which source wins after reconnect.
- For API evolution, check deployed older-client/current-server and new-client/older-server
  combinations that rollout permits, version negotiation/defaults, cursor ordering/deduplication and
  typed error recovery. Inspect backend contracts or acknowledge unavailable evidence; do not invent
  server guarantees from client models.

## UIKit and legacy integration

- Inspect lifecycle ownership, main-thread UI work, delegate/data-source retention, notification/KVO
  cleanup, containment, reuse, diffable-data-source identity, Auto Layout ambiguity, and appearance
  callbacks.
- Ensure SwiftUI wrappers keep coordinator identity stable and update UIKit/AppKit views without
  redoing one-time setup or retaining stale closures.
- Verify accessibility, Dynamic Type, reuse reset, and cell/task cancellation just as for SwiftUI.
- Do not demand a wholesale SwiftUI, async/await, Observation, SwiftData, or Swift Testing rewrite
  unless migration is explicitly in scope.
- For interop/refactoring, preserve containment, appearance, navigation/focus and delegate/callback
  semantics across hosting/representable adapters. Validate only behavior touched by the migration;
  a safe legacy subsystem does not need a wholesale rewrite.

## Tests and evidence

- Tests should assert behavior and requirements, not private implementation constants. Cover
  failure, cancellation, persistence, migration, time-zone/locale, and lifecycle boundaries
  appropriate to the feature.
- Keep time, UUIDs, randomness, transport, location, permissions, and storage deterministic through
  project-approved dependency injection.
- Swift Testing and XCTest may coexist. UI tests remain XCTest. Do not demand migration from a
  mature suite unless it is part of the task.
- For Swift Testing, check that tests contain real expectations, use `#require` for prerequisites,
  assert exact errors where important, avoid fixed sleeps/live networks, and do not rely on
  execution order or shared default stores.
- Parameterized tests with two collections form a Cartesian product; use paired input when that is
  the intent. Treat `.serialized` according to the project's installed Testing version and scope,
  not a blanket rule.
- UI/snapshot automation is one valid evidence source when layout, localization, Dynamic Type,
  permission UI, animation, or visual state is central. Do not require a new
  UI/snapshot/accessibility test target solely for 5.0 when existing project-standard tests or a
  representative simulator/device check covers behavior-bearing product proof. Focused inspection
  may cover only non-behavioral platform-quality subchecks permitted by
  [five-point-evidence.md](five-point-evidence.md).
- When test infrastructure changes, inspect hidden failures behind retries/quarantine, parallel
  shared-state pollution, and simulator/device coverage for the actual mechanism. A device farm is
  an option, not a prerequisite; a fake transport does not prove radio/background delivery.
- Run project-required lint/custom architecture checks when affected and safe. Check changed
  rules/configuration for silently disabled enforcement or excluded source. Do not introduce
  SwiftLint, new style rules, or a coverage quota as a merge requirement.

## Agentic and generated-change integrity

- Do not penalize code merely because an agent generated it. Judge the resulting behavior and
  evidence.
- Reconcile implementation with the approved plan, task, memory bank, and actual repository APIs.
  Look for invented symbols, unsupported flags, missing target membership, stale paths, placeholder
  data, and comments that claim behavior the code does not provide.
- Check broad mechanical edits for duplicated abstractions, lost platform conditions, overwritten
  hand-written changes, inconsistent naming/contracts, and scope outside the task.
- Treat generated tests as independent evidence only when they assert authoritative behavior rather
  than mirroring implementation constants or mocks that cannot fail meaningfully.
- Inspect agent-authored dependency, build-script, migration, entitlement, and schema changes with
  the same execution and supply-chain caution as human-authored changes.

## Additional triggered platform lenses

- **Audio/AVFoundation:** session category/mode/options, interruption and route-change handling,
  background playback entitlement, remote commands/Now Playing state, and download/task lifecycle.
- **StoreKit/RevenueCat:** purchase verification, entitlement refresh, restore, revocation/refund,
  offline grace, account changes, transaction finishing, and test-environment isolation.
- **Media, camera, photos, health, contacts, and location:** limited/denied/restricted
  authorization, purpose strings, data minimization, cancellation, background modes, and recovery
  after settings changes.

## Security, privacy, and release safety

- Minimize sensitive data and permission scope. Confirm usage descriptions match behavior and
  permission requests occur in understandable context.
- Search changed logs, analytics, crash breadcrumbs, and persistence for names, coordinates, tokens,
  health data, contacts, and other sensitive values; redact or omit secrets and prohibited data.
  Intentional project-approved analytics/crash telemetry is acceptable when it follows applicable
  consent, disclosure, minimization, and retention rules.
- Review URL handling, pasteboard/files, web views, deep links, authentication transitions,
  dependency integrity, and build scripts where changed.
- For migrations, remote flags, and staged rollouts, identify rollback/recovery behavior and
  compatibility with the previous released client or backend contract.
- For Keychain/file protection changes, verify accessibility/access-control classes, device-lock and
  background access, access groups/entitlements, backup/synchronization semantics and
  logout/deletion behavior. For biometrics/Secure Enclave, inspect fallback, enrollment/key
  invalidation and authorization boundaries where used; stronger restrictions can break a required
  locked-device workflow.
- For OAuth/OIDC, browser auth, Sign in with Apple or passkeys, trace initiation through callback,
  cancellation, account linking and credential/session state. Verify redirect matching,
  state/nonce/PKCE and challenge/replay handling as the chosen protocol requires;
  identity/token/attestation validation belongs at the correct trusted boundary. Do not require
  every auth technique for every app.
- For changed ATS exceptions, certificate pinning or App Attest, inspect intended trust boundaries,
  server-side verification, replay resistance, key/certificate rotation and recovery. Pinning and
  jailbreak signals have trade-offs; neither is a universal requirement or a substitute for server
  authorization.
- For tracking/data SDK changes, check actual initialization and network/data flows against ATT
  states, privacy manifests/required reasons, purpose strings and App Store privacy declarations
  where accessible. Denial/restriction and consent timing must match the intended policy; a manifest
  or nutrition label does not prove an SDK behaves accordingly. Missing release-console access is a
  named evidence limit, not invented noncompliance.
- For remote flags/config, kill switches or forced updates, check safe defaults, stale/unavailable
  config, permitted combinations, targeting/version compatibility and reachable recovery when the
  backend or store is unavailable. Confirm the changed release/review requirement without making
  phased rollout, TestFlight or expedited-review operations mandatory on every PR.
- If a finding involves an exposed credential, active exploit, or sensitive user data, do not
  publish operational details in a public review. State the blocker minimally and use an authorized
  private disclosure path; ask the user before creating any separate private message or incident
  action.
