# Target acquisition, materialization, and cleanup

Read this reference when starting from a PR URL, local refs, supplied artifacts, or an ordinary checkout. It owns target identity, access fallbacks, materialization trust, isolation, and cleanup. [context-and-workflow.md](context-and-workflow.md) owns execution trust and validation evidence.

## Authorization and access

A review request authorizes read-only retrieval and review-owned temporary clones, worktrees, and build-output directories needed for inspection and validation. Host permissions still apply. It does not authorize source edits, commits, pushes, merges, authentication changes, credential collection, or provider writes.

Use existing credentials without printing them. For missing private access, ask the user to connect/authenticate the provider or supply a checkout/bundle; never request a token in chat.

Identify the provider, then use available native connectors, authenticated CLI/documented APIs plus Git, public APIs/advertised PR refs, or user-supplied checkout/bundle/exact artifacts. Missing MCP alone is not a limitation. Terminal access does not require browser permission. Request narrow host permissions when necessary; do not install tools or start interactive login solely because one route is absent.

| Acquisition state | Minimum evidence | Allowed result |
|---|---|---|
| **Live target ready** | Authoritative current base/head, complete behavior-relevant content, required provider state, and refreshable identity | Full live or draft review; posting requires separate authority and supported provider mechanics |
| **Snapshot ready** | Exact base/merge base/head and complete behavior-relevant content; live currentness unavailable | Scored draft with a visible snapshot label; never post as a current live review |
| **Patch-only / limited inspection** | Reviewable content but exact-target or coverage prerequisites missing; limited scope requested or accepted | Preliminary findings only; no score, decision, `B`/`E` IDs, build claim, or posting |
| **Target inaccessible** | Insufficient material, or prerequisites for the requested full review cannot be acquired | `iOS UltraReview — not started: target inaccessible`; no score or decision |

**Complete behavior-relevant coverage** requires inventorying every changed path and relevant metadata, acquiring complete content for every potentially behavior-relevant delta, and inspecting it with necessary context. Identify binary, generated, or non-renderable omissions and examine their metadata and integration impact. An unknown or material omission prevents scoring. Acquired but unread material also leaves coverage incomplete: report that limitation without a score. Never silently replace a requested full review with limited inspection.

Provider discussions/checks can limit evidence. Never substitute a default branch, similarly named branch, or stale clone for the requested target. Acquisition is provider-neutral; external submission uses only write mechanics supported by this skill and the available tool.

## Freeze identity before choosing an environment

For a live PR resolve repository, PR/MR number, base ref/SHA, current head SHA, merge base, and provider merge-result SHA when available. Capture author/fork status, authenticated actor/capability, draft/mergeability, changed-file/commit counts, checks and tested SHAs, prior decisions, comments, and unresolved threads. For a requested local/historical review, resolve supplied base/head refs to immutable commit IDs and compute the merge base. Do not guess a comparison base. Record exact identities and unavailable metadata/refresh.

When a local repository exists, inspect root, remotes, branch/HEAD, working-tree and in-progress-operation status, and worktree ownership. Suppress configured helpers even during initial inspection: for example, use `git --no-optional-locks -c core.fsmonitor=false status --porcelain` so status cannot invoke a repository-configured fsmonitor. Record initial branch, SHA, and status for the final preservation check. Fetch objects without pulling, switching the ordinary checkout, or force-updating developer branches.

### Read-only local snapshots

A committed-ref review may inspect pinned Git objects directly from an ordinary checkout; no worktree is required for static review. Use object reads such as `rev-parse`, `merge-base`, `ls-tree`, and `show <sha>:<path>`, plus complete merge-base-to-head diffs. Disable pagers, external diff helpers, and textconv for these reads, so inspection does not execute repository-configured helpers. Resolve ref arguments safely and use their recorded immutable IDs thereafter.

This path also works for an exact acquired remote target when its objects and necessary context are available. The acquisition state depends on identity/currentness and content, not whether files were checked out. Inspect repository instructions at the pinned target. Successful qualifying CI or other exact-target evidence may support a score; object inspection does not imply a build or test pass.

