# Health Checker

Minimalistic Python health checker that monitors endpoints and logs results.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Edit `config.json` to add your endpoints:
   ```json
   {
     "endpoints": [
       {
         "name": "API Health",
         "url": "https://api.example.com/health",
         "method": "GET",
         "headers": {"Authorization": "Bearer token"},
         "payload": null,
         "timeout": 10
       }
     ]
   }
   ```

## Usage

Run manually:
```bash
uv run checker.py
```

Check logs:
```bash
tail -f checker.log
```

## Cron Setup

For hourly checks, add to crontab:
```bash
crontab -e
```

Add line:
```
0 * * * * cd /path/to/checker && uv run checker.py
```

## Log Format

```
2024-01-15 14:30:22 - API Health - SUCCESS - 245ms
2024-01-15 14:30:23 - Web App - FAILED - Connection timeout
```

Failed checks prepare a telegram message string in the logs.