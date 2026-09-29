# Triggered Apple platform integrations

Read only sections implicated by the iOS product's actual targets, capabilities, changed contracts,
or affected consumers. These lenses do not require adopting a platform or capability. Apply the
existing severity/evidence rubric, including proportional checks, equivalent evidence, and optional
locked 5.0 paths. Verify uncertain SDK, OS, capability, quota and policy behavior in current
official documentation; do not assume the latest release is the repository's target.

## Push and background execution

- Trace foreground catch-up and durable recovery if silent push or scheduled refresh is delayed,
  coalesced or absent. Neither is a dependable clock or the sole acknowledgment of a required sync
  operation. Distinguish app suspension, termination, user force-quit, disabled refresh and
  locked-device state when material.
- Select the changed mechanism against its purpose: short finite background completion,
  refresh/processing tasks, background URLSession, visible-notification service work or other
  supported modes. Background modes are not interchangeable keep-alive permissions; verify actual
  deployment/SDK eligibility instead of frozen time/quota assumptions.
- For BGTaskScheduler, check permitted identifiers, registration timing and target configuration,
  submission/failure paths, rescheduling where intended, expiration-driven cancellation and
  completion exactly once. Avoid committing success before durable work completes; prevent stale
  completions from mutating a newer task.
- For push, verify token rotation/environment/account association, authorization and settings
  transitions, notification categories/actions, payload parsing, duplicate/reordered delivery and
  cold/warm routing. Server delivery evidence must match the changed contract; client registration
  does not prove APNs delivery.
- For background networking, trace session/delegate restoration, file and credential availability
  while locked, app/extension ownership and completion-handler lifetimes. A deterministic scheduler
  test can prove ordering/recovery logic, not system scheduling or radio delivery.

## External entry points and cross-module navigation

- For Universal Links or custom URLs, inspect associated domains/AASA or scheme configuration where
  accessible, route allowlisting/decoding, and URL-to-module contracts. Avoid treating a URL as
  trusted authorization or accepting arbitrary redirect destinations.
- Trace cold launch, an already-running app, logged-out/account-changing state, restoration,
  repeated delivery and target-scene selection. Capture pending routes until prerequisites are met
  and consume them without losing or duplicating required navigation.
- For Spotlight, Siri/App Intents and shortcuts, check parameter/entity resolution, supported
  invocation contexts, authorization/data access and outcome/error semantics when the normal app UI
  is absent. Inspect exposed/donated metadata for sensitive content and stale identifiers; do not
  require every app to index or donate data.
- For App Clips, verify the supported invocation/association/configuration, unavailable
  capabilities, size/resource constraints and handoff/data continuity with the full app. Do not
  assume entitlement or shared-storage parity; check the actual configuration and current platform
  contract.

## Widgets, Live Activities and other extensions

- Verify app-group/container ownership, entitlement and target/resource membership, atomic
  shared-state access, account isolation and schema compatibility across app/extension versions. An
  app-group identifier alone does not make in-memory singletons shared or coordinate database
  access.
- For WidgetKit, inspect timeline/provider failure paths, placeholder/snapshot privacy, stale data,
  supported families, interaction intents and appropriate invalidation. Reload requests do not
  promise immediate refresh; use actual timeline/update budgets without hardcoding universal quotas.
- For Live Activities, trace start/update/end/dismissal, stale/expired content, account/logout
  transitions and authorization/availability. If remote updates change, inspect token lifecycle and
  the client/server state contract; durable app state must not depend on an activity continuing
  forever.
- For extensions, verify process/time/memory constraints, supported APIs, cancellation and
  completion lifetimes. A successful app-target build does not establish that an affected extension
  links or runs. Use affected-target evidence, not every extension target in the repository.

## iPad, scenes, adaptive layout and input

- Separate scene-local navigation, selection, presentation and restoration from process-wide
  account/data services. Check simultaneous scenes, disconnect/reconnect and scene-specific effect
  cancellation; do not cancel every scene's work when one backgrounds or route to an arbitrary first
  window.
- Review supported resizable/multitasking layouts against the current scene/window geometry, not
  fixed device dimensions or `UIScreen` assumptions. Check collapse/expansion of sidebar/split
  navigation, preserved selection/detail and compact/regular transitions where relevant. Stage
  Manager, split view and Slide Over behavior depends on supported OS/product scope; do not demand
  every combination.
