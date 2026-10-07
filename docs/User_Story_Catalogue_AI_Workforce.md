# USER STORY CATALOGUE
## AI Workforce — Autonomous Business Workflow Automation Platform

---

## DOCUMENT CONTROL

| Field | Details |
|---|---|
| **Document Title** | User Story Catalogue — AI Workforce Platform |
| **Document ID** | USC-AIWF-2026-001 |
| **Version** | 1.0.0 |
| **Status** | Draft |
| **Linked BRD** | BRD-AIWF-2026-001 v1.0.0 |
| **Created Date** | 2026-10-07 |

### Story Priority Legend

| Priority | Description |
|---|---|
| **P0** | Must-have — Blocking; the product cannot function without this |
| **P1** | Critical — Core value proposition; must be in MVP |
| **P2** | Important — Significant value; target for MVP or early Phase 2 |
| **P3** | Nice-to-have — Phase 2 or Phase 3 |

### Phase Legend

| Phase | Description |
|---|---|
| **MVP** | Smallest viable production product |
| **Phase 2** | Full commercial feature set |
| **Phase 3** | Enterprise-grade capabilities |

---

## EPIC INDEX

| Epic | Name | Stories |
|---|---|---|
| EPIC-01 | Authentication & Identity | US-001 – US-012 |
| EPIC-02 | Organization & Workspace Management | US-013 – US-025 |
| EPIC-03 | User & Role Management | US-026 – US-035 |
| EPIC-04 | AI Agent Management | US-036 – US-055 |
| EPIC-05 | Knowledge Management | US-056 – US-072 |
| EPIC-06 | RAG | US-073 – US-082 |
| EPIC-07 | Tools & Integrations | US-083 – US-097 |
| EPIC-08 | Workflow Builder | US-098 – US-117 |
| EPIC-09 | Agentic Orchestration | US-118 – US-128 |
| EPIC-10 | Human-in-the-Loop | US-129 – US-143 |
| EPIC-11 | Guardrails & Governance | US-144 – US-155 |
| EPIC-12 | Workflow Execution | US-156 – US-172 |
| EPIC-13 | Monitoring & Observability | US-173 – US-185 |
| EPIC-14 | AI Evaluation | US-186 – US-197 |
| EPIC-15 | Analytics | US-198 – US-208 |
| EPIC-16 | Administration | US-209 – US-220 |
| EPIC-17 | API & Developer Platform | US-221 – US-232 |
| EPIC-18 | Security & Audit | US-233 – US-244 |
| EPIC-19 | Notifications | US-245 – US-253 |
| EPIC-20 | Billing / Usage / Plan Readiness | US-254 – US-263 |
| EPIC-21 | System Reliability | US-264 – US-272 |
| EPIC-22 | Platform Extensibility | US-273 – US-281 |

---

## EPIC 1 — AUTHENTICATION & IDENTITY

---

### US-001: User Self-Registration

| Field | Details |
|---|---|
| **Story ID** | US-001 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | User Registration |
| **User Role** | Prospective User (unauthenticated) |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a prospective user,
> I want to register an account using my email and a password,
> so that I can access the AI Workforce platform and create or join an organization.

**Business Value:** Enables self-service onboarding, reducing sales friction and enabling growth.

**Preconditions:**
- User is not authenticated
- User has a valid, accessible email address

**Main Flow:**
1. User navigates to the registration page
2. User enters: first name, last name, email address, password
3. System validates all fields (format, strength, uniqueness of email)
4. System creates the user account in an unverified state
5. System sends an email verification link to the provided email
6. System informs the user to check their email before continuing

**Alternate Flow:**
- AF-1: Email already registered → System displays a message that the email is already in use, suggests logging in or resetting password

**Exception Flow:**
- EF-1: Email verification service is unavailable → System creates the account and queues the verification email; user is informed of the delay
- EF-2: User submits form with network interruption → Form state is preserved; user can resubmit

**Acceptance Criteria:**
- **Given** a user provides a valid email and strong password, **When** they submit the registration form, **Then** an account is created, a verification email is sent, and the user is shown a "check your email" message
- **Given** the email is already registered, **When** the user submits the form, **Then** an error message is shown (no information about whether the email exists for security — instead: "If this email is not registered, you'll receive a confirmation email")
- **Given** the password does not meet strength requirements, **When** the user submits, **Then** specific validation errors are displayed inline
- **Given** a registered account is unverified after 24 hours, **When** the user attempts to log in, **Then** they are prompted to resend the verification email

**Validation Rules:**
- Email: valid format, maximum 255 characters
- Password: minimum 12 characters, must contain uppercase, lowercase, number, and special character
- First name, last name: required, 1–100 characters

**Permission Requirements:** None (public endpoint)

**Security Considerations:**
- Rate limit registration endpoint to prevent abuse
- Never confirm or deny whether an email is registered (prevent enumeration)
- Log registration events for security monitoring

**Audit Requirements:** Registration event logged with timestamp, IP address, and outcome

**Dependencies:** Email delivery service, IAM service

---

### US-002: Email Verification

| Field | Details |
|---|---|
| **Story ID** | US-002 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Email Verification |
| **User Role** | Registered User (unverified) |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a newly registered user,
> I want to verify my email address by clicking the link sent to my inbox,
> so that I can confirm my identity and gain access to the platform.

**Business Value:** Ensures users control the email address they register with; reduces fraud and fake accounts.

**Preconditions:**
- User has registered but not yet verified their email
- A verification email has been sent

**Main Flow:**
1. User receives verification email with a unique link
2. User clicks the link
3. System validates the token (not expired, not already used, matches user)
4. System marks the user's email as verified
5. System logs the user in and redirects them to the organization creation/join flow

**Alternate Flow:**
- AF-1: User has lost the email → User can request a new verification email from the login prompt

**Exception Flow:**
- EF-1: Verification link has expired (>24 hours) → System shows an error and offers to resend; the old token is invalidated
- EF-2: Verification link has already been used → System shows a message that the email is already verified; prompts login

**Acceptance Criteria:**
- **Given** a valid, unexpired verification link, **When** clicked, **Then** the user's email is verified and they are logged in
- **Given** an expired link, **When** clicked, **Then** an expiry error is shown and a "resend verification" option is offered
- **Given** an already-used link, **When** clicked, **Then** a message confirms verification is complete and offers login
- **Given** the user requests a new verification email, **When** submitted, **Then** a new token is generated, the old token is invalidated, and a new email is sent

**Validation Rules:** Verification token must be single-use, unique, cryptographically secure, and expire after 24 hours

**Permission Requirements:** None (token-based access)

**Security Considerations:** Tokens must be cryptographically random; verification links must use HTTPS; tokens invalidated immediately after use

**Audit Requirements:** Email verification event logged with timestamp and IP address

**Dependencies:** US-001, Email delivery service

---

### US-003: User Login

| Field | Details |
|---|---|
| **Story ID** | US-003 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Authentication |
| **User Role** | Registered, Verified User |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a registered and verified user,
> I want to log in with my email and password,
> so that I can access the platform and my organizations.

**Business Value:** Core access mechanism for all platform functionality.

**Preconditions:**
- User account exists and email is verified
- Account is not locked or deactivated

**Main Flow:**
1. User enters email and password on the login page
2. System validates credentials
3. If MFA is enabled, system prompts for MFA code
4. System validates MFA code
5. System issues a secure session (access token + refresh token)
6. User is redirected to their default organization or organization selector

**Alternate Flow:**
- AF-1: MFA not enabled → Steps 3 and 4 are skipped; session is issued after credential validation

**Exception Flow:**
- EF-1: Invalid credentials → System displays a generic error ("Email or password is incorrect") without revealing which is wrong; increments failed attempt counter
- EF-2: Account locked (too many failed attempts) → System displays a lockout message and sends an unlock/reset email
- EF-3: Account deactivated → System displays a deactivation message and support contact
- EF-4: Email not verified → System displays a prompt to verify email

**Acceptance Criteria:**
- **Given** valid credentials, **When** the user logs in, **Then** a secure session is created and the user is redirected to the platform
- **Given** invalid credentials, **When** submitted, **Then** a generic error is shown and attempt counter increments
- **Given** 5 consecutive failed login attempts, **When** the sixth attempt occurs, **Then** the account is temporarily locked and the user is notified
- **Given** MFA is enabled, **When** credentials are valid, **Then** an MFA prompt is presented before granting access

**Validation Rules:**
- Email: valid format
- Password: required, not empty

**Permission Requirements:** None (public endpoint)

**Security Considerations:**
- Brute-force protection via lockout after N failed attempts (configurable, default 5)
- Rate limiting on login endpoint
- No indication of which credential field is incorrect
- Session tokens must be HttpOnly, Secure cookies or JWTs with short expiry

**Audit Requirements:** Login success and failure events logged with timestamp, IP address, user agent

**Dependencies:** US-001, US-002, MFA setup (US-005)

---

### US-004: User Logout

| Field | Details |
|---|---|
| **Story ID** | US-004 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Session Management |
| **User Role** | Authenticated User |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an authenticated user,
> I want to log out of the platform,
> so that my session is terminated and my account is protected on shared devices.

**Business Value:** Prevents unauthorized access on shared or public devices.

**Preconditions:** User is logged in with an active session

**Main Flow:**
1. User clicks "Log Out"
2. System invalidates the current session tokens (access + refresh)
3. System clears all session cookies
4. User is redirected to the login page

**Alternate Flow:**
- AF-1: User logs out from all sessions → All refresh tokens for the user are invalidated across all devices

**Acceptance Criteria:**
- **Given** a logged-in user, **When** they click logout, **Then** the session is invalidated and they are redirected to login
- **Given** a user logs out from all sessions, **When** confirmed, **Then** all active sessions are terminated immediately
- **Given** an invalidated session token is used, **When** submitted to the API, **Then** a 401 Unauthorized response is returned

**Security Considerations:** Server-side session invalidation must be enforced; client-side token deletion alone is insufficient

**Audit Requirements:** Logout event logged with timestamp and session identifier

**Dependencies:** US-003

---

### US-005: Multi-Factor Authentication (MFA) Setup

| Field | Details |
|---|---|
| **Story ID** | US-005 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | MFA |
| **User Role** | Authenticated User |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an authenticated user,
> I want to enable multi-factor authentication using an authenticator app,
> so that my account is protected even if my password is compromised.

**Business Value:** Significantly reduces account takeover risk; enterprise customers require MFA.

**Preconditions:** User is logged in; MFA not yet enabled

**Main Flow:**
1. User navigates to Security Settings
2. User selects "Enable MFA"
3. System generates a TOTP secret and displays a QR code
4. User scans the QR code with an authenticator app
5. User enters the generated TOTP code to confirm setup
6. System validates the code and marks MFA as enabled
7. System displays backup codes; user is instructed to save them

**Alternate Flow:**
- AF-1: User disables MFA → User must confirm with password and current MFA code before disabling

**Exception Flow:**
- EF-1: Invalid TOTP code during setup → Error displayed; user can retry; code not committed until valid confirmation

**Acceptance Criteria:**
- **Given** a user enables MFA and scans the QR code, **When** they enter a valid TOTP code, **Then** MFA is activated and backup codes are displayed
- **Given** MFA is enabled, **When** the user logs in with valid credentials, **Then** they must provide a valid TOTP code to proceed
- **Given** an invalid TOTP code at login, **When** submitted, **Then** an error is shown and access is denied
- **Given** a user uses a backup code to log in, **When** the code is valid, **Then** they are granted access and the backup code is consumed

**Security Considerations:** TOTP secret must be stored encrypted; backup codes must be hashed; display them only once

**Audit Requirements:** MFA enable/disable events logged

**Dependencies:** US-003

---

### US-006: Password Reset

| Field | Details |
|---|---|
| **Story ID** | US-006 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Password Management |
| **User Role** | User (authenticated or unauthenticated) |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a user who has forgotten my password,
> I want to request a password reset email,
> so that I can regain access to my account.

**Business Value:** Reduces support burden; enables self-service account recovery.

**Preconditions:** User has a registered account with a verified email

**Main Flow:**
1. User navigates to "Forgot Password" on the login page
2. User enters their email address
3. System displays a generic success message regardless of whether the email exists
4. If the email exists, system sends a password reset email with a time-limited link
5. User clicks the link and is taken to the password reset form
6. User enters a new password (confirmed twice)
7. System validates and updates the password; invalidates all existing sessions
8. User is redirected to login

**Exception Flow:**
- EF-1: Reset link expired (>1 hour) → Error displayed; user is offered a new reset request
- EF-2: Reset link already used → Error displayed; access denied

**Acceptance Criteria:**
- **Given** a user submits a password reset request for a registered email, **When** submitted, **Then** a reset email is sent and a generic success message is shown
- **Given** a valid, unexpired reset link, **When** the user sets a new password meeting strength requirements, **Then** the password is updated and all sessions are invalidated
- **Given** an expired reset link, **When** clicked, **Then** an expiry error is shown
- **Given** the new password matches a recent password in history, **When** submitted, **Then** an error is displayed and the reset is rejected

**Security Considerations:** Prevent email enumeration (always show generic response); single-use tokens; all sessions invalidated on reset

**Audit Requirements:** Password reset request and completion events logged

**Dependencies:** US-001, Email delivery service

