# Agent Capabilities & Operations

This document outlines the operations the **Lifecycle AI Agent** can process, including the natural language triggers and specific examples for each.

## 1. Onboarding
Processes new hires by creating identities in HRIS, GitLab, and Active Directory.
*   **Trigger Keywords**: `onboard`, `hire`, `join`
*   **Example 1**: "Please onboard the new hire John Doe into the Engineering team as a Software Engineer."
*   **Example 2**: "Hire Sarah Conner for the Sales team as a Representative."

## 2. Offboarding
Handles employee departures by terminating status and revoking access.
*   **Trigger Keywords**: `offboard`, `terminate`, `leaving`, `exit`
*   **Example 1**: "Terminate employee Alice Smith effective immediately."
*   **Example 2**: "Offboard Bob Wilson from the company as he is leaving next week."

## 3. Team Transfer
Moves an existing employee between departments and updates their access permissions.
*   **Trigger Keywords**: `move`, `transfer`, `change`
*   **Example 1**: "Move Michael Scott from the Sales team to the Management team."
*   **Example 2**: "Transfer Pam Beesly into the Design team from Administration."

## 4. Project Change
Assigns or changes the project focus for an employee. *(Pattern supported, logic in development)*
*   **Trigger Keywords**: `project`, `assign`
*   **Example 1**: "Assign Jim Halpert to the Scranton Expansion project."
*   **Example 2**: "Change Oscar Martinez's project to the Audit 2024 team."

## 5. Leave Management
Processes sabbatical, maternity/paternity, or other leave requests. *(Pattern supported, logic in development)*
*   **Trigger Keywords**: `leave`, `maternity`, `sabbatical`
*   **Example 1**: "Process a maternity leave request for Angela Martin."
*   **Example 2**: "Put Kevin Malone on a 3-month sabbatical starting Monday."

---
> [!NOTE]
> For **Onboarding** and **Transfers**, the agent automatically attempts to provision Active Directory groups and GitLab projects based on the target team mentioned.
