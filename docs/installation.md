# Installation

## 1. Check prerequisites

Install Git, Node.js 22.20.0 or newer, and a coding agent that supports skills. The tested installer is `skills@1.7.0`; future CLI releases may have different requirements.

```sh
git --version
node --version
npm --version
```

The [Skills CLI](https://github.com/vercel-labs/skills) downloads this public repository. It does not install the agent itself. Review the CLI's prompts before replacing an existing skill with the same name.

## 2. Choose your scope

For one project, run from that project's root:

```sh
npx skills add ImtiazDipto01/ios-ultrareview --skill ios-ultrareview --agent codex --yes
```

For every project, add `--global`:

```sh
npx skills add ImtiazDipto01/ios-ultrareview --skill ios-ultrareview --agent codex --global --yes
```

Use `--agent claude-code` for Claude Code, `--agent cursor` for Cursor, or `--agent codex claude-code cursor` for all three. Omit `--agent` and `--yes` for interactive agent selection. Other agents supported by the installer can select this standard skill too; installation support does not establish identical review behavior.

The CLI can use shared files and symlinks. Add `--copy` if you need independent copies.

| Agent | Project scope in the tested CLI | Global scope in the tested CLI |
| --- | --- | --- |
| Codex | `.agents/skills/ios-ultrareview` | `~/.codex/skills/ios-ultrareview` |
| Claude Code | `.claude/skills/ios-ultrareview` | `~/.claude/skills/ios-ultrareview` |
| Cursor | `.agents/skills/ios-ultrareview` | `~/.cursor/skills/ios-ultrareview` |

These are CLI destinations. Current [Codex documentation](https://developers.openai.com/codex/skills) also documents `~/.agents/skills` for user-scoped discovery. For maximum portability with a new host version, use project scope or its documented manual location. [Claude Code](https://code.claude.com/docs/en/skills) and [Cursor](https://cursor.com/docs/context/skills) document their own discovery rules.

## 3. Verify and use

```sh
npx skills list
```

Open a fresh agent session if the skill does not appear. Select it and provide a PR URL or exact base/head refs. In Codex, mention `$ios-ultrareview`; in Claude Code, use `/ios-ultrareview`; in Cursor, select the skill or ask the agent to use it.

## Pin a release

For a reproducible installation, pin both the tested CLI and the repository tag:

```sh
npx skills@1.7.0 add https://github.com/ImtiazDipto01/ios-ultrareview/tree/v1.0.1/skills/ios-ultrareview --skill ios-ultrareview --agent codex --yes
```

Use the unpinned repository command to follow the default branch. A pinned release intentionally stays on that release until you install a newer source.

## Manual installation

```sh
git clone https://github.com/ImtiazDipto01/ios-ultrareview.git
```

Copy the **entire** `skills/ios-ultrareview` folder into the agent's documented skill directory. For example, create `.agents/skills` in your project and copy the folder there for Codex. For Claude Code, use `.claude/skills`. Avoid overwriting a different local revision without keeping a copy.

For an agent without native discovery, give it access to the entire folder and ask it to read `SKILL.md` and the relevant references. A chat window without terminal/filesystem access cannot run `npx`; use a host-supported skill upload or integration instead. Codex and Claude Code are separate products.

## Update or remove

Re-run the installation command for this skill and your chosen agent/scope to install the current source. To remove it:

```sh
npx skills remove ios-ultrareview --agent codex
```

Add `--global` if you installed globally. Check [CLI documentation](https://github.com/vercel-labs/skills) for its update and removal behavior in your installed version.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `npx` is missing or reports an unsupported engine | Install a supported Node.js version. |
| Skill is installed but invisible | Confirm project/global scope and the agent's documented discovery directory; open a fresh session. |
| Duplicate entries | Inspect project and user installs; retain the version you intend to invoke. |
| Links do not work on your filesystem | Install with `--copy`. |
| Repository fetch fails | Check Git/network access; use the manual clone when available. |
| Review cannot run Xcode | Supply qualifying exact-target build/test evidence or keep the validation gate open. Installation alone supplies no execution evidence. |