---

### US-007: Session Management — Idle Timeout

| Field | Details |
|---|---|
| **Story ID** | US-007 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Session Management |
| **User Role** | Authenticated User |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a platform administrator,
> I want sessions to automatically expire after a period of inactivity,
> so that idle sessions do not pose a security risk.

**Business Value:** Reduces the risk of unauthorized access from unattended sessions.

**Acceptance Criteria:**
- **Given** a session is idle for the configured timeout period, **When** the timeout expires, **Then** the session is invalidated and the user is redirected to login
- **Given** a user is active within the timeout window, **When** the timeout would have expired, **Then** the session is refreshed silently
- **Given** an organization has configured a custom session timeout, **When** members log in, **Then** their sessions respect the organization-configured timeout

**Priority:** P1 | **Phase:** MVP

---

### US-008: View Active Sessions

| Field | Details |
|---|---|
| **Story ID** | US-008 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Session Management |
| **User Role** | Authenticated User |
| **Priority** | P2 |
| **Phase** | Phase 2 |

**User Story:**
> As an authenticated user,
> I want to view all my active sessions and their details,
> so that I can identify and revoke any sessions I do not recognize.

**Acceptance Criteria:**
- **Given** a user navigates to Security Settings, **When** viewing active sessions, **Then** they see a list of sessions with: device type, location (approximate), last active time, and current session indicator
- **Given** a user identifies an unfamiliar session, **When** they revoke it, **Then** that session is immediately invalidated

**Priority:** P2 | **Phase:** Phase 2

---

### US-009: SSO Login (SAML 2.0)

| Field | Details |
|---|---|
| **Story ID** | US-009 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Enterprise SSO |
| **User Role** | Enterprise User |
| **Priority** | P3 |
| **Phase** | Phase 3 |

**User Story:**
> As an enterprise user,
> I want to log in using my organization's SSO identity provider,
> so that I can access the platform without managing a separate password.

**Acceptance Criteria:**
- **Given** an organization has configured SAML 2.0 SSO, **When** a user attempts to log in with their corporate email, **Then** they are redirected to the organization's identity provider
- **Given** successful IdP authentication, **When** the SAML assertion is received, **Then** the user is granted access with the appropriate role
- **Given** the IdP authentication fails, **When** the response is received, **Then** access is denied and an appropriate error is displayed

**Priority:** P3 | **Phase:** Phase 3

---

### US-010: Account Profile Management

| Field | Details |
|---|---|
| **Story ID** | US-010 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | User Profile |
| **User Role** | Authenticated User |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an authenticated user,
> I want to update my profile information (name, avatar, timezone),
> so that my identity is correctly represented across the platform.

**Acceptance Criteria:**
- **Given** a user updates their display name, **When** saved, **Then** the new name is reflected across all platform UI elements
- **Given** a user changes their email address, **When** submitted, **Then** a verification email is sent to the new address and the change does not take effect until verified

**Priority:** P1 | **Phase:** MVP

---

### US-011: Account Deactivation (Self)

| Field | Details |
|---|---|
| **Story ID** | US-011 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Account Lifecycle |
| **User Role** | Authenticated User |
| **Priority** | P2 |
| **Phase** | Phase 2 |

**User Story:**
> As an authenticated user,
> I want to request deletion or deactivation of my account,
> so that I can exercise my right to data control.

**Acceptance Criteria:**
- **Given** a user requests account deletion and is not the sole owner of any organization, **When** confirmed, **Then** their personal data is scheduled for deletion per retention policy and they are logged out
- **Given** a user is the sole owner of an organization, **When** they request deletion, **Then** they are blocked until they transfer or delete the organization

**Priority:** P2 | **Phase:** Phase 2

---

### US-012: Account Lockout & Unlock

| Field | Details |
|---|---|
| **Story ID** | US-012 |
| **Epic** | EPIC-01 — Authentication & Identity |
| **Feature** | Security |
| **User Role** | Authenticated User / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a user whose account has been locked due to too many failed login attempts,
> I want to receive an email with an unlock or password reset link,
> so that I can regain access to my account securely.

**Acceptance Criteria:**
- **Given** an account is locked, **When** the user submits a login attempt, **Then** a lockout message is displayed and an unlock email is sent
- **Given** a valid unlock link, **When** clicked within the expiry window, **Then** the account is unlocked and the user is prompted to log in
- **Given** an admin manually unlocks a user account, **When** confirmed, **Then** the account lock is removed and the user can log in

**Priority:** P1 | **Phase:** MVP

---

## EPIC 2 — ORGANIZATION & WORKSPACE MANAGEMENT

---

### US-013: Create Organization

| Field | Details |
|---|---|
| **Story ID** | US-013 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Organization Creation |
| **User Role** | Authenticated Verified User |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a verified user,
> I want to create a new organization on the platform,
> so that I can set up an isolated workspace for my company's AI operations.

**Business Value:** Organization creation is the gateway to all platform functionality; enables multi-tenant onboarding.

**Preconditions:**
- User is authenticated and email-verified
- User is not at the maximum organization creation limit (per plan)

**Main Flow:**
1. User selects "Create Organization"
2. User provides: organization name, description (optional), industry (optional)
3. System validates the organization name and generates a unique slug
4. System creates the organization and assigns the creating user as Owner
5. System creates default organization settings with sensible defaults
6. User is taken to the organization onboarding flow (optional guided setup)

**Alternate Flow:**
- AF-1: User joins an existing organization via invitation instead of creating → Directed to invitation acceptance flow

**Exception Flow:**
- EF-1: Organization name contains prohibited characters or is a reserved word → Validation error displayed inline

**Acceptance Criteria:**
- **Given** a user provides a valid organization name, **When** submitted, **Then** the organization is created, the user is assigned as Owner, and they enter the organization dashboard
- **Given** the organization name generates a duplicate slug, **When** detected, **Then** the system suggests alternatives or auto-appends a unique suffix
- **Given** a user has reached their plan's organization limit, **When** they attempt to create another, **Then** they are shown an upgrade prompt

**Validation Rules:**
- Organization name: 2–100 characters, required
- Slug: alphanumeric + hyphens, unique across platform, auto-generated from name

**Permission Requirements:** Authenticated user (any verified user can create an organization)

**Security Considerations:** Organization slug must be validated to prevent path traversal or injection in URLs

**Audit Requirements:** Organization creation logged with creator identity and timestamp

**Dependencies:** IAM, Org service

---

### US-014: Update Organization Settings

| Field | Details |
|---|---|
| **Story ID** | US-014 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Organization Settings |
| **User Role** | Organization Owner / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to update my organization's name, description, logo, and settings,
> so that the organization's profile accurately represents our company.

**Acceptance Criteria:**
- **Given** an admin updates the organization name, **When** saved, **Then** the new name is reflected across all UI surfaces for that organization
- **Given** an admin uploads a logo, **When** saved, **Then** the logo is displayed in the navigation and organization profile
- **Given** a non-admin user attempts to access organization settings, **When** navigating to the page, **Then** they receive a 403 Forbidden response

**Permission Requirements:** Organization Owner or Admin role

**Audit Requirements:** All organization settings changes logged with the actor's identity

**Priority:** P1 | **Phase:** MVP

---

### US-015: Invite Member to Organization

| Field | Details |
|---|---|
| **Story ID** | US-015 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Member Invitations |
| **User Role** | Organization Admin / Owner |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to invite a user to join the organization by email,
> so that they can access the platform resources and collaborate on AI workflows.

**Business Value:** Enables team collaboration; drives user growth; critical for multi-user organizations.

**Preconditions:**
- Admin is authenticated and has the Admin or Owner role
- The email to be invited is not already a member

**Main Flow:**
1. Admin navigates to Organization → Members → Invite Member
2. Admin enters the invitee's email address and selects a role
3. System validates the email and checks it is not already a member or pending invitee
4. System creates a pending invitation record
5. System sends an invitation email to the invitee with an acceptance link
6. Pending invitation is listed in the Members section

**Alternate Flow:**
- AF-1: The invitee's email is already registered on the platform → They accept the invitation and are added to the organization with the specified role; they do not need to register again
- AF-2: The invitee's email is not yet registered → They register first, then accept the invitation

**Exception Flow:**
- EF-1: Invitee email is already a pending invitation for this org → Admin is informed of the duplicate; can resend the existing invitation

**Acceptance Criteria:**
- **Given** an admin invites a valid email with a specified role, **When** submitted, **Then** an invitation email is sent and the invitation appears as "Pending" in the member list
- **Given** the invitee clicks the invitation link within the validity period, **When** they accept, **Then** they are added to the organization with the specified role and the invitation status changes to "Accepted"
- **Given** the invitation link has expired (>72 hours), **When** clicked, **Then** an expiry message is shown and the invitee is prompted to contact the admin for a new invitation
- **Given** an admin revokes a pending invitation, **When** confirmed, **Then** the invitation link is invalidated and the invitation is removed from the list

**Validation Rules:**
- Email: valid format, not already a member, not a duplicate pending invitation

**Permission Requirements:** Organization Admin or Owner

**Security Considerations:** Invitation tokens must be cryptographically random and single-use; expiry enforced server-side

**Audit Requirements:** Invitation sent, accepted, revoked, and expired events logged

**Dependencies:** US-013, Email delivery service, IAM service

---

### US-016: Accept Organization Invitation

| Field | Details |
|---|---|
| **Story ID** | US-016 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Member Invitations |
| **User Role** | Invited User |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an invited user,
> I want to accept an organization invitation and join the team,
> so that I can collaborate on the organization's AI workflows and resources.

**Acceptance Criteria:**
- **Given** a valid, unexpired invitation link, **When** clicked by the correct email's owner, **Then** the user is added to the organization and redirected to the organization dashboard
- **Given** the invitation was sent to email A but is clicked by a user logged in with email B, **When** the link is clicked, **Then** the user is shown an error that the invitation is for a different email address
- **Given** an already-accepted invitation link, **When** clicked, **Then** the user is informed it has already been used and is offered a login link

**Priority:** P0 | **Phase:** MVP

---

### US-017: Remove Member from Organization

| Field | Details |
|---|---|
| **Story ID** | US-017 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Member Management |
| **User Role** | Organization Admin / Owner |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to remove a member from the organization,
> so that they no longer have access to the organization's resources.

**Acceptance Criteria:**
- **Given** an admin removes a member, **When** confirmed, **Then** the member's access to the organization is revoked immediately, their active sessions for that organization are invalidated, and their data contributions remain
- **Given** an admin attempts to remove the organization Owner, **When** confirmed, **Then** the action is blocked with a message that ownership must be transferred first
- **Given** the removed member has pending approval requests, **When** they are removed, **Then** those approval requests are reassigned or escalated per policy

**Permission Requirements:** Organization Admin or Owner; cannot remove Owner

**Audit Requirements:** Member removal logged with admin identity and timestamp

**Priority:** P1 | **Phase:** MVP

---

### US-018: Transfer Organization Ownership

| Field | Details |
|---|---|
| **Story ID** | US-018 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Organization Lifecycle |
| **User Role** | Organization Owner |
| **Priority** | P2 |
| **Phase** | MVP |

**User Story:**
> As an organization owner,
> I want to transfer ownership of the organization to another member,
> so that someone else can take administrative responsibility.

**Acceptance Criteria:**
- **Given** an owner initiates ownership transfer to an active member, **When** confirmed with re-authentication, **Then** the new member becomes Owner and the current owner is downgraded to Admin
- **Given** the transfer target is not an active member, **When** submitted, **Then** the transfer is blocked and an error is shown

**Security Considerations:** Ownership transfer requires re-authentication (password or MFA confirmation)

**Audit Requirements:** Ownership transfer logged with both parties' identities

**Priority:** P2 | **Phase:** MVP

---

### US-019: Delete Organization

| Field | Details |
|---|---|
| **Story ID** | US-019 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Organization Lifecycle |
| **User Role** | Organization Owner |
| **Priority** | P2 |
| **Phase** | Phase 2 |

**User Story:**
> As an organization owner,
> I want to permanently delete the organization and all associated data,
> so that data is removed when the organization no longer needs the platform.

**Acceptance Criteria:**
- **Given** an owner initiates organization deletion, **When** they confirm with the organization name and re-authenticate, **Then** the organization is marked for deletion, all members lose access, and data is scheduled for purge within 30 days
- **Given** the organization has active running workflow executions, **When** deletion is initiated, **Then** the admin is warned and must cancel those runs before proceeding

**Security Considerations:** Requires explicit text confirmation and re-authentication; irreversible action

**Audit Requirements:** Organization deletion event logged

**Priority:** P2 | **Phase:** Phase 2

---

### US-020: Create Workspace within Organization

| Field | Details |
|---|---|
| **Story ID** | US-020 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Workspace Management |
| **User Role** | Organization Admin / Owner |
| **Priority** | P3 |
| **Phase** | Phase 2 |

**User Story:**
> As an organization admin,
> I want to create workspaces within the organization to group teams or projects,
> so that different departments can operate independently within the same organization.

**Acceptance Criteria:**
- **Given** an admin creates a workspace with a name, **When** submitted, **Then** the workspace is created within the organization and can be assigned to members
- **Given** a member is assigned to a workspace, **When** they access the platform, **Then** they can only see resources within their assigned workspaces

