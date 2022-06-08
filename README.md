# slack-app-test

Sequence Diagram of Slack App with 
```mermaid
sequenceDiagram
    autonumber
    par Branch to 
        Channel->>App: @botname run for 'target' on environment
    end
    Note right of App: Send thread, username, target, environment
    par App to CI
    App-->>CI: Trigger a test workflow
    end
    CI->>CI: Run tests
    CI-->>Channel: Send a test results message
    alt is failed
        CI-->>Channel: Send test report 
    end    
```

Sequence Diagram of Build and Deployment

```mermaid
sequenceDiagram
    autonumber
    alt test image build
    PC->>Github: PR Request from a non-deployment branch
    Github->>Github: Merge
    Github->>DroneCI: Trigger a build request
    DroneCI: Build a test image
    else slack app image build
    PC->>Github: PR Request from a `deployment` branch
    Github->>DroneCI: Trigger a build request
    DroneCI->>DroneCI: Build a slack app image
    PC->>Gitploy: Deployment Request with `deployment` branch
    Gitploy->>Gitploy:: Deploy a built image to a public endpoint
    end
```
