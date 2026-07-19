# Deployment Guide

This document provides step-by-step instructions for deploying the Credit Card Approval Prediction application to various platforms.

## Prerequisites

- Python 3.8+
- Git
- pip package manager
- Account on your chosen deployment platform

## Local Deployment

### Development Environment
```bash
# Clone the repository
git clone https://github.com/Sairamhemanth/Credit-card-approval-prediction.git
cd Credit-card-approval-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

### Production Environment
```bash
# Use Gunicorn to serve the application
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create Heroku App**
```bash
heroku login
heroku create your-app-name
```

2. **Deploy Code**
```bash
git push heroku main
```

3. **Open Application**
```bash
heroku open
```

4. **View Logs**
```bash
heroku logs --tail
```

### Environment Variables
```bash
heroku config:set FLASK_ENV=production
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t credit-card-app:latest .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  credit-card-app:latest
```

### Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
```

Run with:
```bash
docker-compose up
```

## AWS Deployment (EC2)

### Steps

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS AMI
   - Configure security group (allow ports 80, 443, 5000)

2. **Connect and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/Sairamhemanth/Credit-card-approval-prediction.git
cd Credit-card-approval-prediction

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

3. **Run with Gunicorn and Nginx**
```bash
# Install Nginx
sudo apt-get install nginx -y

# Configure Gunicorn as service
sudo nano /etc/systemd/system/credit-card.service
```

4. **Service File Content**
```ini
[Unit]
Description=Credit Card Approval Prediction Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Credit-card-approval-prediction
ExecStart=/home/ubuntu/Credit-card-approval-prediction/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

5. **Start Service**
```bash
sudo systemctl enable credit-card.service
sudo systemctl start credit-card.service
```

## Google Cloud Deployment

### Using Cloud Run

1. **Prepare Application**
   - Ensure Dockerfile exists
   - Ensure PORT is set from environment variable

2. **Deploy**
```bash
gcloud run deploy credit-card-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Azure Deployment

1. **Create App Service**
```bash
az group create --name myResourceGroup --location eastus
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name credit-card-app --runtime "PYTHON|3.9"
```

2. **Deploy**
```bash
az webapp up --name credit-card-app --resource-group myResourceGroup
```

## Environment Variables

Set these variables in your deployment environment:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
```

## Monitoring and Maintenance

### Check Application Health
- Visit `/` to verify the app is running
- Monitor logs for errors
- Track prediction metrics

### Update Application
```bash
git pull origin main
pip install -r requirements.txt
systemctl restart credit-card  # or restart your service
```

### Backup Models
Regularly backup the `models/` directory to preserve trained models.

## Security Considerations

1. **Use HTTPS** - Enable SSL/TLS in production
2. **Environment Variables** - Never commit secrets to git
3. **Input Validation** - Validate all user inputs
4. **Rate Limiting** - Implement rate limiting for API endpoints
5. **Dependencies** - Regularly update dependencies for security patches

```bash
pip install --upgrade pip
pip list --outdated
```

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
lsof -i :5000  # Find process
kill -9 <PID>  # Kill process
```

**Module Import Errors**
```bash
pip install -r requirements.txt
python -m pip install --upgrade pip
```

**Template Not Found**
- Verify `templates/` directory exists
- Check Flask app is running from correct directory

### Enable Debug Logging
```bash
export FLASK_DEBUG=True
python app.py
```

## Performance Optimization

1. **Enable Caching**
   - Cache model predictions
   - Use browser caching for static files

2. **Database Optimization**
   - Add indexes for frequently queried fields
   - Archive old predictions

3. **Load Balancing**
   - Use multiple Gunicorn workers
   - Deploy behind load balancer (nginx, HAProxy)

## Documentation Links

- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Documentation](https://devcenter.heroku.com/)

---

For questions or issues, please open a GitHub issue or contact the maintainer.