**Priority:** P3 | **Phase:** Phase 2

---

### US-021: View Organization Dashboard

| Field | Details |
|---|---|
| **Story ID** | US-021 |
| **Epic** | EPIC-02 — Organization & Workspace Management |
| **Feature** | Organization Overview |
| **User Role** | Any Organization Member |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization member,
> I want to see an overview dashboard when I enter the organization,
> so that I have a clear picture of recent activity, key metrics, and pending actions.

**Acceptance Criteria:**
- **Given** a member enters the organization, **When** the dashboard loads, **Then** they see: recent workflow executions (filtered by their permissions), pending approval requests (if they are an approver), key metrics (success rate, recent failures), and quick navigation links
- **Given** an Analyst user views the dashboard, **When** they navigate to the workflow builder, **Then** they see a read-only view and cannot edit

**Priority:** P1 | **Phase:** MVP

---

### US-022 – US-025: Additional Organization Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-022 | Switch Between Organizations | MVP | P1 |
| US-023 | View Organization Member List | MVP | P1 |
| US-024 | Configure Organization AI Model Settings | MVP | P1 |
| US-025 | Configure Organization Session Policy | Phase 2 | P2 |

---

## EPIC 3 — USER & ROLE MANAGEMENT

---

### US-026: View Members and Roles

| Field | Details |
|---|---|
| **Story ID** | US-026 |
| **Epic** | EPIC-03 — User & Role Management |
| **Feature** | Role Management |
| **User Role** | Organization Admin / Owner |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to view all members and their assigned roles,
> so that I can understand who has what access and identify any misconfigurations.

**Acceptance Criteria:**
- **Given** an admin navigates to Members, **When** the page loads, **Then** they see a list of all active members, pending invitations, and their roles; the list is searchable and filterable by role
- **Given** a non-admin member navigates to Members, **When** the page loads, **Then** they see a read-only list of members without role management controls

**Priority:** P1 | **Phase:** MVP

---

### US-027: Change Member Role

| Field | Details |
|---|---|
| **Story ID** | US-027 |
| **Epic** | EPIC-03 — User & Role Management |
| **Feature** | Role Assignment |
| **User Role** | Organization Admin / Owner |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to change a member's role within the organization,
> so that their access permissions reflect their current responsibilities.

**Acceptance Criteria:**
- **Given** an admin changes a member's role from Analyst to Workflow Manager, **When** saved, **Then** the member immediately gains Workflow Manager permissions and loses Analyst-only restrictions
- **Given** an admin attempts to change the Owner's role, **When** they try to reassign, **Then** the action is blocked; ownership transfer must be used instead
- **Given** a member's role is demoted, **When** the role change is saved, **Then** any active sessions are updated to reflect the new permissions at next token refresh

**Audit Requirements:** Role change event logged with old role, new role, admin identity, and timestamp

**Priority:** P1 | **Phase:** MVP

---

### US-028 – US-035: Additional Role & User Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-028 | Deactivate a Member Account | MVP | P1 |
| US-029 | Reactivate a Member Account | Phase 2 | P2 |
| US-030 | Bulk Invite Members | Phase 2 | P2 |
| US-031 | View My Role and Permissions | MVP | P1 |
| US-032 | Custom Role Definition | Phase 3 | P3 |
| US-033 | Role-Based Feature Visibility | MVP | P0 |
| US-034 | Enforce MFA for Org Members (Admin Policy) | Phase 2 | P2 |
| US-035 | View User Activity Audit Trail | MVP | P1 |

---

## EPIC 4 — AI AGENT MANAGEMENT

---

### US-036: Create AI Agent

| Field | Details |
|---|---|
| **Story ID** | US-036 |
| **Epic** | EPIC-04 — AI Agent Management |
| **Feature** | Agent Creation |
| **User Role** | Agent Builder / Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to create a new AI agent with a name, purpose, and system instructions,
> so that I can configure an intelligent agent that will perform specific business tasks.

**Business Value:** Agent creation is the foundational capability of the platform's AI workforce.

**Preconditions:**
- User has Agent Builder, Workflow Manager, or Admin role
- At least one AI model is configured for the organization

**Main Flow:**
1. User navigates to Agents → Create Agent
2. User provides: name, description, purpose statement, system instructions
3. User selects the AI model provider and model
4. User configures model parameters (temperature, max tokens, etc.)
5. User selects which tools the agent is permitted to use
6. User selects which knowledge collections the agent can access
7. User configures memory strategy and execution budget
8. User sets the agent's risk profile
9. System validates the configuration
10. Agent is created in Draft state

**Alternate Flow:**
- AF-1: No AI models configured → User is prompted to configure an AI model in Organization Settings first

**Exception Flow:**
- EF-1: System instructions exceed the model's context limit → Validation error displayed with instructions to shorten

**Acceptance Criteria:**
- **Given** a user provides valid agent configuration, **When** submitted, **Then** the agent is created in Draft state with all configurations saved
- **Given** the selected model is unavailable, **When** the configuration is submitted, **Then** a warning is shown but the agent is still created; availability will be checked at execution time
- **Given** no knowledge collections are selected, **When** saved, **Then** the agent is created without RAG access, which is clearly indicated in the configuration
- **Given** no tools are selected, **When** saved, **Then** the agent operates in text-only mode, clearly indicated

**Validation Rules:**
- Name: 2–100 characters, required
- System instructions: required, ≤ model's context limit
- At least one AI model must be configured in the organization

**Permission Requirements:** Agent Builder, Workflow Manager, or Admin role

**Security Considerations:** System instructions must be validated against injection patterns; stored securely

**Audit Requirements:** Agent creation logged with creator identity, agent ID, and model selection

**Dependencies:** AI model configuration (US-024), Tool Registry (US-083), Knowledge Collections (US-056)

---

### US-037: Configure Agent Tool Permissions

| Field | Details |
|---|---|
| **Story ID** | US-037 |
| **Epic** | EPIC-04 — AI Agent Management |
| **Feature** | Agent Configuration |
| **User Role** | Agent Builder / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to explicitly configure which tools an agent is permitted to invoke,
> so that the agent's capabilities are scoped and it cannot perform unauthorized actions.

**Acceptance Criteria:**
- **Given** an agent is configured with Tool A and Tool B only, **When** the agent attempts to call Tool C, **Then** the call is blocked by the orchestration engine and an error is added to the execution trace
- **Given** an admin adds a new tool to the registry, **When** the agent configuration is viewed, **Then** the new tool appears in the "available tools" list as unselected; no implicit access is granted

**Permission Requirements:** Agent Builder or Admin

**Audit Requirements:** Tool permission changes to an agent logged

**Priority:** P0 | **Phase:** MVP

---

### US-038: Configure Agent Knowledge Access

| Field | Details |
|---|---|
| **Story ID** | US-038 |
| **Epic** | EPIC-04 — AI Agent Management |
| **Feature** | Agent Configuration |
| **User Role** | Agent Builder / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to specify which knowledge collections an agent can query,
> so that the agent accesses only the information relevant to its purpose and within data access boundaries.

**Acceptance Criteria:**
- **Given** an agent is granted access to Knowledge Collection A only, **When** executing, **Then** all RAG queries are limited to Collection A; queries against Collection B return no results
- **Given** a knowledge collection is deleted, **When** the agent configuration is viewed, **Then** the deleted collection is removed from the agent's access list and the agent's behavior is updated accordingly

**Priority:** P0 | **Phase:** MVP

---

### US-039: Test Agent in Sandbox

| Field | Details |
|---|---|
| **Story ID** | US-039 |
| **Epic** | EPIC-04 — AI Agent Management |
| **Feature** | Agent Testing |
| **User Role** | Agent Builder / Workflow Manager / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to run a test execution of an agent using a sample input in a sandboxed environment,
> so that I can verify the agent's behavior, reasoning, and outputs before publishing it for production use.

**Business Value:** Enables safe iteration and quality assurance before deploying AI agents to production workflows.

**Preconditions:**
- Agent exists in Draft or Testing state
- User has Agent Builder or higher role

**Main Flow:**
1. User navigates to the agent detail page
2. User selects "Test Agent"
3. User enters a test input message or scenario
4. System transitions the agent to Testing state (if in Draft)
5. System executes the agent in sandbox mode (production tools may be mocked)
6. System displays: agent reasoning trace, tool calls attempted (mocked or real), knowledge retrieved, and final output
7. User reviews the test results

**Alternate Flow:**
- AF-1: User configures test to use real tools (opted in) → Tools execute against real endpoints in test mode

**Exception Flow:**
- EF-1: Agent exceeds execution budget during test → Test fails with budget exceeded error; trace shows where budget was exhausted

**Acceptance Criteria:**
- **Given** a user provides a test input, **When** the test executes, **Then** a full reasoning trace is displayed including: system prompt, user input, tool calls, knowledge retrievals, and final answer
- **Given** sandbox mode is active, **When** the agent calls a tool, **Then** the tool call is mocked by default and marked as [SANDBOXED] in the trace
- **Given** the test uses real tools (opted in), **When** the agent executes, **Then** real tool calls are made and results are actual; this is clearly indicated
- **Given** the agent produces an output, **When** the test completes, **Then** the user can rate the output quality and add notes

**Permission Requirements:** Agent Builder, Workflow Manager, or Admin

**Audit Requirements:** Test execution events logged (distinct from production runs)

**Dependencies:** US-036, Orchestration engine, Tool registry

---

### US-040: Publish Agent

| Field | Details |
|---|---|
| **Story ID** | US-040 |
| **Epic** | EPIC-04 — AI Agent Management |
| **Feature** | Agent Lifecycle |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to publish an agent after review and testing,
> so that it can be used in production workflows.

**Acceptance Criteria:**
- **Given** an agent is in Testing state and all validations pass, **When** published by an authorized user, **Then** the agent transitions to Published state and becomes selectable in the workflow builder
- **Given** an agent in Draft state is published without testing, **When** the publish action is triggered, **Then** the system warns that testing has not been completed but allows publishing if the user confirms
- **Given** a Member (non-manager) attempts to publish an agent, **When** they access the publish control, **Then** they see the option disabled or hidden based on their role

**Permission Requirements:** Workflow Manager or Admin (cannot be Agent Builder alone)

**Audit Requirements:** Agent publication event logged with publisher identity and timestamp

**Priority:** P0 | **Phase:** MVP

---

### US-041: Deprecate / Archive Agent

| Field | Details |
|---|---|
| **Story ID** | US-041 |
| **Epic** | EPIC-04 — AI Agent Management |
| **Feature** | Agent Lifecycle |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to deprecate an agent so that no new workflows use it while existing workflows continue,
> and later archive it when it is fully retired.

**Acceptance Criteria:**
- **Given** an agent is deprecated, **When** a user tries to add the agent to a new workflow, **Then** it does not appear in the selectable agent list and a "deprecated" badge is shown on the agent detail page
- **Given** a deprecated agent is used in an existing published workflow, **When** that workflow executes, **Then** the agent continues to function normally
- **Given** an agent is archived, **When** viewing the agent list, **Then** the archived agent is hidden by default but accessible via "show archived" filter

**Priority:** P1 | **Phase:** MVP

---

### US-042 – US-055: Additional Agent Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-042 | View Agent Execution History | MVP | P1 |
| US-043 | Update Agent Configuration | MVP | P1 |
| US-044 | Configure Agent Memory Strategy | MVP | P1 |
| US-045 | Set Agent Execution Budget | MVP | P0 |
| US-046 | Set Agent Risk Profile | MVP | P0 |
| US-047 | View Agent List | MVP | P1 |
| US-048 | Duplicate Agent Configuration | Phase 2 | P2 |
| US-049 | Create Agent Version (versioning) | Phase 2 | P2 |
| US-050 | View Agent Version History | Phase 2 | P2 |
| US-051 | Roll Back to Previous Agent Version | Phase 2 | P2 |
| US-052 | Configure Agent Output Format | MVP | P2 |
| US-053 | View Agent Detail Page | MVP | P1 |
| US-054 | Delete Agent (Draft only) | MVP | P2 |
| US-055 | Search and Filter Agent List | Phase 2 | P2 |

---

## EPIC 5 — KNOWLEDGE MANAGEMENT

---

### US-056: Create Knowledge Collection

| Field | Details |
|---|---|
| **Story ID** | US-056 |
| **Epic** | EPIC-05 — Knowledge Management |
| **Feature** | Knowledge Organization |
| **User Role** | Agent Builder / Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to create a named knowledge collection,
> so that I can organize related documents and control which agents can access them.

**Acceptance Criteria:**
- **Given** a user creates a knowledge collection with a name and description, **When** submitted, **Then** the collection is created and appears in the knowledge management section
- **Given** a collection is created, **When** an agent is configured, **Then** the collection appears as an option in the agent's knowledge access settings
- **Given** no access permissions are configured on a collection, **When** an agent attempts to query it, **Then** access is denied by default

**Permission Requirements:** Agent Builder, Workflow Manager, or Admin

**Audit Requirements:** Collection creation logged

**Priority:** P0 | **Phase:** MVP

---

### US-057: Upload Document to Knowledge Collection

