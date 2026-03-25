# Deploy Reference

## Recommended Rollout Paths

### 1. Existing Local Installer

Use when:

- the user is already inside the repository
- the audience accepts a project checkout

Command:

```bash
python3 install.py
```

### 2. pipx / Standard Python Entry Point

Use when:

- the audience wants a faster global install
- Python tooling is already available
- you want a single command install without manual PATH editing

Target command shape:

```bash
pipx install git+<repo-url>
```

This path depends on `pyproject.toml` and a console script entry point.

### 3. Package Manager Distribution

Use when:

- the tool becomes stable enough for repeated external distribution
- you want the shortest onboarding path for macOS users

Target path:

- Homebrew Tap
- release artifacts or signed installers

## Guidance

- Prefer `install.py` for local development or private onboarding.
- Prefer `pipx` once the Python entry point is available.
- Mention Homebrew only as the later-stage distribution option unless it already exists.