Dirty and untracked ordinary-checkout files are outside a committed snapshot. Name that exclusion and leave them untouched. Never silently combine HEAD, index, working files, or another task's output. If the user requests uncommitted changes, use a limited no-score inspection unless coherent immutable base/head artifacts covering the intended inputs have been acquired under that scope. Do not create commits, stash, reset, or clean to manufacture a snapshot. Move to an owned isolated environment before executing checks.

## Materialize only when needed

**Before any checkout or worktree creation**, inspect effective Git hooks/filter configuration and target `.gitattributes`, `.gitmodules`, dependency manifests, and executable infrastructure from objects. Suppress automatic LFS materialization and recursive submodule initialization. If hooks, smudge/process filters, LFS, submodules, or other materialization cannot be trusted, stay object-only or use trusted secrets-free CI. The later execution gate does not replace this preflight.

With no local repository, create a unique OS temporary review root and clone/fetch without checkout through authorized access. Do not populate or later delete the user's arbitrary starting folder. After preflight, materialize a detached head checkout; acquire base/merge-result objects separately.

Reuse an existing checkout only if it is a clean dedicated agent-managed review worktree, already at the exact head, with no merge/rebase/cherry-pick/revert/bisect in progress and no conflicting owner or active process. Otherwise create a review-owned detached worktree at the immutable head outside the ordinary checkout. Branch-name equality is insufficient. Never resolve packages, initialize submodules, build, test, stash, clean, reset, or merge in the ordinary checkout.

### Exact-target execution records

Before executing code, apply the [execution trust gate](context-and-workflow.md#execution-trust-gate). Worktree separation protects checkout state, not secrets. Do not copy ignored credentials automatically.

In the selected environment:

1. verify remote/root, clean status, exact HEAD, base/head objects, and complete merge-base-to-head diff;
2. record pre-validation HEAD, index/tracked state, untracked/ignored paths, and submodule commits;
3. use uniquely owned DerivedData, results/logs, SwiftPM scratch and package directories outside both ordinary checkout and worktree where tools support it;
4. after each run reverify HEAD, tracked/index state, submodules, and understood generated inputs. Unexpected mutation invalidates exact-SHA evidence; and
5. preserve command/job, target SHA, scheme/configuration/destination or equivalent scope, relevant tests, exit status, generated-input provenance, and results.

Another branch or earlier commit never qualifies. For a merge-result run, prove it contains recorded head and current base; use a separate clean detached environment or authoritative CI.

Refresh target components at review completion and immediately before an authorized live write. If refresh is unavailable, label the result snapshot and do not post as current. If head changes, reacquire the immutable target and use a fresh environment for any execution. Mark earlier evidence stale and reassess affected content/anchors/checks; never reset an old worktree or transplant its score. If only base or merge result changes, recompute the comparison and rerun affected merge-result validation.

## Cleanup

Track every process and clone/worktree/build/temp path created by this review, including baseline state and disposable outputs. Preserve evidence before cleanup after success, failure, or abort and resolve any authorized submission attempt first.

1. Wait for or stop only review-started processes; never terminate by broad name. Foreign processes using a target require retention and a reported reason.
2. Move outside removal targets. Canonicalize each path and confirm it is the recorded session-owned path, never the user's checkout/root/home/starting folder or a reused/pre-existing worktree.
3. Recheck expected SHA and tracked, untracked, ignored, generated, and submodule state against baseline. Remove only understood disposable paths created this session and absent at baseline. Preserve unexplained state; never manufacture cleanliness with `clean`, `reset`, or `stash`.
4. Remove a clean linked worktree with `git worktree remove -- <exact-path>` without force. Remove a standalone clone only through its canonical session root after the same checks. Then remove explicitly tracked build/temp outputs.
5. Do not broadly prune worktrees or recursively delete unresolved paths. Verify deregistration, owned-artifact removal, and unchanged ordinary-checkout branch/SHA/status.
6. Report cleanup success locally, or exact retained paths and reasons. Keep local paths out of provider reviews unless needed to explain evidence.

Never remove a reused/pre-existing checkout or force-remove dirty state. Honor a user's request to retain the environment and report its path.
