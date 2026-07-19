# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please email **[your-email@example.com]** instead of using the public issue tracker.

Please include the following information:
- Description of the vulnerability
- Affected versions
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We take security seriously and will respond within 48 hours to acknowledge receipt of your report.

## Security Best Practices

When using this application, please follow these security guidelines:

### 1. Installation & Updates
- Always use the latest stable version
- Regularly update dependencies: `pip install --upgrade -r requirements.txt`
- Monitor security advisories

### 2. Deployment
- Use HTTPS/TLS in production
- Set `FLASK_DEBUG = False` in production
- Use strong `SECRET_KEY` values
- Implement rate limiting
- Use environment variables for sensitive data

### 3. Data Protection
- Validate all user inputs
- Sanitize data before processing
- Don't log sensitive information
- Implement proper access controls

### 4. Dependencies
- Review dependency updates before deploying
- Use `pip-audit` to check for known vulnerabilities:
  ```bash
  pip install pip-audit
  pip-audit
  ```
- Keep Python version updated

### 5. Code Review
- Review all pull requests before merging
- Use linters and security scanners
- Follow secure coding practices

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | ✅ Yes             |
| < 1.0   | ❌ No              |

## Security Tools

We recommend using these tools to identify vulnerabilities:

- **bandit** - Identify common security issues in Python:
  ```bash
  pip install bandit
  bandit -r .
  ```

- **safety** - Check dependencies for known vulnerabilities:
  ```bash
  pip install safety
  safety check
  ```

- **pip-audit** - Audit Python packages:
  ```bash
  pip install pip-audit
  pip-audit
  ```

## Responsible Disclosure

We appreciate responsible disclosure of security vulnerabilities. Please:
1. Do not publicly disclose the vulnerability until we've had time to fix it
2. Give us reasonable time to release a patch (usually 30 days)
3. Work with us to understand the impact and severity

## Security Headers

When deploying, ensure proper security headers are configured:
- Content-Security-Policy
- X-Content-Type-Options
- X-Frame-Options
- Strict-Transport-Security

## Contact

For security inquiries, contact the maintainer directly rather than using public channels.

---

Thank you for helping keep this project secure! 🔒
