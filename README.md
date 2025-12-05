# NextWork DevOps Pipeline

## Overview

**NextWork Web Project** is a Java JSP web application demonstrating a complete AWS DevOps CI/CD pipeline. The application is packaged as a WAR file and deployed to Apache Tomcat with Apache HTTP Server as a reverse proxy. This project showcases automated build, test, and deployment using AWS CodeBuild, CodeDeploy, and CodePipeline.

## Features

- **Java JSP Web Application**: Simple web application with JSP pages
- **Maven Build System**: Dependency management and build lifecycle
- **AWS CodeBuild Integration**: Automated builds with `buildspec.yml`
- **AWS CodeDeploy Integration**: Automated deployment with `appspec.yml`
- **Apache Tomcat Deployment**: WAR file deployment to Tomcat server
- **Apache HTTP Proxy**: Reverse proxy configuration for production access
- **AWS CodeArtifact Integration**: Private Maven repository support
- **CloudFormation Infrastructure**: Complete infrastructure as code

## Architecture Overview

![Architecture Overview](./aws-cicd-image.png)

## Project Structure

```
.
├── Code Files/
│   └── nextworkwebapp.yaml   # CloudFormation template for infrastructure
├── ArtifactZip/
│   └── nextwork-devops-cicd-artifact.zip  # Deployment artifact
├── scripts/
│   ├── install_dependencies.sh  # Installs Tomcat and Apache HTTP Server
│   ├── start_server.sh          # Starts Tomcat and HTTP services
│   └── stop_server.sh           # Stops running services
├── src/main/webapp/
│   ├── index.jsp             # Main web application page
│   └── WEB-INF/web.xml       # Web application configuration
├── tools/
│   └── redact_aws_accounts.py   # Security tool to redact AWS account IDs
├── target/                   # Maven build output (generated)
├── appspec.yml              # AWS CodeDeploy deployment specification
├── buildspec.yml            # AWS CodeBuild build instructions
├── pom.xml                  # Maven project configuration
└── settings.xml             # Maven settings with CodeArtifact configuration
```

## Infrastructure & Deployment

### Prerequisites

- AWS Account with appropriate permissions
- Java 8 (Corretto 8) runtime
- Maven 3.x
- AWS CLI configured
- AWS CodeArtifact repository (configured in settings.xml)

### Infrastructure Setup

1. **Deploy CloudFormation Stack**:
   ```bash
   aws cloudformation create-stack \
     --stack-name nextwork-web-infrastructure \
     --template-body file://Code\ Files/nextworkwebapp.yaml \
     --parameters ParameterKey=MyIP,ParameterValue=YOUR_IP/32 \
     --capabilities CAPABILITY_IAM
   ```

2. **Infrastructure Components**:
   - VPC with public subnet
   - EC2 instance with IAM role
   - Security group allowing HTTP access
   - Internet Gateway and routing

### Local Build

```bash
# Set CodeArtifact authentication token
export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
  --domain nextwork-devops-cicd-code-artifact-domain \
  --domain-owner YOUR_AWS_ACCOUNT_ID \
  --region us-east-2 --query authorizationToken --output text)

# Build the project
mvn -s settings.xml compile
mvn -s settings.xml package
```

### CI/CD Pipeline

**AWS CodeBuild** (`buildspec.yml`):
- Installs Java Corretto 8
- Authenticates with CodeArtifact
- Compiles and packages WAR file
- Outputs deployment artifacts

**AWS CodeDeploy** (`appspec.yml`):
- Deploys WAR to `/usr/share/tomcat/webapps/`
- Executes deployment hooks:
  - `BeforeInstall`: Installs Tomcat and Apache HTTP Server
  - `ApplicationStart`: Starts services and enables auto-start
  - `ApplicationStop`: Gracefully stops running services

### Deployment Architecture

- **Apache Tomcat**: Serves the Java web application on port 8080
- **Apache HTTP Server**: Acts as reverse proxy on port 80
- **Virtual Host**: Configured for `app.nextwork.com`
- **Proxy Configuration**: Routes traffic to Tomcat backend

## Security Features

### AWS Account Protection
- **Redaction Tool**: `tools/redact_aws_accounts.py` automatically redacts AWS account IDs from files
- **Environment Variables**: Sensitive data stored in environment variables, not hardcoded
- **IAM Roles**: EC2 instances use IAM roles instead of access keys
- **GitIgnore**: Comprehensive `.gitignore` protects sensitive files

### Usage:
```bash
# Redact AWS account IDs from all files
python tools/redact_aws_accounts.py .
```

## Application Details

- **Group ID**: `com.nextwork.app`
- **Artifact ID**: `nextwork-web-project`
- **Version**: `1.0-SNAPSHOT`
- **Packaging**: WAR
- **Final Name**: `nextwork-web-project.war`

## Customization

- **Dependencies**: Update Maven dependencies in `pom.xml`
- **Infrastructure**: Modify CloudFormation template in `Code Files/nextworkwebapp.yaml`
- **Build Process**: Customize `buildspec.yml` for different build requirements
- **Deployment**: Modify scripts in `scripts/` directory for custom deployment logic
- **Web Content**: Update JSP files in `src/main/webapp/`

## Monitoring & Troubleshooting

- **Application Logs**: Check Tomcat logs in `/var/log/tomcat/`
- **HTTP Logs**: Check Apache logs in `/var/log/httpd/`
- **CodeDeploy Logs**: Available in AWS CodeDeploy console
- **CloudFormation Events**: Monitor stack events for infrastructure issues

## License

This project is for educational and demonstration purposes.

---

*Complete AWS DevOps pipeline demonstration with infrastructure as code, automated CI/CD, and security best practices.*
