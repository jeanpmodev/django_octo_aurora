Feature: Aurora Runtime Software Topology Showcase

  Scenario: Render live project structure in single-query mode
    Given a clean Django runtime environment
    When a user requests the Aurora showcase endpoint
    Then the response status code should be 200
    And the rendered canvas should contain the project topology payload
    And subsequent requests should execute in a single database query

  Scenario: Refresh topology snapshot from Django Admin
    Given an authenticated Django superuser
    When the admin triggers the Aurora snapshot refresh action
    Then a new AuroraSnapshot record should be persisted