| Field | Details |
|---|---|
| **Story ID** | US-057 |
| **Epic** | EPIC-05 — Knowledge Management |
| **Feature** | Document Ingestion |
| **User Role** | Agent Builder / Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to upload documents (PDF, DOCX, TXT, MD) to a knowledge collection,
> so that AI agents can retrieve relevant content from those documents during workflow execution.

**Business Value:** Documents represent the organization's proprietary knowledge; uploading them enables grounded, accurate AI responses.

**Preconditions:**
- User has permission to manage the target knowledge collection
- File meets format and size requirements

**Main Flow:**
1. User navigates to the Knowledge Collection
2. User selects "Upload Document"
3. User selects one or more files from their device
4. System validates file format and size
5. System uploads the file to secure storage
6. System queues the document for the asynchronous ingestion pipeline
7. Document appears in the collection with status "Pending"
8. Ingestion pipeline processes the document (extract, chunk, embed, index)
9. Status updates to "Indexed" upon successful completion
10. User receives an in-app notification upon completion or failure

**Alternate Flow:**
- AF-1: User uploads multiple files simultaneously → Each file is processed independently; individual statuses are shown

**Exception Flow:**
- EF-1: File format is unsupported → Validation error shown; file is rejected before upload
- EF-2: File exceeds size limit → Validation error shown with the limit
- EF-3: Ingestion pipeline fails → Status set to "Failed" with error details; retry option offered

**Acceptance Criteria:**
- **Given** a user uploads a valid PDF, **When** the upload completes, **Then** the document appears with "Pending" status and begins ingestion
- **Given** ingestion completes successfully, **When** the status updates, **Then** the document status shows "Indexed" and the agent can retrieve content from it
- **Given** ingestion fails, **When** the failure is detected, **Then** the status shows "Failed" with a human-readable error message and a "Retry Ingestion" button
- **Given** a user uploads a file type not in the supported list, **When** they attempt to submit, **Then** validation blocks the upload and shows supported formats

**Validation Rules:**
- Supported formats: PDF, DOCX, TXT, MD, HTML
- Maximum file size: configurable per plan (default 50MB per file)
- File name: no special characters that could cause path traversal

**Permission Requirements:** Manage Knowledge Collection permission

**Security Considerations:** Files must be scanned for malware before ingestion; file names sanitized; no executable files permitted

**Audit Requirements:** Document upload, ingestion start, ingestion success/failure logged

**Dependencies:** US-056, File storage service, Ingestion pipeline

---

### US-058: View Document Ingestion Status

| Field | Details |
|---|---|
| **Story ID** | US-058 |
| **Epic** | EPIC-05 — Knowledge Management |
| **Feature** | Document Ingestion |
| **User Role** | Agent Builder / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to view the ingestion status of all documents in a knowledge collection,
> so that I know which documents are ready for use and which need attention.

**Acceptance Criteria:**
- **Given** a user views a knowledge collection, **When** the page loads, **Then** each document shows its current status (Pending, Processing, Indexed, Failed) with last updated timestamp
- **Given** a document shows "Failed" status, **When** the user clicks on it, **Then** they see a description of the error and available remediation options (retry, delete, re-upload)

**Priority:** P1 | **Phase:** MVP

---

### US-059: Retry Failed Document Ingestion

| Field | Details |
|---|---|
| **Story ID** | US-059 |
| **Epic** | EPIC-05 — Knowledge Management |
| **Feature** | Document Lifecycle |
| **User Role** | Agent Builder / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to retry ingestion of a failed document,
> so that I can recover without needing to re-upload the original file.

**Acceptance Criteria:**
- **Given** a document is in "Failed" state, **When** the user clicks "Retry Ingestion," **Then** the document is requeued for ingestion and the status resets to "Pending"
- **Given** the retry also fails, **When** the second failure occurs, **Then** the status returns to "Failed" with updated error details

**Priority:** P1 | **Phase:** MVP

---

### US-060: Delete Document from Knowledge Collection

| Field | Details |
|---|---|
| **Story ID** | US-060 |
| **Epic** | EPIC-05 — Knowledge Management |
| **Feature** | Document Lifecycle |
| **User Role** | Agent Builder / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to delete a document from a knowledge collection,
> so that outdated or incorrect information is not retrieved by AI agents.

**Acceptance Criteria:**
- **Given** a user deletes an indexed document, **When** confirmed, **Then** the document is de-indexed from the vector store before deletion is confirmed; a confirmation message is shown
- **Given** a document is de-indexed, **When** an agent subsequently queries the knowledge collection, **Then** the deleted document's content is not returned in any retrieval results
- **Given** deletion fails during the de-indexing step, **When** the failure occurs, **Then** the document remains in its current state and the user is notified of the failure to de-index

**Security Considerations:** Deletion must be confirmed by the user; irreversible in terms of the file (unless backups exist)

**Audit Requirements:** Document deletion event logged with actor identity and document metadata

**Priority:** P1 | **Phase:** MVP

---

### US-061 – US-072: Additional Knowledge Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-061 | Add Knowledge from URL | Phase 2 | P2 |
| US-062 | Add Knowledge from Plain Text | MVP | P2 |
| US-063 | Add Document Metadata and Tags | MVP | P2 |
| US-064 | Update Document (Re-upload New Version) | Phase 2 | P2 |
| US-065 | Re-index Knowledge Collection | Phase 2 | P2 |
| US-066 | Configure Knowledge Collection Access | MVP | P1 |
| US-067 | View Knowledge Collection List | MVP | P1 |
| US-068 | Search Documents within Collection | Phase 2 | P2 |
| US-069 | View Document Preview and Chunks | Phase 2 | P2 |
| US-070 | Delete Knowledge Collection | Phase 2 | P2 |
| US-071 | Export Knowledge Collection Metadata | Phase 3 | P3 |
| US-072 | Classify Knowledge Collection (Data Classification) | Phase 3 | P3 |

---

## EPIC 6 — RAG

---

### US-073: Agent Retrieves Context During Execution

| Field | Details |
|---|---|
| **Story ID** | US-073 |
| **Epic** | EPIC-06 — RAG |
| **Feature** | RAG Retrieval |
| **User Role** | System (Agent) |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an AI agent executing a workflow task,
> I want to automatically retrieve relevant context from permitted knowledge collections,
> so that my responses are grounded in organizational knowledge rather than relying solely on model training data.

**Business Value:** Grounds AI responses in organizational knowledge; reduces hallucination; enables proprietary knowledge leverage.

**Preconditions:**
- Agent has access to at least one indexed knowledge collection
- A RAG node or RAG-enabled agent node is included in the workflow

**Main Flow:**
1. During agent execution, the agent formulates a retrieval query based on the task context
2. The RAG engine queries the permitted knowledge collections using semantic similarity
3. The engine returns the top-K most relevant chunks with their source attribution
4. Retrieved chunks are injected into the agent's context
5. The agent generates a response informed by the retrieved context
6. Retrieved chunks and their sources are logged in the execution trace

**Acceptance Criteria:**
- **Given** an agent executes with a query relevant to an indexed document, **When** RAG retrieval runs, **Then** relevant document chunks are returned and included in the agent's context
- **Given** the agent has no permission to access a knowledge collection, **When** a query is attempted against it, **Then** the collection is excluded from retrieval and the access attempt is logged
- **Given** no relevant content is found above the similarity threshold, **When** retrieval completes, **Then** the agent receives an empty retrieval result and proceeds without hallucinating retrieved content
- **Given** retrieval succeeds, **When** the execution trace is viewed, **Then** the retrieved chunks with document name, section, and similarity score are visible

**Permission Requirements:** Agent-level knowledge access permissions enforced by orchestration engine

**Security Considerations:** Retrieval must be strictly scoped to agent-permitted collections; no cross-tenant retrieval possible

**Audit Requirements:** RAG retrieval events logged per agent execution step

**Dependencies:** US-056, US-057, US-036, Vector store integration

---

### US-074: Configure RAG Node in Workflow

| Field | Details |
|---|---|
| **Story ID** | US-074 |
| **Epic** | EPIC-06 — RAG |
| **Feature** | RAG Workflow Integration |
| **User Role** | Workflow Manager / Agent Builder |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to add a RAG Retrieval node to a workflow,
> so that I can explicitly control when and how knowledge is retrieved and passed to downstream nodes.

**Acceptance Criteria:**
- **Given** a RAG node is added to a workflow, **When** configured, **Then** the user can specify: target knowledge collection(s), retrieval query (static or dynamic from workflow input), top-K, and similarity threshold
- **Given** a workflow with a RAG node executes, **When** the RAG node runs, **Then** the retrieved content is passed as output to the next node in the workflow graph

**Priority:** P1 | **Phase:** MVP

---

### US-075: View Retrieved Citations in Execution Trace

| Field | Details |
|---|---|
| **Story ID** | US-075 |
| **Epic** | EPIC-06 — RAG |
| **Feature** | RAG Observability |
| **User Role** | Agent Builder / Analyst / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an analyst reviewing an agent's execution,
> I want to see exactly which document chunks were retrieved and used in the agent's response,
> so that I can verify the grounding and identify any knowledge gaps.

**Acceptance Criteria:**
- **Given** an agent execution trace is viewed, **When** navigating to the RAG step, **Then** the user sees: the retrieval query, retrieved chunks with similarity scores, source document names, page/section references, and whether each chunk was used in the final response
- **Given** the response cites a fact, **When** the user traces it, **Then** they can link it back to the specific chunk and source document

**Priority:** P1 | **Phase:** MVP

---

### US-076 – US-082: Additional RAG Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-076 | Configure Retrieval Parameters (Top-K, Threshold) | MVP | P1 |
| US-077 | Hybrid Retrieval (Semantic + Keyword) | Phase 2 | P2 |
| US-078 | Test Knowledge Collection with a Query | MVP | P2 |
| US-079 | Evaluate RAG Retrieval Quality | Phase 2 | P2 |
| US-080 | View RAG Usage Metrics per Collection | Phase 2 | P2 |
| US-081 | Re-rank Retrieval Results | Phase 3 | P3 |
| US-082 | Multi-Collection Retrieval with Priority | Phase 2 | P2 |

---

## EPIC 7 — TOOLS & INTEGRATIONS

---

### US-083: View Tool Registry

| Field | Details |
|---|---|
| **Story ID** | US-083 |
| **Epic** | EPIC-07 — Tools & Integrations |
| **Feature** | Tool Registry |
| **User Role** | Agent Builder / Workflow Manager / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to browse the organization's tool registry,
> so that I can see which tools are available and select the right ones for my agent.

**Acceptance Criteria:**
- **Given** a user navigates to the Tool Registry, **When** the page loads, **Then** they see a list of all registered tools with: name, description, category, risk level, and availability status
- **Given** the user filters by category "Email," **When** the filter is applied, **Then** only email-category tools are shown

**Priority:** P1 | **Phase:** MVP

---

### US-084: Configure HTTP/REST Tool

| Field | Details |
|---|---|
| **Story ID** | US-084 |
| **Epic** | EPIC-07 — Tools & Integrations |
| **Feature** | Built-in Tools |
| **User Role** | Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to configure an HTTP/REST API tool with an endpoint URL, authentication, and request schema,
> so that AI agents can make calls to our external APIs as part of workflow execution.

**Acceptance Criteria:**
- **Given** an admin configures an HTTP tool with a URL, method, headers, and auth credentials, **When** saved, **Then** the tool appears in the registry and is selectable for agent assignment
- **Given** the configured endpoint returns an error during a test call, **When** the test is run, **Then** the error response is displayed and the tool is saved but marked as "health unknown"

**Permission Requirements:** Admin role

**Audit Requirements:** Tool configuration changes logged

**Priority:** P0 | **Phase:** MVP

---

### US-085: Store API Credential Securely

| Field | Details |
|---|---|
| **Story ID** | US-085 |
| **Epic** | EPIC-07 — Tools & Integrations |
| **Feature** | Credential Management |
| **User Role** | Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to store an API credential (API key, OAuth token, secret) in the platform's secure vault,
> so that AI agents can use these credentials in tool calls without the credentials being exposed to users.

**Business Value:** Enables secure, centralized credential management; eliminates hardcoded credentials in workflows.

**Acceptance Criteria:**
- **Given** an admin adds an API credential, **When** saved, **Then** the credential is encrypted and stored; only the last 4 characters of the key are shown in the UI
- **Given** a credential is stored, **When** a user tries to view the full value, **Then** the full value is never returned; they can only test or rotate it
- **Given** a credential is used by an agent tool call, **When** the execution trace is viewed, **Then** the credential value is masked in all logs

**Permission Requirements:** Admin role

**Security Considerations:** Credentials encrypted at rest; access to credentials for tool invocation is system-internal only; access logged

**Audit Requirements:** Credential creation, update, deletion, and usage events logged

**Priority:** P0 | **Phase:** MVP

---

### US-086: Configure Tool Retry Policy

| Field | Details |
|---|---|
| **Story ID** | US-086 |
| **Epic** | EPIC-07 — Tools & Integrations |
| **Feature** | Tool Execution Policy |
| **User Role** | Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to configure a retry policy for a tool (max retries, backoff strategy),
> so that transient failures in external API calls are handled automatically without failing the workflow.

