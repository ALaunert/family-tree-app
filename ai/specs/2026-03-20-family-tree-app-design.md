# Family Tree App Design

Date: 2026-03-20
Status: Approved for planning

## Summary

This project is a private, Docker-contained web application for digitizing a paper ancestry tree into a visual family tree. The primary user experience is a login-protected tree view for visitors. Moderators use the same tree-first interface, with additional editing tools for maintaining person records and relationships.

The project must be self-contained inside its own project directory under `~/projects/family-tree-app`. That directory should include source code, Docker configuration, operational tooling, documentation, and AI-generated project artifacts such as specs and plans.

## Goals

- Digitize a paper family tree into a private web app
- Make the visual tree the main experience for normal viewers
- Allow trusted moderators to add and edit people and relationships
- Keep development and deployment containerized with Docker
- Keep project artifacts, including specs and plans, inside the project directory
- Prepare the project for later deployment to the user's own server

## Non-Goals for the First Increment

- Bulk imports such as CSV or GEDCOM
- Public access without login
- Open self-signup
- Rich genealogy workflows with uncertain dates, event timelines, or document attachments
- Mandatory photo support

## Product Scope

### Users and access

- Development use is single-user
- Deployed use is private and login-protected
- View access is limited to logged-in family members or invited users
- Moderator accounts are created only by the owner
- A small trusted editor group is supported after deployment

### Data scale

- Initial expected scale is under 100 people
- Manual data entry is the only required input path in v1

## Experience Design

### Viewer experience

- Users log in and land on the visual family tree
- The tree supports pan, zoom, and person selection
- Selecting a person opens their details and relationship context
- The tree is the main product surface for visitors

### Moderator experience

- Moderators use the same tree-first interface
- Moderator-only controls allow editing person records and relationships
- Adding and editing should be form-driven, not graph-only
- Search or quick-jump should help moderators locate people efficiently

## Architecture

The first version should use one web application with role-aware behavior rather than separate viewer and admin applications.

Core components:

- Frontend web app for tree browsing, person details, and moderator actions
- Backend API for authentication, permissions, people, and relationships
- Relational database for accounts, people, and family links

This architecture is preferred over a records-first UI because the tree is the primary experience, and preferred over a graph-database design because the current data scale and relationship complexity do not justify the extra system weight.

## Data Model

### Person

Each person record should support:

- Full name
- Optional birth date
- Optional death date
- Short notes or description
- Metadata needed for display and editing
- Future optional photo support

### Relationship

Relationships should be stored explicitly instead of hard-coding family fields on the person record.

Required relationship types for v1:

- Parent-child
- Partner/spouse

This model allows sibling relationships to be inferred through shared parents and keeps the schema flexible enough for future extensions.

## UI Surfaces

The first version should include three main surfaces in one application:

1. Login-protected tree view
2. Person details panel or page
3. Moderator editing flow for adding people and linking relationships

The default landing page for all users is the tree view.

## Security and Permissions

- Full tree access requires login
- Viewer users are read-only
- Moderator users can create and update people and relationships
- Only the owner creates accounts in the first deployed version

The design should assume living family data may be present and therefore should not expose the tree publicly.

## Deployment Model

- Local development runs in Docker
- Server deployment runs in Docker
- The container structure should stay as similar as possible between development and deployment
- Environment-specific values should vary by configuration, not by architecture

## Project Structure

The project directory should contain both runtime assets and planning artifacts.

Expected top-level concerns:

- Application source code
- Docker configuration
- Environment templates
- Documentation
- `ai/` directory for specs, plans, and design artifacts
- `Makefile` as the operator entry point

The `Makefile` should remain thin and wrap common workflows such as setup, local development, logs, tests, and later deployment.

## Error Handling

The first version should include:

- Validation for required fields
- Validation for invalid relationship operations
- Clear permission errors for unauthorized actions
- Empty states for an empty tree or missing relationships
- Safe handling when records change or disappear during viewing

## Testing Strategy

The initial test strategy should focus on:

- API tests for auth, people CRUD, and relationship rules
- Database-level integrity checks for relationship validity
- UI tests for login, tree loading, person selection, and moderator edits
- A container-based smoke test covering startup through the `Makefile`

## Bootstrap Requirements

The first implementation plan should include repository bootstrap tasks:

- Create the self-contained project directory at `~/projects/family-tree-app`
- Initialize git
- Prepare the public GitHub repository `family-tree-app`
- Add Docker scaffolding
- Add the `Makefile`
- Establish the `ai/` planning area from the start

## Open Decisions Deferred to Planning

- Exact frontend and backend framework choices
- Exact relational schema details
- Exact tree rendering library and layout strategy
- Authentication implementation details
- Concrete Docker service breakdown

These should be decided in the implementation plan, while staying within the approved product and architectural boundaries above.
