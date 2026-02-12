# Contributing to LankaCommerce Cloud (LCC)

Thanks for taking the time to contribute! 🎉

This project is being built via an AI-agent-driven document series, but human contributions (code, docs, testing, review) are extremely valuable.

## Code of Conduct

Please read and follow `CODE_OF_CONDUCT.md`. By participating, you agree to uphold these standards.

## Ways to contribute

- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests
- Help with translations and UX language quality (Sinhala / Tamil / Singlish)

## Development setup (local)

> The full monorepo scaffolding (backend/frontend/docker) is implemented in subsequent Phase-01 tasks.

For now, you can:
1. Fork the repository
2. Clone your fork
3. Create a branch for your change

When the stack is available, this section will include:
- Docker Compose startup
- Environment variable setup
- Running backend/frontend tests

## Coding standards

### Python
- Follow PEP 8
- Formatting: Black (target line length 88)
- Prefer type hints where practical

### TypeScript / JavaScript
- Linting: ESLint
- Formatting: Prettier
- Keep components small and testable

### Commit messages (Conventional Commits)

Format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation only
- `style`: formatting only
- `refactor`: code restructure (no behavior change)
- `test`: tests
- `chore`: maintenance

Examples:
- `chore(repo): add editorconfig and git attributes`
- `docs(readme): add sri lanka context and quickstart`

## Branch strategy

- `main`: stable, always releasable
- `develop`: integration branch (introduced when CI/release flow is added)

Branch naming:
- Feature: `feature/<description>` (e.g., `feature/add-sinhala-search`)
- Bugfix: `fix/<description>` (e.g., `fix/cart-calculation-error`)
- Hotfix: `hotfix/<description>` (e.g., `hotfix/payment-timeout`)
- Release: `release/<version>` (e.g., `release/1.2.0`)

## Pull request process

1. Create a focused branch
2. Keep changes small and scoped
3. Add/update tests where applicable
4. Update docs when behavior changes
5. Ensure lint + tests pass
6. Open a PR with a clear description and screenshots where relevant

Reviewers typically look for:
- Correctness and safety (multi-tenant boundaries!)
- Clear naming and structure
- Tests for business-critical flows
- Minimal breaking changes

## Reporting issues

- Bugs: include steps to reproduce, expected vs actual behavior, logs
- Features: describe problem, proposed solution, alternatives

### Security issues

Please do **not** open public issues for security vulnerabilities.
Instead, report privately to: `security@lankacommerce.lk` (placeholder)
