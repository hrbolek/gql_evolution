# AGENTS.md

## Purpose

This repository is an educational GraphQL federation subgraph.

The project demonstrates an architecture that is intentionally close to
a real deployable application while remaining understandable and
modifiable by students.

Changes should preserve this architectural intent.

---

## Architecture

The main dependency direction is:

GraphQL
→ Service
→ DataLoader / persistence layer
→ SQLAlchemy
→ Database

The important source areas are:

- `src/DBDefinitions/`
  - SQLAlchemy models
  - database runtime
  - persistence-related definitions

- `src/Dataloaders/`
  - data loading and persistence helpers
  - batching/caching where applicable

- `src/ServiceDefinitions/`
  - application and domain services
  - business operations
  - reusable application logic

- `src/GraphTypeDefinitions/`
  - Strawberry GraphQL types
  - GraphQL resolvers
  - GraphQL context
  - schema and federation-related definitions

- `src/AgentDefinitions/`
  - runtime application agents
  - PydanticAI tools
  - agent-facing GraphQL functionality

- `.CoderDefinitions/`
  - development-only coding agent
  - not part of the runtime application

---

## Dependency Rules

Respect the architectural dependency direction.

GraphQL code may depend on Services.

Services may depend on DataLoaders and database abstractions.

Database and DataLoader code must not depend on GraphQL.

Avoid introducing reverse dependencies.

In particular:

- GraphQL resolvers must not access SQLAlchemy directly.
- Runtime PydanticAI tools must not access SQLAlchemy directly.
- Runtime agents should use the application's GraphQL API unless a task
  explicitly requires another architecture.
- Do not introduce a second parallel business-logic implementation for agents.

Prefer existing abstractions and patterns before creating new ones.

---

## GraphQL and Federation

This project represents a GraphQL federation subgraph.

When modifying GraphQL code:

- preserve existing Strawberry patterns,
- preserve federation semantics,
- preserve entity identifiers and federation keys,
- avoid breaking the public GraphQL contract without an explicit requirement,
- keep resolver logic thin,
- delegate business operations to Services.

A subgraph should remain independently runnable and testable while also being
usable as part of the larger federation.

---

## Services

Business operations belong primarily in `ServiceDefinitions`.

Before implementing a new service method:

1. inspect `BaseService`,
2. inspect similar existing domain services,
3. reuse established patterns where possible.

Do not duplicate generic CRUD behavior in individual services unless domain
behavior requires it.

Domain-specific rules belong in domain services.

---

## Database

Use the existing SQLAlchemy architecture.

Do not bypass the established persistence/DataLoader mechanisms without an
explicit reason.

When modifying database models:

- preserve existing identifier conventions,
- preserve relationship conventions,
- consider asynchronous SQLAlchemy usage,
- update corresponding tests.

Do not introduce synchronous database access into asynchronous application
paths.

---

## GraphQL Context and Transactions

The project uses GraphQL context and session lifecycle infrastructure.

Before changing request/session behavior, inspect:

- `src/GraphTypeDefinitions/GraphQLContext.py`
- `src/GraphTypeDefinitions/SessionCommitExtension.py`
- `src/ServiceDefinitions/ServiceContext.py`

Do not create arbitrary SQLAlchemy sessions inside resolvers or agent tools.

Preserve the existing transaction lifecycle unless the task explicitly changes
that architecture.

---

## Runtime Agents

`src/AgentDefinitions/` contains runtime PydanticAI functionality.

Runtime agents are application clients, not privileged database processes.

Preferred flow:

PydanticAI tool
→ GraphQL operation
→ GraphQL authorization
→ Service
→ DataLoader / persistence
→ Database

Agent tools should expose meaningful application capabilities rather than
unrestricted database CRUD.

Examples of preferred tools:

- `find_events`
- `get_event`
- `create_event`
- `invite_user`

Prefer these over a generic tool such as:

- `execute_sql`
- `crud(entity, operation, values)`
- unrestricted GraphQL execution

unless unrestricted access is explicitly part of the exercise.

---

## Agent Identity and Security

Never allow the language model to choose or fabricate the authenticated
identity.

Identity, credentials, effective-user information, delegation tokens and
authorization context must come from trusted runtime dependencies.

Do not expose secrets as tool arguments.

Do not log API keys, authentication tokens or other credentials.

Agent permissions must never exceed the permissions delegated by the
authenticated user.

Future impersonation/delegation mechanisms should distinguish between:

- authenticated actor,
- effective user,
- agent identity,
- delegation scope.

---

## Coding Agent

`.CoderDefinitions/` contains development infrastructure for the coding agent.

The coding agent may inspect and modify the repository in order to complete
explicit development tasks.

Normally it may modify:

- `src/`
- `tests/`
- documentation related to the requested task

It should not modify the following unless explicitly requested:

- `.CoderDefinitions/`
- `.devcontainer/`
- CI/CD configuration
- credentials or environment-secret files

Never expose or print:

- `AI_API_KEY`
- OpenAI API keys
- LiteLLM keys
- authentication tokens
- other secrets from the environment

Do not commit secret files.

---

## Coding Workflow

Before changing code:

1. inspect the relevant repository structure,
2. read relevant implementation files,
3. read existing tests,
4. identify the existing architectural pattern,
5. prefer a minimal compatible change.

After changing code:

1. run the most relevant tests,
2. fix failures caused by the change,
3. run broader tests when appropriate,
4. run linting/type checking if configured,
5. inspect `git diff`,
6. summarize the changes and remaining issues.

Do not claim that tests passed unless they were actually executed.

Do not delete, disable or weaken tests merely to obtain a passing test suite.

---

## Testing

Tests are organized primarily by architectural layer:

- `tests/db/`
- `tests/services/`
- `tests/graphql/`

When modifying a layer, start with its corresponding tests.

Typical command:

```bash
pytest
```

For focused work prefer targeted tests first, for example:

```bash
pytest tests/services
pytest tests/graphql
pytest tests/db
```

Run the complete test suite before considering a larger architectural change
finished when practical.

---

## Educational Intent

This is an educational repository.

Code should demonstrate architecture clearly.

Prefer:

- explicit code,
- understandable abstractions,
- strong typing,
- small focused components,
- testable behavior,
- patterns that students can reuse in derived subgraph projects.

Avoid unnecessary framework magic or abstractions whose complexity exceeds
their educational benefit.

When multiple implementations are possible, prefer the implementation that
best demonstrates the architectural principle being taught.

---

## Derived Projects

This repository may serve as a basis for derived student subgraph projects.

Changes to shared patterns should therefore consider whether they can be
reused consistently in derived repositories.

A derived subgraph should ideally remain:

1. independently runnable,
2. independently testable,
3. independently accessible through GraphQL,
4. usable by a runtime agent,
5. composable into the GraphQL federation,
6. suitable as an isolated workspace for a coding agent.
