name: "Feature"
about: "New feature, enhancement, or integration"
title: "[FEATURE] "
labels: "feature"
assignees: ""
body:
  - type: markdown
    attributes:
      value: |
        ## Summary
        Describe the feature in one line.
  - type: input
    id: problem
    attributes:
      label: Problem
      description: "What user problem does this solve?"
      placeholder: "e.g., Users cannot persist historical biomarker trends"
    validations:
      required: true
  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: "High-level implementation approach, libraries/APIs to use"
      placeholder: |
        Example:
        - SQLite for local history
        - AES-256 for local PII encryption
    validations:
      required: true
  - type: checkboxes
    id: acceptance
    attributes:
      label: Acceptance criteria
      options:
        - label: "Clear success criteria defined (endpoints, UI, behavior)"
        - label: "Tests added or existing tests updated"
        - label: "Docs updated (if applicable)"
        - label: "Privacy / PII checklist passed"
  - type: dropdown
    id: milestone
    attributes:
      label: Milestone
      description: "Select suggested milestone"
      options:
        - Phase 1
        - Phase 2
        - Phase 3
        - Phase 4
  - type: dropdown
    id: size
    attributes:
      label: Size estimate
      options:
        - size/S
        - size/M
        - size/L