- For changed keyboard/pointer/trackpad interactions, trace focus, command
  discoverability/conflicts, selection, hover and a usable non-touch path. Drag/drop must validate
  imported types/data, handle asynchronous cancellation, preserve security-scoped resource access
  where needed and define copy/move ownership.
- For drawing/Pencil or external-display features, check input/tool/session lifetime, saved content,
  scene/display role and disconnection recovery. These capabilities are conditional; a general iPad
  screen does not require them.
- Scene-lifecycle adoption and multi-window support are separate decisions. Verify current
  SDK/repository requirements before flagging adoption/configuration; safe single-window products do
  not need multi-window merely to receive 5.0.

## Companion watchOS integration

- Confirm whether the watch app is independent or phone-dependent, who owns authentication/data and
  what works when the phone is unavailable. Check account replacement, restore, installation/version
  skew and shared-contract compatibility rather than assuming app-group access across devices.
- Match Watch Connectivity transfer semantics to the product: `sendMessage` is immediate
  communication with an activated reachable counterpart; application context is replaceable latest
  state; user-info/file transfers queue work. Reachability can change after a check. Inspect
  activation/deactivation, delegate ownership/isolation, errors, pending transfers and
  retry/reconciliation; do not discard required work merely because the peer is unreachable.
- Distinguish transport enqueue/completion from domain acknowledgment. Where duplicate application
  or ordering matters, check identifiers, replay/idempotency, payload versioning and reconciliation.
  Do not require an extra application queue when platform transfers and the actual outcome contract
  already suffice.
- For complications/WidgetKit/Smart Stack changes, check supported families, relevance and
  stale-content/update behavior under watch budgets. For workout/HealthKit, refresh or extended
  runtime sessions, verify purpose-specific eligibility, permissions, lifecycle,
  expiration/invalidation and required recovery; these mechanisms are not generic unlimited
  background execution.
- Check relevant small-screen accessibility, Digital Crown/focus, haptics and bounded
  CPU/memory/network use. Match battery/performance evidence to representative hardware and
  workload; no universal numerical budget is assumed.
- Changed obligations that depend on real paired delivery or system execution need suitable paired
  physical-device evidence because simulator support is incomplete. Application routing, enqueue
  choice and recovery logic can be proven with deterministic tests without automatically requiring
  hardware. Simple copy, static configuration or pure state changes do not automatically require
  hardware. Name the exact missing mechanism/evidence and use the existing validation rules.

## Supported Catalyst and compatible-app destinations

- Activate this section only when the iOS product supports or materially changes Catalyst, Designed
  for iPad on Mac, or compatible iOS/iPadOS execution on visionOS. Inspect platform build
  conditions, framework/API availability, entitlement/resource differences, window/input behavior
  and graceful fallback for unavailable hardware.
- Compilation/linkage is not proof that camera, location, health or other hardware-dependent
  behavior is available on a compatible destination. Check current platform documentation and
  runtime support checks, not a permanent list of unavailable APIs.
- Do not require adopting native macOS/visionOS architecture or adding a new destination. A full
  standalone watchOS, macOS or native visionOS review needs its own authorized specialist scope.

## Primary guidance

- [Background
  strategies](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app)
  and [background
  notifications](https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app).
- [Universal
  Links](https://developer.apple.com/documentation/xcode/supporting-universal-links-in-your-app),
  [App Intents](https://developer.apple.com/documentation/appintents),
  [WidgetKit](https://developer.apple.com/documentation/widgetkit), and
  [ActivityKit](https://developer.apple.com/documentation/activitykit).
- [Desktop-class iPad
  apps](https://developer.apple.com/documentation/uikit/building-a-desktop-class-ipad-app) and
  [multiple
  windows](https://developer.apple.com/documentation/uikit/supporting-multiple-windows-on-ipad).
- [WCSession](https://developer.apple.com/documentation/watchconnectivity/wcsession), [Watch
  Connectivity transfer
  sample](https://developer.apple.com/documentation/watchconnectivity/transferring-data-with-watch-connectivity),
  and [extended runtime
  sessions](https://developer.apple.com/documentation/watchkit/using-extended-runtime-sessions).
- [Compatible apps on
  visionOS](https://developer.apple.com/documentation/visionos/making-your-app-compatible-with-visionos/).
