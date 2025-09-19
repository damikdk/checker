#!/usr/bin/env python3
import json
import requests
import logging
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

    logging.info(f"----------------- Starting check")

    for endpoint in config['endpoints']:
        name = endpoint['name']
        start_time = datetime.now()

        try:
            response = requests.request(
                method=endpoint['method'],
                url=endpoint['url'],
                headers=endpoint.get('headers', {}),
                json=endpoint.get('payload'),
                timeout=endpoint.get('timeout', 10),
                stream=endpoint.get('stream', False)
            )
            
            response_time = int(
                (datetime.now() - start_time).total_seconds() * 1000)

            success = response.status_code == 200
            
            # Also check if response contains required success_payload keys
            if not success and endpoint.get('success_payload'):
                try:
                    response_json = response.json()
                    success_keys = endpoint.get('success_payload', [])
                    success = all(key in response_json for key in success_keys)
                except:
                    success = False

            # if not endpoint.get('stream', False):
            #     print(str(response.json())[:100])

            if success:
                logging.info(f"{name} - SUCCESS - {response_time}ms")
            else:
                logging.info(
                    f"{name} - FAILED - {response_time}ms - HTTP {response.status_code}")
                failed_checks.append(name)
        except Exception as e:
            response_time = int(
                (datetime.now() - start_time).total_seconds() * 1000)
            logging.info(f"{name} - FAILED - {response_time}ms - {str(e)}")
            failed_checks.append(name)

    if failed_checks:
        message = f"🚨 Health Check Alert\n\n {len(failed_checks)} endpoint(s) failed:\n\n - {'\n - '.join(failed_checks)}"

        if config['telegram']['enabled']:
            send_telegram_message(
                message,
                config['telegram']['bot_token'],
                config['telegram']['chat_id']
            )

        logging.info(f"Result: {message}")
    else:
        if config['telegram']['enabled']:
            send_telegram_message(
                "All checks passed!",
                config['telegram']['bot_token'],
                config['telegram']['chat_id']
            )

        logging.info(f"----------------- All checks passed!")


def send_telegram_message(message, bot_token, chat_id):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            logging.info("Telegram message sent successfully")
        else:
            logging.error(
                f"Failed to send Telegram message: {response.status_code}")
    except Exception as e:
        logging.error(f"Telegram error: {e}")


if __name__ == "__main__":
    main()
