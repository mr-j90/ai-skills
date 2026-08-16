# Walkthrough Examples

Two worked examples showing how user input translates to the canonical markdown.

---

## Example 1 — Simple login walkthrough

### User input

> "Write a walkthrough for logging into CrewClock. The URL is crewclock.app/login. Users need their work email and a password set by their admin. First they enter email and password, then click Sign In, then they land on their dashboard. Use these screenshots: login-page.png, dashboard.png. PDF please."

### Canonical markdown produced

```markdown
# Logging in to CrewClock

Sign in to your CrewClock account and reach your dashboard.

## Overview

This guide walks you through signing in to CrewClock for the first time. It's intended for workers and supervisors who have been invited to an organization by their admin.

## Prerequisites

- Your work email address
- The password set or provided by your admin
- A modern browser (Chrome, Edge, Safari, or Firefox)

## Steps

### 1. Navigate to the login page

Open your browser and go to https://crewclock.app/login.

![CrewClock login page](images/login-page.png)

### 2. Enter your credentials

Type your work email in the **Email** field and your password in the **Password** field. Then click **Sign In**.

> [!TIP]
> If you've forgotten your password, use the "Forgot password?" link below the form.

### 3. Land on your dashboard

After signing in successfully, you'll be taken to your dashboard where you can view your schedule and clock in.

![CrewClock dashboard](images/dashboard.png)

## Helpful Resources

- **Login URL**: https://crewclock.app/login
- **Support**: support@crewclock.app
```

### Output
`/mnt/user-data/outputs/logging-in-to-crewclock.pdf`

---

## Example 2 — Feature guide with troubleshooting

### User input

> "Need a walkthrough for submitting a timesheet in CrewClock. Steps: open the Timesheets tab, select the pay period, review hours, click Submit, confirm. Screenshots: timesheets-tab.png, select-period.png, review.png, submit-confirm.png. Common issues: 'Submit button is grayed out' means they have unsaved edits; 'Period not showing' means pay period isn't open yet. Also mention the mobile app works too. Generate all three formats."

### Canonical markdown produced

```markdown
# Submitting Your Timesheet

Review and submit your weekly timesheet in CrewClock for payroll processing.

## Overview

This guide shows you how to submit a completed timesheet for approval. Submissions should be done before the pay period closes so your hours are included in the next payroll run.

## Prerequisites

- An active CrewClock account with recorded hours
- Access to the pay period you want to submit

## Steps

### 1. Open the Timesheets tab

From your dashboard, click **Timesheets** in the left navigation.

![Timesheets tab location](images/timesheets-tab.png)

> [!TIP]
> The mobile app has the same Timesheets section under the bottom navigation.

### 2. Select the pay period

Choose the pay period you want to submit from the dropdown at the top of the page.

![Pay period selector](images/select-period.png)

### 3. Review your hours

Scan each day to confirm your hours are accurate. Make any last edits before submitting — once submitted, changes require supervisor approval.

![Reviewing hours](images/review.png)

> [!WARNING]
> Submitted timesheets cannot be edited directly. You'll need to request a reopen from your supervisor.

### 4. Click Submit and confirm

Click the **Submit** button at the bottom of the page, then confirm in the dialog that appears.

![Submit confirmation dialog](images/submit-confirm.png)

## Helpful Resources

- **Login URL**: https://crewclock.app/login
- **Support**: support@crewclock.app
- **Mobile app**: Available on iOS and Android

## Troubleshooting

### Submit button is grayed out

You have unsaved edits on the page. Click **Save** first, then the Submit button will become active.

### Pay period isn't showing in the dropdown

The pay period hasn't been opened yet by your admin, or it has already closed. Contact your supervisor to confirm the schedule.
```

### Outputs
- `/mnt/user-data/outputs/submitting-your-timesheet.pdf`
- `/mnt/user-data/outputs/submitting-your-timesheet.docx`
- `/mnt/user-data/outputs/submitting-your-timesheet.md`

---

## Notes on these examples

- **Imperative headings** throughout ("Navigate to", "Enter", "Click") — never "Navigating to" or "You click".
- **Callouts are sparse** — one TIP and one WARNING across 4 steps, not one per step.
- **No empty sections** — Example 1 omits Troubleshooting because the user didn't provide any.
- **Image paths** are relative (`images/filename.png`) so the renderers resolve them consistently.
