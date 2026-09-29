# Sources and provenance

This skill is an independently written synthesis. It adapts general review ideas and iOS engineering
checks from the projects below, while adding an original feature-intent workflow, confidence rubric,
GitHub submission policy, and convergence-focused re-review protocol.

## Source projects

- [SwiftUI-Agent-Skill at
  `be297ff`](https://github.com/twostraws/SwiftUI-Agent-Skill/blob/be297ff80dddec529af1f9b1f1f114aab6c9d11c/swiftui-pro/SKILL.md)
  by Paul Hudson — SwiftUI data flow, lifecycle, navigation, animation, accessibility, localization,
  and performance review signals. [MIT
  license](https://github.com/twostraws/SwiftUI-Agent-Skill/blob/be297ff80dddec529af1f9b1f1f114aab6c9d11c/LICENSE).
- [SwiftData-Agent-Skill at
  `922d989`](https://github.com/twostraws/SwiftData-Agent-Skill/blob/922d989473a9914210b41529a1ac5636aff4b8c1/swiftdata-pro/SKILL.md)
  by Paul Hudson — context isolation, explicit saves, relationships, predicates, migrations, and
  conditional CloudKit checks. [MIT
  license](https://github.com/twostraws/SwiftData-Agent-Skill/blob/922d989473a9914210b41529a1ac5636aff4b8c1/LICENSE).
- [Swift-Concurrency-Agent-Skill at
  `bee3f69`](https://github.com/twostraws/Swift-Concurrency-Agent-Skill/blob/bee3f69ba17142da148d3c5406f148ed62592b69/swift-concurrency-pro/SKILL.md)
  by Paul Hudson — actor isolation, reentrancy, structured tasks, cancellation, streams,
  continuations, and legacy interop. [MIT
  license](https://github.com/twostraws/Swift-Concurrency-Agent-Skill/blob/bee3f69ba17142da148d3c5406f148ed62592b69/LICENSE).
- [Swift-Testing-Agent-Skill at
  `2d6bba1`](https://github.com/twostraws/Swift-Testing-Agent-Skill/blob/2d6bba14a3c8bf3694f218b92fffe617c41ae43e/swift-testing-pro/SKILL.md)
  by Paul Hudson — Swift Testing assertions, parameterization, concurrency, async tests, and XCTest
  coexistence. [MIT
  license](https://github.com/twostraws/Swift-Testing-Agent-Skill/blob/2d6bba14a3c8bf3694f218b92fffe617c41ae43e/LICENSE).
- [Dimillian/Skills review-swarm at
  `05ba982`](https://github.com/Dimillian/Skills/blob/05ba982bfeb0d77d3c97d4542b0ee15034d05f84/review-swarm/SKILL.md)
  by Thomas Ricouard — intent-first review swarms, deduplication, evidence discipline, SwiftUI
  ownership/composition, and performance investigation. [MIT
  license](https://github.com/Dimillian/Skills/blob/05ba982bfeb0d77d3c97d4542b0ee15034d05f84/LICENSE).
- [sanyuan0704/sanyuan-skills code-review-expert at
  `08b6572`](https://github.com/sanyuan0704/sanyuan-skills/blob/08b6572ef108f22d4e8a3ecf9182a4bbef097744/skills/code-review-expert/SKILL.md)
  — impact-radius review, risk scanning, actionable inline feedback, and honest reporting of
  validation gaps. [MIT
  license](https://github.com/sanyuan0704/sanyuan-skills/blob/08b6572ef108f22d4e8a3ecf9182a4bbef097744/LICENSE).

## Primary platform and review guidance

- [Apple: Adding tests to your Xcode
  project](https://developer.apple.com/documentation/xcode/adding-tests-to-your-xcode-project) —
  proportional unit, integration, UI, and performance test roles.
- [Apple: Updating your Xcode project configuration file
  format](https://developer.apple.com/documentation/xcode/updating-your-xcode-project-configuration-file-format)
  — review the project representation actually used by the repository and treat format changes as
  compatibility-sensitive.
- [Apple: Managing files and folders in your Xcode
  project](https://developer.apple.com/documentation/xcode/managing-files-and-folders-in-your-xcode-project)
  — target membership and synchronized/buildable folder behavior.
- [Apple: Adding a build configuration file to your
  project](https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project)
  — `.xcconfig` ownership and configuration mapping.
- [Swift Package Manager: Resolving package
  versions](https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/ResolvingPackageVersions.md)
  — manifest and `Package.resolved` semantics.
- [CocoaPods: Using CocoaPods](https://guides.cocoapods.org/using/using-cocoapods.html) —
  `Podfile.lock` source-control and update expectations.
- [Git: git-worktree](https://git-scm.com/docs/git-worktree) — detached worktree creation, branch
  ownership, listing, and conservative removal semantics.
- [OpenAI: Codex worktrees](https://developers.openai.com/es-419/docs/environments/git-worktrees) —
  isolated parallel Codex checkouts, detached-head behavior, and managed worktree lifecycle.
- [Apple: Localization](https://developer.apple.com/documentation/xcode/localization) — validation
  of languages and regions the project actually supports.
- [Apple: Performing accessibility
  audits](https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app)
  — applicable accessibility checks without making one automation strategy universal.
- [Apple: App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) —
  privacy, permissions, analytics, data minimization, security, and app-completeness constraints.
- [Apple: Improving app
  responsiveness](https://developer.apple.com/documentation/xcode/improving-app-responsiveness) —
  performance validation for credible responsiveness risks.
- [Swift: Incremental concurrency
  adoption](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/incrementaladoption/)
  — mixed-module modes, callback/Objective-C interoperability and isolation migration; verify
  enabled compiler features rather than assuming executor behavior.
- [Apple: Choosing background
  strategies](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app)
  and [background
  notifications](https://developer.apple.com/documentation/usernotifications/pushing-background-updates-to-your-app)
  — eligible runtime, system-discretionary delivery and recovery requirements.
- [Apple: Building a desktop-class iPad
  app](https://developer.apple.com/documentation/uikit/building-a-desktop-class-ipad-app) — adaptive
  scenes, resizable windows, external displays and input integration for supported behavior.
- [Apple: WCSession](https://developer.apple.com/documentation/watchconnectivity/wcsession) and
  [Watch Connectivity
  transfers](https://developer.apple.com/documentation/watchconnectivity/transferring-data-with-watch-connectivity)
  — live versus queued/latest-state transport, session lifecycle and paired-device validation.
- [Apple: Compatible apps on
  visionOS](https://developer.apple.com/documentation/visionos/making-your-app-compatible-with-visionos/)
  — availability differences and graceful fallback without requiring native visionOS adoption.
- [Apple: Restricting Keychain
  accessibility](https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility),
  [App Tracking Transparency](https://developer.apple.com/documentation/apptrackingtransparency),
  and [privacy
  manifests](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files) —
  protection/lifecycle trade-offs, tracking authorization and app/SDK disclosure obligations.
- [Apple: Crash/device
  diagnostics](https://developer.apple.com/documentation/xcode/diagnosing-issues-using-crash-reports-and-device-logs)
  and [jetsam
  reports](https://developer.apple.com/documentation/xcode/identifying-high-memory-use-with-jetsam-event-reports)
  — diagnostic/symbol provenance and distinct memory-pressure termination evidence.
- [OpenAI: Testing skills with evaluations](https://developers.openai.com/blog/eval-skills) — blind
  task-specific runs, captured outcomes and measurable regression checks; fixture outcomes do not
  establish hardware reliability or cross-model performance.
- [Google Engineering Practices: The Standard of Code
  Review](https://google.github.io/eng-practices/review/reviewer/standard.html) — evidence over
  preference, forward progress, and avoiding perfection-driven review loops.

All six linked repositories were published under the MIT License when this synthesis was prepared.
Their licenses permit use and modification subject to their terms. This skill paraphrases concepts
rather than bundling upstream skill files, templates, or examples. Before redistributing a
materially modified version, re-check upstream license state and retain required attribution for any
copied or substantially adapted content.

## Deliberate departures

- Do not assume the newest iOS or Swift release. Repository settings and supported deployment
  targets are authoritative.
- Do not make SwiftData, SwiftUI, Observation, structured concurrency, or Swift Testing mandatory
  when safe legacy technology is established.
- Do not enforce one-type-per-file, fixed file/line-size limits, MV vs. MVVM preferences, or
  modernization as merge blockers.
- Do not translate generic web/JavaScript review checks into irrelevant iOS findings.
- Do not confuse per-finding reviewer certainty with this skill's overall PR merge-confidence score.
- Broader senior-engineer coverage is conditional review guidance, not a competency checklist or new
  merge threshold. Specialist lenses do not prescribe architecture/frameworks, universal device
  testing, or unavailable platform adoption. Operational signing/release/authentication actions
  still require the relevant authorization.
