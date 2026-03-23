# Vercel Deployment Guide

This repository is configured for deployment on Vercel as a serverless application.

## Quick Deploy to Vercel

### Option 1: Using Vercel CLI

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Follow the prompts to link to your Vercel account

### Option 2: Using Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Import this GitHub repository
3. Vercel will automatically detect the configuration
4. Click "Deploy"

## Configuration Files

- **vercel.json**: Main Vercel configuration
  - Sets Python runtime to 3.9
  - Configures serverless functions with 512MB memory and 60s timeout
  - Routes all requests to appropriate API endpoints

- **api/**: Directory containing serverless functions
  - `index.py`: Serves the main HTML interface
  - `health.py`: Health check endpoint
  - `convert.py`: PDF to handwriting conversion endpoint

- **.vercelignore**: Excludes unnecessary files from deployment

## API Endpoints

Once deployed, your application will have these endpoints:

- `GET /` - Main web interface
- `GET /health` - Health check (returns JSON status)
- `POST /convert` - PDF conversion endpoint

## Environment Variables

No environment variables are required for basic operation. The application uses secure defaults.

## Limitations

- Maximum file size: 16MB (as configured)
- Function timeout: 60 seconds
- Function memory: 512MB
- Large PDFs may take longer to process

## Testing Your Deployment

After deployment, you can test the endpoints:

```bash
# Health check
curl https://your-app.vercel.app/health

# Web interface
open https://your-app.vercel.app
```

## Troubleshooting

If you encounter issues:

1. **500 Error**: Check the Vercel function logs in your dashboard
2. **Timeout**: Increase `maxDuration` in `vercel.json` (max 60s on free tier)
3. **Memory Error**: Increase `memory` in `vercel.json` (max 1024MB on pro tier)
4. **Import Error**: Ensure all dependencies are in `requirements.txt`

## Local Development

For local development, you can still use the Flask app:

```bash
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Production Considerations

- The serverless functions use `/tmp` for temporary file storage
- Files are automatically cleaned up after each request
- No persistent storage - all files are temporary
- Consider using Vercel Pro for production workloads with higher limits
