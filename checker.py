#!/usr/bin/env python3
import json, requests, logging
from datetime import datetime

logging.basicConfig(filename='checker.log', level=logging.INFO, 
                   format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def main():
    failed_checks = []
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        logging.error(f"Config error - FAILED - {e}")
        return
    
    for endpoint in config['endpoints']:
        name = endpoint['name']
        start_time = datetime.now()
        try:
            response = requests.request(
                method=endpoint['method'],
                url=endpoint['url'],
                headers=endpoint.get('headers', {}),
                json=endpoint.get('payload'),
                timeout=endpoint.get('timeout', 10)
            )
            response_time = int((datetime.now() - start_time).total_seconds() * 1000)
            if response.status_code == 200:
                logging.info(f"{name} - SUCCESS - {response_time}ms")
            else:
                logging.info(f"{name} - FAILED - {response_time}ms - HTTP {response.status_code}")
                failed_checks.append(name)
        except Exception as e:
            response_time = int((datetime.now() - start_time).total_seconds() * 1000)
            logging.info(f"{name} - FAILED - {response_time}ms - {str(e)}")
            failed_checks.append(name)
    
    if failed_checks:
        message = f"🚨 Health Check Alert: {len(failed_checks)} endpoint(s) failed - {', '.join(failed_checks)}"
        logging.info(f"Telegram message prepared: {message}")

if __name__ == "__main__":
    main()