**Acceptance Criteria:**
- **Given** a tool has a retry policy of max 3 attempts with exponential backoff, **When** the tool call returns a 429 or 503 error, **Then** the system retries up to 3 times with increasing delay before failing the step
- **Given** the tool call returns a 400 or 403 error (non-retryable), **When** the error occurs, **Then** the step fails immediately without retrying

**Priority:** P1 | **Phase:** MVP

---

### US-087 – US-097: Additional Tool & Integration Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-087 | Configure Email Tool | MVP | P1 |
| US-088 | Test Tool Configuration | MVP | P1 |
| US-089 | Assign Tool Risk Level | MVP | P0 |
| US-090 | View Tool Execution History | MVP | P1 |
| US-091 | Revoke API Credential | MVP | P1 |
| US-092 | Rotate API Credential | Phase 2 | P2 |
| US-093 | Connect OAuth Integration (CRM, ticketing) | Phase 2 | P2 |
| US-094 | Register Custom Tool via REST API Spec | Phase 2 | P2 |
| US-095 | Configure Tool Rate Limits | Phase 2 | P2 |
| US-096 | View Tool Health Status | Phase 2 | P2 |
| US-097 | Deactivate Tool | MVP | P1 |

---

## EPIC 8 — WORKFLOW BUILDER

---

### US-098: Create New Workflow

| Field | Details |
|---|---|
| **Story ID** | US-098 |
| **Epic** | EPIC-08 — Workflow Builder |
| **Feature** | Workflow Creation |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to create a new workflow with a name and description,
> so that I can begin building an automation for a business process.

**Acceptance Criteria:**
- **Given** a user provides a workflow name, **When** submitted, **Then** a new workflow is created in Draft state and the user is taken to the visual workflow builder
- **Given** a workflow name is not provided, **When** submitted, **Then** a validation error is shown

**Priority:** P0 | **Phase:** MVP

---

### US-099: Add Node to Workflow Canvas

| Field | Details |
|---|---|
| **Story ID** | US-099 |
| **Epic** | EPIC-08 — Workflow Builder |
| **Feature** | Visual Workflow Builder |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to drag and drop nodes onto the workflow canvas,
> so that I can visually construct the automation flow.

**Business Value:** Enables non-technical users to build complex AI automations without coding.

**Acceptance Criteria:**
- **Given** a user drags an "AI Agent Node" from the node palette, **When** dropped on the canvas, **Then** the node appears on the canvas and a configuration panel opens
- **Given** multiple nodes are on the canvas, **When** the user draws a connection from node A to node B, **Then** an edge is created representing the flow
- **Given** a node is double-clicked, **When** the action completes, **Then** the node's configuration panel opens
- **Given** a node is deleted from the canvas, **When** confirmed, **Then** all edges connected to that node are also removed

**Priority:** P0 | **Phase:** MVP

---

### US-100: Configure AI Agent Node

| Field | Details |
|---|---|
| **Story ID** | US-100 |
| **Epic** | EPIC-08 — Workflow Builder |
| **Feature** | Node Configuration |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to configure an AI Agent Node by selecting a published agent and defining its input,
> so that the workflow knows which agent to invoke and what to send it.

**Acceptance Criteria:**
- **Given** an AI Agent Node is added to the canvas, **When** the configuration panel opens, **Then** the user can select from published agents, map workflow data to the agent's input, and configure output mapping
- **Given** a deprecated agent is not shown in the list, **When** the user searches, **Then** deprecated agents are hidden unless "show deprecated" is checked
- **Given** no published agents exist, **When** the user opens the AI Agent Node configuration, **Then** a message prompts them to publish an agent first

**Priority:** P0 | **Phase:** MVP

---

### US-101: Configure Human Approval Node

| Field | Details |
|---|---|
| **Story ID** | US-101 |
| **Epic** | EPIC-08 — Workflow Builder |
| **Feature** | Node Configuration |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to add a Human Approval Node and configure the approvers and timeout policy,
> so that the workflow pauses at the right point and routes to the right people for approval.

**Acceptance Criteria:**
- **Given** a Human Approval Node is configured, **When** the workflow reaches that node during execution, **Then** the workflow pauses, an approval request is created, and the configured approvers are notified
- **Given** no approver roles are configured on the node, **When** the workflow is published, **Then** a validation error is shown requiring at least one approver role or user to be configured

**Priority:** P0 | **Phase:** MVP

---

### US-102: Configure Condition Node

| Field | Details |
|---|---|
| **Story ID** | US-102 |
| **Epic** | EPIC-08 — Workflow Builder |
| **Feature** | Node Configuration |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to add a Condition Node with branching logic,
> so that the workflow can take different paths based on data or AI output values.

**Acceptance Criteria:**
- **Given** a Condition Node is configured with an expression (e.g., `{output.confidence} > 0.8`), **When** the workflow executes and the condition evaluates to true, **Then** the "true" branch is followed
- **Given** the condition evaluates to false, **When** execution continues, **Then** the "false" branch is followed
- **Given** the condition expression references a field that does not exist in the workflow data, **When** evaluated, **Then** the step fails with a descriptive error identifying the missing field

**Priority:** P1 | **Phase:** MVP

---

### US-103: Configure Trigger for Workflow

| Field | Details |
|---|---|
| **Story ID** | US-103 |
| **Epic** | EPIC-08 — Workflow Builder |
| **Feature** | Workflow Triggers |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to configure how a workflow is triggered (manually, on a schedule, or via webhook),
> so that the workflow starts at the right time and with the right inputs.

**Acceptance Criteria:**
- **Given** a Manual Trigger is selected, **When** the workflow is published, **Then** authorized users can start the workflow from the UI with optional input parameters
- **Given** a Scheduled Trigger is configured with a cron expression, **When** the schedule fires, **Then** the workflow is automatically started
- **Given** a Webhook Trigger is configured, **When** an external system sends a POST to the workflow's webhook URL, **Then** the workflow is started with the webhook payload as input
- **Given** the workflow is Disabled, **When** the scheduled trigger fires, **Then** the execution is skipped and a log entry is created

**Priority:** P0 | **Phase:** MVP

---

### US-104: Validate and Publish Workflow

| Field | Details |
|---|---|
| **Story ID** | US-104 |
| **Epic** | EPIC-08 — Workflow Builder |
| **Feature** | Workflow Lifecycle |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want the system to validate my workflow before I publish it,
> so that I can catch structural errors before the workflow goes live.

**Acceptance Criteria:**
- **Given** a workflow has an AI Agent Node referencing an unpublished agent, **When** the user attempts to publish, **Then** a validation error is shown listing the specific issue
- **Given** a workflow has an orphaned node (no incoming or outgoing connections), **When** validation runs, **Then** an error is highlighted on the orphaned node
- **Given** all validation checks pass, **When** the user publishes, **Then** the workflow transitions to Published state and is available for execution

**Priority:** P0 | **Phase:** MVP

---

### US-105 – US-117: Additional Workflow Builder Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-105 | Disable / Re-enable Workflow | MVP | P1 |
| US-106 | View Workflow List | MVP | P1 |
| US-107 | Undo / Redo in Workflow Builder | MVP | P1 |
| US-108 | Copy and Paste Nodes | Phase 2 | P2 |
| US-109 | Delete Workflow (Draft only) | MVP | P2 |
| US-110 | Archive Workflow | Phase 2 | P2 |
| US-111 | Configure Tool Node | MVP | P1 |
| US-112 | Configure Notification Node | MVP | P1 |
| US-113 | Configure Transform / Mapping Node | MVP | P2 |
| US-114 | Add Sub-Workflow Node | Phase 2 | P2 |
| US-115 | Add Loop Node | Phase 2 | P2 |
| US-116 | Workflow Version History | Phase 2 | P2 |
| US-117 | Duplicate Workflow | Phase 2 | P2 |

---

## EPIC 9 — AGENTIC ORCHESTRATION

---

### US-118: Agent Executes Multi-Step Reasoning

| Field | Details |
|---|---|
| **Story ID** | US-118 |
| **Epic** | EPIC-09 — Agentic Orchestration |
| **Feature** | Multi-Step Agent Execution |
| **User Role** | System (Orchestration Engine) |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As the orchestration engine,
> I need to support an AI agent executing multiple reasoning steps (plan → tool call → observe → reason → respond),
> so that complex tasks requiring tool use and knowledge retrieval can be completed autonomously.

**Acceptance Criteria:**
- **Given** an agent is tasked with a complex query, **When** it determines a tool call is needed, **Then** the engine executes the permitted tool, returns the result to the agent, and continues reasoning
- **Given** an agent reaches its maximum step budget, **When** the limit is hit, **Then** execution stops with a budget exceeded error; partial trace is preserved
- **Given** an agent is in an infinite loop (same tool being called repeatedly with same args), **When** the loop is detected, **Then** execution is halted and an error is generated

**Priority:** P0 | **Phase:** MVP

---

### US-119: Enforce Agent Tool Permission at Runtime

| Field | Details |
|---|---|
| **Story ID** | US-119 |
| **Epic** | EPIC-09 — Agentic Orchestration |
| **Feature** | Safe Autonomy |
| **User Role** | System (Orchestration Engine) |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As the orchestration engine,
> I need to enforce tool permissions at runtime,
> so that an agent cannot invoke a tool it is not explicitly permitted to use, even if the AI model suggests it.

**Acceptance Criteria:**
- **Given** an agent is configured with tools [A, B] but the model decides to call tool C, **When** the tool call is intercepted, **Then** the call is blocked, an error is added to the trace, and the agent is informed of the constraint
- **Given** an agent calls a High-risk tool, **When** no approved Human Approval record exists for this execution step, **Then** the call is blocked and routed to the Human Approval queue

**Priority:** P0 | **Phase:** MVP

---

### US-120: Risk-Based Action Classification

| Field | Details |
|---|---|
| **Story ID** | US-120 |
| **Epic** | EPIC-09 — Agentic Orchestration |
| **Feature** | Safe Autonomy |
| **User Role** | System (Orchestration Engine) / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As the orchestration engine,
> I need to classify each intended agent action against the organization's risk policy before execution,
> so that high-risk or irreversible actions are never executed without appropriate authorization.

**Acceptance Criteria:**
- **Given** a tool is classified as "High" risk, **When** an agent plans to invoke it, **Then** the engine pauses execution, creates an approval request, and waits for approval before proceeding
- **Given** a tool is classified as "Low" risk, **When** an agent plans to invoke it, **Then** the engine executes the tool autonomously without requiring approval
- **Given** organization policy maps "Critical" risk to "Blocked," **When** an agent plans to invoke a Critical-risk tool, **Then** the invocation is blocked and the workflow fails with an appropriate error message

**Priority:** P0 | **Phase:** MVP

---

### US-121 – US-128: Additional Orchestration Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-121 | Enforce Agent Execution Budget | MVP | P0 |
| US-122 | Manage Agent Context Window | MVP | P1 |
| US-123 | Capture Agent Reasoning Trace | MVP | P0 |
| US-124 | Handle AI Model API Failure Gracefully | MVP | P0 |
| US-125 | Agent-to-Agent Handoff | Phase 2 | P2 |
| US-126 | Agent Dry-Run Mode | Phase 2 | P2 |
| US-127 | Detect and Handle Prompt Injection Attempt | Phase 2 | P2 |
| US-128 | Handle AI Model Timeout and Retry | MVP | P1 |

---

## EPIC 10 — HUMAN-IN-THE-LOOP

---

### US-129: View Approval Queue

| Field | Details |
|---|---|
| **Story ID** | US-129 |
| **Epic** | EPIC-10 — Human-in-the-Loop |
| **Feature** | Approval Queue |
| **User Role** | Approver |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an approver,
> I want to view all pending approval requests assigned to me,
> so that I can review and act on them promptly to keep workflows moving.

**Business Value:** Enables human oversight of AI actions; critical for safe production deployment of AI agents.

**Preconditions:**
- User has the Approver role (or Admin/Workflow Manager with approval rights)
- At least one approval request is pending for this user

**Main Flow:**
1. User navigates to Approvals → My Queue
2. System displays all pending approval requests assigned to the user, sorted by creation time
3. User can see for each request: workflow name, agent name, the action awaiting approval, context summary, time remaining before timeout
4. User clicks into a specific request to view full details

**Acceptance Criteria:**
- **Given** an approver navigates to the approval queue, **When** the page loads, **Then** they see all pending requests assigned to them with key context information
- **Given** a request's timeout is approaching (< 1 hour), **When** displayed in the queue, **Then** it is visually highlighted as urgent
- **Given** a request has timed out, **When** it appears in the queue, **Then** it is marked as "Timed Out" and no longer actionable

**Permission Requirements:** Approver, Workflow Manager, or Admin role

**Priority:** P0 | **Phase:** MVP

---

### US-130: Approve an Action Request

| Field | Details |
|---|---|
| **Story ID** | US-130 |
| **Epic** | EPIC-10 — Human-in-the-Loop |
| **Feature** | Approval Actions |
| **User Role** | Approver |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an approver,
> I want to approve a pending action request,
> so that the paused workflow can resume and the AI agent can proceed with the approved action.

**Acceptance Criteria:**
- **Given** an approver reviews a pending request and clicks "Approve," **When** confirmed, **Then** the approval is recorded, the workflow resumes from the paused state, and the approver receives a confirmation
- **Given** the workflow has been cancelled externally before approval, **When** the approver attempts to approve, **Then** they see a message that the workflow is no longer active and the approval is void
- **Given** an approver provides an optional comment with approval, **When** the workflow continues, **Then** the comment is recorded in the approval record and visible in the audit log

