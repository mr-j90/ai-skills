# Linear Issue Creator — Examples

## Example 1: Simple bug report

**User input**: "The login page throws a 500 when you use an email with a plus sign. Team: Engineering, Project: Auth"

**Generated issue**:
- **Title**: Fix 500 error on login when email contains plus sign
- **Labels**: bug, backend, auth
- **Size**: S (1 pt) — single input validation fix, known root cause
- **Priority**: 2 (High) — customer-facing auth flow
- **Description**:
```md
## Context
The login page returns a 500 error when a user enters an email containing a `+` character (e.g., `user+tag@example.com`). This blocks affected users from signing in.

## Acceptance Criteria
- [ ] Emails with `+` characters are accepted by the login endpoint
- [ ] Existing users with `+` in their email can sign in successfully
- [ ] Add regression test for special character emails

## Notes
- Estimate: S — likely an input sanitization or URL encoding fix in a single handler
```

---

## Example 2: Feature request

**User input**: "We need to add CSV export to the admin reports dashboard. Should support filtering by date range and report type."

**Generated issue**:
- **Title**: Add CSV export with date range and report type filters to admin dashboard
- **Labels**: feature, frontend, backend
- **Size**: L (5 pts) — touches UI, API, and data layer; needs export logic + filtering
- **Priority**: 3 (Normal)
- **Description**:
```md
## Context
Admin users need the ability to export report data as CSV files from the reports dashboard. The export should respect the currently applied date range and report type filters.

## Acceptance Criteria
- [ ] "Export CSV" button visible on admin reports dashboard
- [ ] Export respects active date range filter
- [ ] Export respects active report type filter
- [ ] CSV includes headers matching table columns
- [ ] Large exports (>10k rows) handled gracefully (streaming or background job)

## Notes
- Estimate: L — requires new API endpoint for export, UI button + loading state, and potentially background job for large datasets
- Consider: should this be async with email delivery for very large exports?
```

---

## Example 3: Infra / DevOps task

**User input**: "Migrate the staging environment from App Service to Azure Container Apps. Need to handle env vars, managed identity, and update the pipeline. This is a big one."

**Generated issue**:
- **Title**: Migrate staging environment from App Service to Azure Container Apps
- **Labels**: devops, infra, tech-debt
- **Size**: XL (8 pts) — multi-service migration, pipeline changes, identity config, risk of downtime
- **Priority**: 3 (Normal)
- **Description**:
```md
## Context
Migrate the staging environment from Azure App Service to Azure Container Apps to align with the production architecture. This involves containerization, environment variable migration, managed identity reconfiguration, and CI/CD pipeline updates.

## Acceptance Criteria
- [ ] Staging app runs on Azure Container Apps
- [ ] All environment variables migrated and validated
- [ ] Managed identity configured with correct role assignments
- [ ] Azure DevOps pipeline updated for ACA deployment
- [ ] Health checks and ingress configured
- [ ] Staging verified end-to-end before App Service decommission

## Notes
- Estimate: XL — cross-cutting work spanning infra, identity, and CI/CD with rollback risk
- Coordinate with DevOps team on pipeline changes
- Consider: blue-green or canary deployment for cutover
```

---

## Example 4: Multiple tasks in one message

**User input**: "I need three tickets for the API team on Project Horizon: 1) add rate limiting to the public endpoints, 2) update the Swagger docs for v2, 3) fix the broken health check on staging"

**Generated issues** (3 separate):

| # | Title | Labels | Size | Priority |
|---|-------|--------|------|----------|
| 1 | Add rate limiting to public API endpoints | feature, api, backend | L (5) | Normal |
| 2 | Update Swagger documentation for API v2 | documentation, api | M (3) | Normal |
| 3 | Fix broken health check endpoint on staging | bug, devops, api | S (1) | High |
