name: "Bug"
about: "Report a bug"
title: "[BUG] "
labels: "bug"
assignees: ""
body:
  - type: markdown
    attributes:
      value: |
        ## Brief
        Provide a short summary and reproduction details below.
  - type: textarea
    id: repro
    attributes:
      label: Steps to reproduce
      description: "Step-by-step instructions to trigger the bug"
      placeholder: |
        1. 
        2. 
        3.
    validations:
      required: true
  - type: input
    id: expected
    attributes:
      label: Expected behavior
      placeholder: "What should happen?"
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: Actual behavior
      placeholder: "What happened instead?"
    validations:
      required: true
  - type: input
    id: environment
    attributes:
      label: Environment
      description: "Version/branch, OS, DB, browser"
      placeholder: "e.g., main@abc123, macOS 13, SQLite"
  - type: textarea
    id: logs
    attributes:
      label: Logs / stack trace
      description: "Redact any PII before pasting"
  - type: dropdown
    id: severity
    attributes:
      label: Severity / priority
      options:
        - p0
        - p1
        - p2
  - type: checkboxes
    id: acceptance
    attributes:
      label: Acceptance criteria
      options:
        - label: "Repro steps included"
        - label: "Fix implemented and linked to this issue"
        - label: "Tests added"
        - label: "Regression test added"