**Audit Requirements:** Approval decision logged with approver identity, comment, and timestamp

**Priority:** P0 | **Phase:** MVP

---

### US-131: Reject an Action Request

| Field | Details |
|---|---|
| **Story ID** | US-131 |
| **Epic** | EPIC-10 — Human-in-the-Loop |
| **Feature** | Approval Actions |
| **User Role** | Approver |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an approver,
> I want to reject a pending action request with a reason,
> so that the AI agent does not proceed with an action I have determined to be inappropriate.

**Acceptance Criteria:**
- **Given** an approver rejects a request with a reason, **When** confirmed, **Then** the workflow is notified of the rejection, the current execution path fails, and a configured failure handler (if any) is triggered
- **Given** the rejection reason field is left empty, **When** submitted, **Then** a validation prompt asks for a reason (configurable whether required or optional per organization)

**Audit Requirements:** Rejection logged with reason, approver identity, and timestamp

**Priority:** P0 | **Phase:** MVP

---

### US-132: Delegate Approval Request

| Field | Details |
|---|---|
| **Story ID** | US-132 |
| **Epic** | EPIC-10 — Human-in-the-Loop |
| **Feature** | Approval Delegation |
| **User Role** | Approver |
| **Priority** | P2 |
| **Phase** | Phase 2 |

**User Story:**
> As an approver,
> I want to delegate an approval request to another authorized user,
> so that requests are not blocked when I am unavailable.

**Acceptance Criteria:**
- **Given** an approver delegates a request to another authorized approver, **When** delegated, **Then** the request appears in the delegate's queue, is removed from the original approver's queue, and the delegation is logged
- **Given** the delegate is not authorized to approve this type of request, **When** delegation is attempted, **Then** the delegation is blocked and an error is shown

**Audit Requirements:** Delegation event logged with delegating approver, delegate, and timestamp

**Priority:** P2 | **Phase:** Phase 2

---

### US-133: Approval Timeout and Auto-Rejection

| Field | Details |
|---|---|
| **Story ID** | US-133 |
| **Epic** | EPIC-10 — Human-in-the-Loop |
| **Feature** | Approval Escalation |
| **User Role** | System |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As the platform,
> I need to automatically escalate or reject approval requests that are not acted on within the configured timeout,
> so that workflows are not indefinitely blocked by inactive approvers.

**Acceptance Criteria:**
- **Given** an approval request has been pending for the configured timeout duration, **When** the timeout fires, **Then** the request is escalated to the next configured escalation level if defined, or auto-rejected
- **Given** all escalation levels are exhausted without action, **When** the final timeout fires, **Then** the approval is auto-rejected, the workflow fails the step, and the relevant admins are notified

**Priority:** P1 | **Phase:** MVP

---

### US-134 – US-143: Additional HITL Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-134 | Request Changes on Approval (Send Back) | Phase 2 | P2 |
| US-135 | Configure Approval Policy | MVP | P1 |
| US-136 | View Approval History | MVP | P1 |
| US-137 | View Approval Request Detail with Full Context | MVP | P0 |
| US-138 | Approval Notification (Email) | MVP | P0 |
| US-139 | Approval Notification (In-App) | MVP | P0 |
| US-140 | View Organization-Wide Approval Metrics | Phase 2 | P2 |
| US-141 | Configure Multi-Approver Requirements | Phase 2 | P2 |
| US-142 | Approval Queue Filtering and Sorting | Phase 2 | P2 |
| US-143 | Approval Escalation Chain Configuration | Phase 2 | P2 |

---

## EPIC 11 — GUARDRAILS & GOVERNANCE

---

### US-144: Configure Organization AI Policy

| Field | Details |
|---|---|
| **Story ID** | US-144 |
| **Epic** | EPIC-11 — Guardrails & Governance |
| **Feature** | AI Behavior Policy |
| **User Role** | Organization Admin / Owner |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to configure platform-level AI behavior policies,
> so that all AI agents operating in the organization adhere to our company's acceptable use standards.

**Acceptance Criteria:**
- **Given** an admin configures a prohibited topic list, **When** an agent receives a request touching a prohibited topic, **Then** the agent refuses the request with a configured message and the event is logged
- **Given** an admin requires PII masking in logs, **When** execution logs are stored, **Then** detected PII patterns are masked before storage

**Priority:** P1 | **Phase:** MVP

---

### US-145: Risk Level to Approval Policy Mapping

| Field | Details |
|---|---|
| **Story ID** | US-145 |
| **Epic** | EPIC-11 — Guardrails & Governance |
| **Feature** | Risk Policy |
| **User Role** | Organization Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to configure which risk levels require human approval before an AI agent can act,
> so that the organization's risk tolerance is systematically enforced across all workflows.

**Acceptance Criteria:**
- **Given** the policy maps "High" risk to "Approval Required," **When** an agent attempts a High-risk tool call, **Then** the call is paused and routed to the approval queue
- **Given** the policy maps "Low" risk to "Autonomous," **When** an agent attempts a Low-risk tool call, **Then** the call executes without approval

**Priority:** P0 | **Phase:** MVP

---

### US-146 – US-155: Additional Guardrails Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-146 | Configure PII Detection and Masking | Phase 2 | P2 |
| US-147 | Configure Prompt Injection Detection | Phase 2 | P2 |
| US-148 | Set Tool-Level Risk Classification | MVP | P0 |
| US-149 | View Governance Policy Summary | MVP | P1 |
| US-150 | Configure Data Retention Policy | Phase 2 | P2 |
| US-151 | Configure Log Masking Rules | Phase 2 | P2 |
| US-152 | View Security Events and Anomalies | Phase 2 | P2 |
| US-153 | Configure Output Filtering Rules | Phase 2 | P2 |
| US-154 | Enforce Cost Budget Limits | Phase 2 | P2 |
| US-155 | Configure Data Classification for Knowledge | Phase 3 | P3 |

---

## EPIC 12 — WORKFLOW EXECUTION

---

### US-156: Manually Trigger Workflow Execution

| Field | Details |
|---|---|
| **Story ID** | US-156 |
| **Epic** | EPIC-12 — Workflow Execution |
| **Feature** | Workflow Execution |
| **User Role** | Workflow Manager / Member / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to manually trigger a published workflow with optional input parameters,
> so that I can start a business process on demand.

**Business Value:** Enables on-demand execution of AI-powered business workflows.

**Preconditions:**
- Workflow is in Published state
- User has permission to execute workflows
- Organization has available execution capacity (not at plan limit)

**Main Flow:**
1. User navigates to the workflow detail page
2. User clicks "Run Now"
3. If the trigger requires input parameters, a form is displayed
4. User fills in required inputs and submits
5. System validates the inputs
6. System creates a workflow Run record with status "Queued"
7. The execution engine picks up the run and processes it
8. User is redirected to the run detail page to monitor execution

**Exception Flow:**
- EF-1: Organization is at concurrent run limit → User is informed; they can wait or upgrade
- EF-2: Required input parameter is missing → Validation error shown before submission

**Acceptance Criteria:**
- **Given** a user triggers a published workflow, **When** submitted with valid inputs, **Then** a Run is created in "Queued" state and the user is taken to the run monitoring page
- **Given** the organization has reached its plan's concurrent run limit, **When** a user attempts to trigger, **Then** an error is shown explaining the limit
- **Given** the workflow trigger requires an input parameter, **When** the user omits it, **Then** a validation error is shown before the run is created

**Permission Requirements:** Member (manual trigger), Workflow Manager (all trigger types), Admin

**Audit Requirements:** Workflow execution triggered event logged with triggering user, workflow ID, and input (masked if sensitive)

**Dependencies:** US-103, US-104, Execution engine

---

### US-157: View Workflow Execution Run List

| Field | Details |
|---|---|
| **Story ID** | US-157 |
| **Epic** | EPIC-12 — Workflow Execution |
| **Feature** | Execution History |
| **User Role** | Workflow Manager / Analyst / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to view the execution history of a workflow,
> so that I can see recent runs, their statuses, and quickly identify any failures.

**Acceptance Criteria:**
- **Given** a user navigates to a workflow's execution history, **When** the page loads, **Then** they see a paginated list of runs with: run ID, status, trigger type, start time, end time, and duration
- **Given** the user filters by "Failed" status, **When** the filter is applied, **Then** only failed runs are shown
- **Given** an Analyst user views the execution list, **When** they click into a run, **Then** they can see full run details but cannot retry or cancel

**Priority:** P1 | **Phase:** MVP

---

### US-158: View Workflow Run Detail and Step Trace

| Field | Details |
|---|---|
| **Story ID** | US-158 |
| **Epic** | EPIC-12 — Workflow Execution |
| **Feature** | Execution Monitoring |
| **User Role** | Workflow Manager / Analyst / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to view the detailed step-by-step execution trace of a workflow run,
> so that I can understand exactly what happened, why it failed, or verify that outputs are correct.

**Acceptance Criteria:**
- **Given** a user opens a run's detail page, **When** it loads, **Then** they see a list of all steps with: status, duration, input, output, and error (if failed); clicking a step expands its full details
- **Given** an AI Agent step is expanded, **When** viewed, **Then** the agent's full reasoning trace is visible (plan, tool calls, observations, final answer)
- **Given** a RAG step is expanded, **When** viewed, **Then** the retrieval query, returned chunks, sources, and similarity scores are visible

**Priority:** P0 | **Phase:** MVP

---

### US-159: Cancel a Running Workflow

| Field | Details |
|---|---|
| **Story ID** | US-159 |
| **Epic** | EPIC-12 — Workflow Execution |
| **Feature** | Execution Control |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to cancel a running or paused workflow execution,
> so that I can stop a workflow that is producing incorrect results or is no longer needed.

**Acceptance Criteria:**
- **Given** a workflow is in "Running" state, **When** a manager cancels it, **Then** the run transitions to "Cancelled" state; any in-progress step is allowed to complete or safely terminated; no further steps are executed
- **Given** a workflow is in "Paused" (awaiting approval) state, **When** cancelled, **Then** the pending approval request is voided, the run is cancelled, and the approver is notified

**Audit Requirements:** Cancellation event logged with actor identity and reason

**Priority:** P1 | **Phase:** MVP

---

### US-160: Retry a Failed Workflow Run

| Field | Details |
|---|---|
| **Story ID** | US-160 |
| **Epic** | EPIC-12 — Workflow Execution |
| **Feature** | Execution Recovery |
| **User Role** | Workflow Manager / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want to retry a failed workflow run,
> so that transient failures (network issues, API timeouts) can be resolved without manual re-triggering.

**Acceptance Criteria:**
- **Given** a workflow run has failed, **When** a manager clicks "Retry," **Then** a new run is created with the same inputs, linked to the original failed run, and the retry is noted in both records
- **Given** the retry is attempted on a workflow that has since been Disabled, **When** the retry is initiated, **Then** the retry is blocked and the user is informed that the workflow is disabled

**Audit Requirements:** Retry event logged with actor and linked to original run

**Priority:** P1 | **Phase:** MVP

---

### US-161 – US-172: Additional Execution Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-161 | View Real-Time Execution Progress | Phase 2 | P2 |
| US-162 | Schedule Workflow Execution | MVP | P1 |
| US-163 | Trigger Workflow via Webhook | Phase 2 | P2 |
| US-164 | Enforce Concurrent Run Limits | MVP | P0 |
| US-165 | Enforce Total Run Limits (Plan) | MVP | P0 |
| US-166 | View Step Input and Output Data | MVP | P1 |
| US-167 | View Token Usage per Run | MVP | P1 |
| US-168 | View Estimated Cost per Run | MVP | P1 |
| US-169 | Handle Workflow Step Timeout | MVP | P1 |
| US-170 | Automatic Step Retry on Transient Failure | MVP | P1 |
| US-171 | Idempotency Guard for Duplicate Triggers | MVP | P1 |
| US-172 | View Run Linked to Approval Request | MVP | P1 |

---

## EPIC 13 — MONITORING & OBSERVABILITY

---

### US-173: Organization Observability Dashboard

| Field | Details |
|---|---|
| **Story ID** | US-173 |
| **Epic** | EPIC-13 — Monitoring & Observability |
| **Feature** | Observability Dashboard |
| **User Role** | Workflow Manager / Analyst / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As a workflow manager,
> I want a centralized observability dashboard for my organization,
> so that I have a real-time view of workflow health, active runs, recent failures, and key metrics.

**Acceptance Criteria:**
- **Given** a user opens the observability dashboard, **When** the page loads, **Then** they see: number of active runs, recent failure alerts, latency trend chart (last 24h), token usage (last 24h), and cost (last 24h)
- **Given** a failure alert is shown, **When** clicked, **Then** the user is taken directly to the failed run's detail page

**Priority:** P1 | **Phase:** MVP

---

### US-174: View Agent Execution Trace

| Field | Details |
|---|---|
| **Story ID** | US-174 |
| **Epic** | EPIC-13 — Monitoring & Observability |
| **Feature** | AI Tracing |
| **User Role** | Agent Builder / Analyst / Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to view the full hierarchical execution trace of an agent invocation,
> so that I can debug issues, understand the agent's reasoning, and verify tool and knowledge usage.

