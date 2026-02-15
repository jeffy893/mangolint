# Mangolint Deployment Guide

This guide covers deploying Mangolint to various platforms.

## Prerequisites

- AWS Account with Bedrock access
- Claude 3 model access enabled in Amazon Bedrock
- AWS credentials (Access Key ID and Secret Access Key)

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `BEDROCK_REGION` - AWS region for Bedrock (default: us-east-1)
- `SECRET_KEY` - Flask secret key (generate a secure random string for production)

## Local Development

1. Create and activate virtual environment:
```bash
./setup.sh
source venv/bin/activate
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run the application:
```bash
python app.py
```

4. Access at `http://localhost:5000`

## Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set AWS_ACCESS_KEY_ID=your_access_key
heroku config:set AWS_SECRET_ACCESS_KEY=your_secret_key
heroku config:set BEDROCK_REGION=us-east-1
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set FLASK_ENV=production
```

4. Deploy:
```bash
git push heroku main
```

5. Open your app:
```bash
heroku open
```

## AWS Elastic Beanstalk Deployment

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB application:
```bash
eb init -p python-3.10 mangolint
```

3. Create environment and deploy:
```bash
eb create mangolint-env
```

4. Set environment variables:
```bash
eb setenv AWS_ACCESS_KEY_ID=your_access_key \
         AWS_SECRET_ACCESS_KEY=your_secret_key \
         BEDROCK_REGION=us-east-1 \
         SECRET_KEY=your_secret_key \
         FLASK_ENV=production
```

5. Open your app:
```bash
eb open
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t mangolint .
```

2. Run the container:
```bash
docker run -p 5000:5000 \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e BEDROCK_REGION=us-east-1 \
  -e SECRET_KEY=your_secret_key \
  mangolint
```

## Production Considerations

### Security
- Never commit `.env` file to version control
- Use IAM roles instead of access keys when possible
- Rotate credentials regularly
- Use AWS Secrets Manager for sensitive data
- Enable HTTPS/SSL in production

### Performance
- Adjust gunicorn workers based on server capacity (default: 2)
- Increase timeout for longer Bedrock API calls (default: 120s)
- Consider caching frequently analyzed terms
- Monitor Bedrock API usage and costs

### Monitoring
- Set up application logging
- Monitor Bedrock API latency and errors
- Track usage metrics
- Set up alerts for failures

### Scaling
- Use load balancer for multiple instances
- Consider async task queue for heavy analysis
- Implement rate limiting for API endpoints
- Cache common ingredient analyses

## Environment-Specific Configuration

### Development
```env
FLASK_ENV=development
DEBUG=True
```

### Production
```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<strong-random-key>
```

## Troubleshooting

### Bedrock Access Issues
- Verify AWS credentials are correct
- Ensure Bedrock is available in your region
- Check IAM permissions for Bedrock access
- Verify Claude 3 model access is enabled

### Deployment Failures
- Check Python version matches runtime.txt
- Verify all dependencies in requirements.txt
- Check environment variables are set
- Review application logs

### Performance Issues
- Increase gunicorn timeout
- Add more workers
- Check Bedrock API latency
- Monitor server resources

## Support

For issues or questions:
- Check AWS Bedrock documentation
- Review Flask deployment guides
- Check platform-specific documentation (Heroku, EB, etc.)
