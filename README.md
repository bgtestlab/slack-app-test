# slack-app-test

```mermaid
sequenceDiagram
    autonumber
    par Channel to Bot
        Channel->>Bot: @autotest run for 'target' on environment
    end
    Note right of Bot: Send thread, username, target, environment
    par Bot to CI
    Bot-->>CI: Trigger a test workflow
    end
    CI->>CI: Run tests
    CI-->>Channel: Send a test results message
    alt is failed
        CI-->>Channel: Send test report
    end   
```