**Acceptance Criteria:**
- **Given** a user views an agent execution trace, **When** expanded, **Then** they see in sequential order: system prompt, user input, planning steps, each tool call (input, output, latency, status), each RAG retrieval, and the final output
- **Given** a tool call failed, **When** viewed in the trace, **Then** the failure is highlighted with the error response and retry attempts shown

**Priority:** P0 | **Phase:** MVP

---

### US-175: Token Usage and Cost Monitoring

| Field | Details |
|---|---|
| **Story ID** | US-175 |
| **Epic** | EPIC-13 — Monitoring & Observability |
| **Feature** | Cost Monitoring |
| **User Role** | Admin / Analyst |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to monitor token usage and estimated AI cost per workflow, per agent, and across the organization,
> so that I can manage AI spending and identify cost-intensive workflows.

**Acceptance Criteria:**
- **Given** an admin views the cost monitoring page, **When** the page loads, **Then** they see: total token usage and estimated cost for the current billing period, top 5 most expensive workflows, and daily cost trend chart
- **Given** the organization's cost approaches a configured budget alert threshold, **When** the threshold is crossed, **Then** the admin receives an in-app and email notification

**Priority:** P1 | **Phase:** MVP

---

### US-176 – US-185: Additional Monitoring Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-176 | View Error Logs per Workflow | MVP | P1 |
| US-177 | View Latency Metrics per Step | MVP | P1 |
| US-178 | Configure Metric-Based Alerts | MVP | P1 |
| US-179 | View Tool Execution Metrics | Phase 2 | P2 |
| US-180 | View RAG Performance Metrics | Phase 2 | P2 |
| US-181 | Platform Health Dashboard (Super Admin) | MVP | P1 |
| US-182 | View Run Error Details with Stack Context | MVP | P1 |
| US-183 | Alert on Workflow Failure Rate Spike | Phase 2 | P2 |
| US-184 | Alert on Latency Degradation | Phase 2 | P2 |
| US-185 | Search and Filter Execution Runs | MVP | P1 |

---

## EPIC 14 — AI EVALUATION

---

### US-186: Create Evaluation Dataset

| Field | Details |
|---|---|
| **Story ID** | US-186 |
| **Epic** | EPIC-14 — AI Evaluation |
| **Feature** | Evaluation Framework |
| **User Role** | Agent Builder / Admin |
| **Priority** | P2 |
| **Phase** | MVP (Basic) |

**User Story:**
> As an agent builder,
> I want to create an evaluation dataset with input/expected output pairs,
> so that I can systematically test my agent's quality against known good answers.

**Acceptance Criteria:**
- **Given** a user creates an evaluation dataset with 10 input/output pairs, **When** saved, **Then** the dataset is stored and associated with the organization
- **Given** a dataset is linked to an agent, **When** an evaluation run is triggered, **Then** the agent is invoked once per dataset entry and results are compared to expected outputs

**Priority:** P2 | **Phase:** MVP (Basic)

---

### US-187: Run Agent Evaluation

| Field | Details |
|---|---|
| **Story ID** | US-187 |
| **Epic** | EPIC-14 — AI Evaluation |
| **Feature** | Agent Evaluation |
| **User Role** | Agent Builder / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an agent builder,
> I want to run an evaluation suite against a configured agent,
> so that I can measure the agent's quality and track improvement or regression over time.

**Acceptance Criteria:**
- **Given** an evaluation run is triggered, **When** it completes, **Then** the results show: per-question scores (task completion, groundedness, relevance), an overall aggregate score, and a pass/fail status based on the configured threshold
- **Given** the evaluation score falls below the configured threshold, **When** results are generated, **Then** an alert is sent to the agent builder/admin

**Priority:** P1 | **Phase:** MVP

---

### US-188: View Evaluation Results and Trend

| Field | Details |
|---|---|
| **Story ID** | US-188 |
| **Epic** | EPIC-14 — AI Evaluation |
| **Feature** | Evaluation Analytics |
| **User Role** | Agent Builder / Analyst / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an analyst,
> I want to view evaluation results over time for a specific agent,
> so that I can identify quality trends and regressions across model updates or agent configuration changes.

**Acceptance Criteria:**
- **Given** multiple evaluation runs have been completed for an agent, **When** the evaluation history page is viewed, **Then** a trend chart shows the score over time with annotations for agent version changes

**Priority:** P1 | **Phase:** MVP

---

### US-189 – US-197: Additional Evaluation Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-189 | Configure Evaluation Scoring Threshold | MVP | P2 |
| US-190 | Evaluate RAG Retrieval Quality | Phase 2 | P2 |
| US-191 | Hallucination Detection Scoring | Phase 2 | P2 |
| US-192 | Custom Evaluation Criteria | Phase 2 | P3 |
| US-193 | Compare Evaluation Results Across Agent Versions | Phase 2 | P2 |
| US-194 | Compare Evaluation Results Across Models | Phase 2 | P2 |
| US-195 | Export Evaluation Results | Phase 2 | P2 |
| US-196 | Evaluation Alert Configuration | Phase 2 | P2 |
| US-197 | Regression Testing Suite | Phase 3 | P3 |

---

## EPIC 15 — ANALYTICS

---

### US-198: View Workflow Analytics Dashboard

| Field | Details |
|---|---|
| **Story ID** | US-198 |
| **Epic** | EPIC-15 — Analytics |
| **Feature** | Analytics Dashboard |
| **User Role** | Analyst / Workflow Manager / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an analyst,
> I want to view an analytics dashboard showing workflow performance metrics,
> so that I can understand the effectiveness of our AI automation and identify areas for improvement.

**Acceptance Criteria:**
- **Given** an analyst opens the analytics dashboard, **When** the page loads, **Then** they see: total executions, success rate, failure rate, average duration, automation rate, and human approval rate for the selected period
- **Given** the user filters by a specific workflow, **When** the filter is applied, **Then** all metrics reflect only that workflow's data

**Priority:** P1 | **Phase:** MVP

---

### US-199: View AI Cost Analytics

| Field | Details |
|---|---|
| **Story ID** | US-199 |
| **Epic** | EPIC-15 — Analytics |
| **Feature** | Cost Analytics |
| **User Role** | Admin / Analyst |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to view AI cost analytics broken down by workflow and agent,
> so that I can identify where AI spend is concentrated and optimize accordingly.

**Acceptance Criteria:**
- **Given** an admin views cost analytics, **When** the page loads, **Then** they see: total AI cost for the period, cost by workflow (top 10), cost by agent (top 10), and daily cost trend
- **Given** the user sets a date range filter, **When** applied, **Then** all cost figures update to reflect only the selected range

**Priority:** P1 | **Phase:** MVP

---

### US-200 – US-208: Additional Analytics Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-200 | View Agent Performance Metrics | MVP | P1 |
| US-201 | View Human Approval Analytics | Phase 2 | P2 |
| US-202 | View Execution Volume Trend | MVP | P1 |
| US-203 | View Time Saved Estimate | Phase 2 | P2 |
| US-204 | Filter Analytics by Date Range | MVP | P1 |
| US-205 | Filter Analytics by Workflow or Agent | Phase 2 | P2 |
| US-206 | Export Analytics Data (CSV) | Phase 2 | P2 |
| US-207 | View Token Usage Breakdown | MVP | P1 |
| US-208 | Usage Summary Report | Phase 2 | P2 |

---

## EPIC 16 — ADMINISTRATION

---

### US-209: Organization Administration Panel

| Field | Details |
|---|---|
| **Story ID** | US-209 |
| **Epic** | EPIC-16 — Administration |
| **Feature** | Admin Panel |
| **User Role** | Organization Admin / Owner |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want access to a dedicated administration panel,
> so that I can manage all organizational settings, users, integrations, and policies from one place.

**Acceptance Criteria:**
- **Given** an admin navigates to Settings / Admin, **When** the page loads, **Then** they have access to sections covering: Users, Roles, AI Models, Integrations, Policies, Usage, and Audit Logs
- **Given** a Workflow Manager (non-admin) navigates to the Admin URL, **When** the page loads, **Then** they receive a 403 Forbidden response

**Priority:** P1 | **Phase:** MVP

---

### US-210: Configure Organization AI Model Provider

| Field | Details |
|---|---|
| **Story ID** | US-210 |
| **Epic** | EPIC-16 — Administration |
| **Feature** | AI Model Management |
| **User Role** | Organization Admin |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to configure one or more AI model providers with their API credentials,
> so that AI agents in the organization can use the desired models.

**Acceptance Criteria:**
- **Given** an admin adds an OpenAI API key, **When** saved, **Then** the connection is validated (a test call is made), and if successful, the provider is available for agent configuration
- **Given** the API key is invalid, **When** the validation test fails, **Then** an error is shown and the configuration is not saved

**Security Considerations:** API keys are encrypted at rest; never returned in plaintext; masked in UI

**Audit Requirements:** AI model provider configuration changes logged

**Priority:** P0 | **Phase:** MVP

---

### US-211 – US-220: Additional Admin Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-211 | View Audit Logs | MVP | P1 |
| US-212 | Filter and Search Audit Logs | Phase 2 | P2 |
| US-213 | Export Audit Logs | Phase 2 | P2 |
| US-214 | Configure Organization Usage Limits | Phase 2 | P2 |
| US-215 | View Organization Usage Summary | MVP | P1 |
| US-216 | Configure Default Approval Policy | MVP | P1 |
| US-217 | Super Admin Platform Console | MVP | P1 |
| US-218 | Super Admin — Suspend Organization | Phase 2 | P2 |
| US-219 | View System Health (Super Admin) | MVP | P1 |
| US-220 | Manage Organization Plan (Super Admin) | Phase 2 | P2 |

---

## EPIC 17 — API & DEVELOPER PLATFORM

---

### US-221: Create API Key

| Field | Details |
|---|---|
| **Story ID** | US-221 |
| **Epic** | EPIC-17 — API & Developer Platform |
| **Feature** | API Key Management |
| **User Role** | Organization Admin |
| **Priority** | P2 |
| **Phase** | Phase 2 |

**User Story:**
> As an organization admin,
> I want to create API keys with configurable scopes,
> so that developers can programmatically access platform features without sharing user credentials.

**Acceptance Criteria:**
- **Given** an admin creates an API key with a name and selected scopes, **When** created, **Then** the full key is displayed once; subsequent views show only the last 4 characters
- **Given** a developer uses an API key to trigger a workflow, **When** the request is received, **Then** the trigger is authenticated, the workflow runs, and the key usage is logged

**Priority:** P2 | **Phase:** Phase 2

---

### US-222: Trigger Workflow via API

| Field | Details |
|---|---|
| **Story ID** | US-222 |
| **Epic** | EPIC-17 — API & Developer Platform |
| **Feature** | API Workflow Trigger |
| **User Role** | API User (Developer) |
| **Priority** | P2 |
| **Phase** | Phase 2 |

**User Story:**
> As a developer,
> I want to trigger a workflow execution via a REST API call using an API key,
> so that I can integrate AI Workforce workflows into our existing systems and products.

**Acceptance Criteria:**
- **Given** a developer calls the workflow trigger API with a valid API key and required inputs, **When** the request is received, **Then** a run is created and the run ID is returned in the response
- **Given** the API key does not have execute scope, **When** the trigger is attempted, **Then** a 403 Forbidden response is returned
- **Given** the workflow does not exist or is not published, **When** the trigger is attempted, **Then** a 404 Not Found response is returned

**Priority:** P2 | **Phase:** Phase 2

---

### US-223 – US-232: Additional Developer Platform Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-223 | List and Filter API Keys | Phase 2 | P2 |
| US-224 | Revoke API Key | Phase 2 | P2 |
| US-225 | View API Key Usage Logs | Phase 2 | P2 |
| US-226 | Configure Outbound Webhook for Workflow Events | Phase 2 | P2 |
| US-227 | Test Webhook Delivery | Phase 2 | P2 |
| US-228 | View Webhook Delivery History | Phase 2 | P2 |
| US-229 | Get Workflow Run Status via API | Phase 2 | P2 |
| US-230 | List Workflows via API | Phase 2 | P2 |
| US-231 | API Documentation and Sandbox | Phase 2 | P2 |
| US-232 | IP Allowlisting for API Access | Phase 3 | P3 |

---

## EPIC 18 — SECURITY & AUDIT

---

### US-233: View Audit Log

| Field | Details |
|---|---|
| **Story ID** | US-233 |
| **Epic** | EPIC-18 — Security & Audit |
| **Feature** | Audit Trail |
| **User Role** | Organization Admin / Analyst |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization admin,
> I want to view the organization's audit log,
> so that I can track who did what on the platform for compliance and security purposes.

**Acceptance Criteria:**
- **Given** an admin navigates to the audit log, **When** the page loads, **Then** they see a chronological list of audit events with: timestamp, actor (user or system), event type, affected resource, and outcome
- **Given** an admin attempts to modify an audit log entry, **When** the action is attempted, **Then** the action is blocked; audit logs are read-only for all users
- **Given** an admin filters by actor and date range, **When** the filter is applied, **Then** only matching events are shown

**Priority:** P1 | **Phase:** MVP

---

### US-234 – US-244: Additional Security & Audit Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-234 | Audit Log for Agent Events | MVP | P1 |
| US-235 | Audit Log for Workflow Events | MVP | P1 |
| US-236 | Audit Log for Approval Events | MVP | P1 |
| US-237 | Audit Log for Tool and Credential Events | MVP | P1 |
| US-238 | Export Audit Log (CSV) | Phase 2 | P2 |
| US-239 | Configure Audit Log Retention | Phase 2 | P2 |
| US-240 | Security Event Alerting | Phase 2 | P2 |
| US-241 | Rate Limiting on Public Endpoints | MVP | P0 |
| US-242 | Detect and Alert Anomalous Login Behavior | Phase 2 | P2 |
| US-243 | SIEM Integration (Audit Log Export) | Phase 3 | P3 |
| US-244 | Data Export for Compliance (GDPR) | Phase 2 | P2 |

---

## EPIC 19 — NOTIFICATIONS

---

### US-245: Approval Request Notification

| Field | Details |
|---|---|
| **Story ID** | US-245 |
| **Epic** | EPIC-19 — Notifications |
| **Feature** | Approval Notifications |
| **User Role** | Approver |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As an approver,
> I want to be notified immediately when a new approval request is assigned to me,
> so that I can act promptly and prevent workflows from being blocked unnecessarily.

**Acceptance Criteria:**
- **Given** an approval request is created and assigned to me, **When** the request is created, **Then** I receive both an in-app notification and an email notification within 60 seconds
- **Given** the email notification is clicked, **When** it opens, **Then** I am taken directly to the approval request detail page (authenticated flow)

**Priority:** P0 | **Phase:** MVP

---

### US-246 – US-253: Additional Notification Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-246 | Workflow Failure Notification | MVP | P1 |
| US-247 | Workflow Completion Notification | Phase 2 | P2 |
| US-248 | Document Ingestion Complete Notification | MVP | P1 |
| US-249 | Cost Budget Alert Notification | Phase 2 | P2 |
| US-250 | AI Evaluation Score Alert Notification | Phase 2 | P2 |
| US-251 | Configure Notification Preferences | Phase 2 | P2 |
| US-252 | In-App Notification Center | MVP | P1 |
| US-253 | Approval Timeout Warning Notification | MVP | P1 |

---

## EPIC 20 — BILLING / USAGE / PLAN READINESS

---

### US-254: View Current Plan and Usage

| Field | Details |
|---|---|
| **Story ID** | US-254 |
| **Epic** | EPIC-20 — Billing / Usage / Plan Readiness |
| **Feature** | Plan Management |
| **User Role** | Organization Owner / Admin |
| **Priority** | P1 |
| **Phase** | MVP |

**User Story:**
> As an organization owner,
> I want to view our current plan and usage against plan limits,
> so that I understand our consumption and can plan for upgrades.

**Acceptance Criteria:**
- **Given** an owner navigates to Billing / Plan, **When** the page loads, **Then** they see: current plan name, usage against limits (workflow runs, storage, members), and next reset date
- **Given** usage exceeds 80% of a limit, **When** the page is viewed, **Then** the relevant limit is visually highlighted as approaching

**Priority:** P1 | **Phase:** MVP

---

### US-255 – US-263: Additional Billing Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-255 | Enforce Workflow Run Limit per Plan | MVP | P0 |
| US-256 | Enforce Storage Limit per Plan | MVP | P0 |
| US-257 | Enforce Member Limit per Plan | Phase 2 | P1 |
| US-258 | Block Executions When Limit Exceeded | MVP | P0 |
| US-259 | Notify Admin When Approaching Limits | Phase 2 | P1 |
| US-260 | Usage History Report | Phase 2 | P2 |
| US-261 | Plan Upgrade Request Flow | Phase 2 | P2 |
| US-262 | Track Token Usage Against Budget | Phase 2 | P2 |
| US-263 | Per-Workflow Cost Cap Configuration | Phase 3 | P3 |

---

## EPIC 21 — SYSTEM RELIABILITY

---

### US-264: Workflow Execution Recovery After System Restart

| Field | Details |
|---|---|
| **Story ID** | US-264 |
| **Epic** | EPIC-21 — System Reliability |
| **Feature** | Fault Tolerance |
| **User Role** | System |
| **Priority** | P0 |
| **Phase** | MVP |

**User Story:**
> As the platform,
> I need to recover in-progress workflow executions after an unexpected restart,
> so that no workflow execution is lost due to infrastructure failures.

**Acceptance Criteria:**
- **Given** an execution engine instance restarts while workflows are running, **When** the instance recovers, **Then** in-progress runs are detected, their last successfully committed state is identified, and execution resumes from the last committed step
- **Given** a step was in-progress when the restart occurred, **When** recovery runs, **Then** the step is re-executed (idempotency controls prevent duplicate side effects where possible)

**Priority:** P0 | **Phase:** MVP

---

### US-265 – US-272: Additional Reliability Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-265 | Circuit Breaker for External Services | MVP | P1 |
| US-266 | Automatic Retry for Failed External Calls | MVP | P1 |
| US-267 | Graceful Degradation on Partial Service Failure | MVP | P1 |
| US-268 | Database Failover | MVP | P0 |
| US-269 | Knowledge Ingestion Queue Persistence | MVP | P1 |
| US-270 | Webhook Delivery Retry | Phase 2 | P2 |
| US-271 | Email Delivery Retry for Critical Notifications | MVP | P1 |
| US-272 | Health Check Endpoint | MVP | P1 |

---

## EPIC 22 — PLATFORM EXTENSIBILITY

---

### US-273: Register Custom Tool via API Specification

| Field | Details |
|---|---|
| **Story ID** | US-273 |
| **Epic** | EPIC-22 — Platform Extensibility |
| **Feature** | Tool Extensibility |
| **User Role** | Organization Admin |
| **Priority** | P2 |
| **Phase** | Phase 2 |

**User Story:**
> As an organization admin,
> I want to register a custom tool by providing its REST API specification,
> so that AI agents can invoke our internal APIs as part of workflows without requiring platform code changes.

**Acceptance Criteria:**
- **Given** an admin provides an OpenAPI-compatible specification for a custom tool, **When** validated and saved, **Then** the tool appears in the tool registry and is selectable for agent assignment
- **Given** the provided spec is malformed, **When** validated, **Then** specific validation errors are shown identifying the spec issues

**Priority:** P2 | **Phase:** Phase 2

---

### US-274 – US-281: Additional Extensibility Stories (Summary)

| Story ID | Title | Phase | Priority |
|---|---|---|---|
| US-274 | Workflow Template Creation and Reuse | Phase 2 | P2 |
| US-275 | Agent Template Creation and Reuse | Phase 2 | P2 |
| US-276 | Export Workflow as Template | Phase 2 | P2 |
| US-277 | Import Workflow from Template | Phase 2 | P2 |
| US-278 | Custom Webhook Event Types | Phase 3 | P3 |
| US-279 | Plugin / Connector Registration (Phase 3) | Phase 3 | P3 |
| US-280 | Sub-Workflow Invocation | Phase 2 | P2 |
| US-281 | Cross-Organization Template Marketplace | Phase 3 | P3 |

---

## BOUNDARY DEFINITIONS

---

## MVP Feature Boundary

The MVP contains everything necessary to deliver the core value chain with production quality:

**Included in MVP:**
- EPIC-01: Auth & Identity (US-001 to US-007, US-010, US-012)
- EPIC-02: Organization (US-013 to US-018, US-021 to US-024)
- EPIC-03: User & Role Mgmt (US-026, US-027, US-028, US-031, US-033, US-035)
- EPIC-04: AI Agent Mgmt (US-036 to US-047, US-052, US-053)
- EPIC-05: Knowledge Mgmt (US-056 to US-060, US-062, US-063, US-066, US-067)
- EPIC-06: RAG (US-073 to US-076, US-078)
- EPIC-07: Tools (US-083 to US-091, US-097)
- EPIC-08: Workflow Builder (US-098 to US-109, US-111, US-112)
- EPIC-09: Orchestration (US-118 to US-124, US-128)
- EPIC-10: HITL (US-129 to US-131, US-133, US-135 to US-140)
- EPIC-11: Guardrails (US-144, US-145, US-148, US-149)
- EPIC-12: Execution (US-156 to US-162, US-164 to US-172)
- EPIC-13: Monitoring (US-173 to US-178, US-181, US-182, US-185)
- EPIC-14: Evaluation (US-186 to US-189 — basic)
- EPIC-15: Analytics (US-198, US-199, US-200, US-202, US-204, US-207)
- EPIC-16: Admin (US-209, US-210, US-211, US-215, US-216, US-217, US-219)
- EPIC-18: Security & Audit (US-233 to US-237, US-241)
- EPIC-19: Notifications (US-245, US-246, US-248, US-252, US-253)
- EPIC-20: Billing/Usage (US-254 to US-256, US-258)
- EPIC-21: Reliability (US-264 to US-269, US-271, US-272)

---

## Phase 2 Feature Boundary

Adds developer access, advanced agent capabilities, and deeper integrations:

- Developer API (EPIC-17: US-221 to US-231)
- Agent versioning and rollback (US-049 to US-051)
- Workflow versioning (US-116)
- OAuth integration connectors (US-093)
- Advanced HITL (US-132, US-134, US-141 to US-143)
- Advanced guardrails (US-146, US-147, US-150 to US-154)
- Advanced analytics (US-201, US-203, US-205, US-206, US-208)
- Advanced evaluation (US-190 to US-196)
- Advanced monitoring alerts (US-183, US-184)
- Workspace management (US-020)
- Sub-workflow and loop nodes (US-114, US-115, US-280)
- Platform extensibility (US-273 to US-277)
- Advanced notification preferences (US-251)
- Security alerting (US-240, US-242)
- Billing enforcement (US-257, US-259, US-260, US-261, US-262)

---

## Phase 3 Feature Boundary

Enterprise-grade capabilities:

- SSO / SAML (US-009)
- Custom role definition (US-032)
- SIEM integration (US-243)
- GDPR compliance automation (US-244)
- Advanced data governance (US-072, US-155)
- Per-workflow cost caps (US-263)
- Marketplace / plugin ecosystem (US-279, US-281)
- IP allowlisting (US-232)

---

## Critical Business Decisions Required Before Architecture

| # | Decision | Reason |
|---|---|---|
| 1 | **Managed vs. BYOK AI model strategy** — Does the platform host model API keys, or do all orgs bring their own? | Affects billing architecture, cost recovery model, and security scope |
| 2 | **Multi-tenant data isolation model** — Row-level security, schema-per-tenant, or database-per-tenant? | Foundational database architecture decision; cannot be changed easily |
| 3 | **Vector database selection** | Affects RAG performance, query capabilities, and multi-tenant isolation approach |
| 4 | **Evaluation strategy at MVP** — LLM-as-judge vs. rule-based scoring only | Affects dependency on additional model calls and cost |
| 5 | **Exact plan tier limits** | Required for plan enforcement feature implementation |
| 6 | **Phase 2 connector list** — Which CRM, ticketing, and email connectors are in Phase 2? | Scoping decision for Phase 2 sprint planning |
| 7 | **Real-time execution streaming** — Is live streaming of agent reasoning steps required at MVP? | Significant engineering investment; must be decided early |
| 8 | **Approval email: direct action links** — Should approvers be able to approve/reject via email link (without logging in)? | Security and UX tradeoff |
| 9 | **Data retention defaults** — What are the default retention periods for logs, traces, and evaluation results? | Legal, compliance, and storage cost implications |
| 10 | **Free trial or freemium tier** — Is a trial tier available at MVP launch? | Affects go-to-market and onboarding flow |

---

## Ambiguous Requirements Requiring Clarification

| # | Ambiguity | Options to Decide |
|---|---|---|
| 1 | Approval "Request Changes" flow — when the approver requests changes, what exactly happens? Does the workflow route back to a previous step, or does it fail and require re-triggering? | Option A: Fail and re-trigger; Option B: Route to a configured "revision" node |
| 2 | Agent memory strategy — what exactly constitutes "long-term memory"? Is this cross-session context storage, and what privacy implications does it have? | Requires product + legal alignment |
| 3 | Workflow step retry idempotency — how is idempotency enforced for tool calls that may have side effects (e.g., sending an email)? | Requires engineering design |
| 4 | Token cost calculation — is pricing estimated (using known model pricing) or actual (using provider billing APIs)? | Affects accuracy and maintenance burden |
| 5 | Knowledge collection re-indexing — does this delete and rebuild all embeddings, or only update changed documents? | Affects performance and cost during re-indexing |
| 6 | Multi-approver logic — for quorum approval (e.g., 2-of-3), how is the order of approvals managed, and what happens if one approver rejects while another approves? | Requires product design |
| 7 | Workflow concurrency — should the idempotency guard be the default or opt-in? Some workflows are designed to run concurrently | Requires product decision |
| 8 | Agent "purpose statement" — is this a user-facing field only or does it influence the system prompt? | Affects agent behavior and evaluation |

---

*End of User Story Catalogue*

*Document Version: 1.0.0 | Status: Draft*
*Linked BRD: BRD-AIWF-2026-001*
*Total Stories: 281 | MVP: ~160 | Phase 2: ~80 | Phase 3: ~41*
