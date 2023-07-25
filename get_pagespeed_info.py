import requests

import secret


def get_pagespeed_data(api_key, url):
    api_endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "key": api_key
    }

    try:
        response = requests.get(api_endpoint, params=params)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return None


def print_audit_details(audits):
    for audit_key, audit_data in audits.items():
        if audit_key == "screenshot-thumbnails":
            continue  # Skip printing details for "Screenshot Thumbnails" audit
        print(f"{'-' * 40}")
        print(f"Audit: {audit_data['title']}")
        print(f"Score: {audit_data['score']}")
        if 'description' in audit_data:
            print(f"Description: {audit_data['description']}")
        if 'details' in audit_data:
            if isinstance(audit_data['details'], dict):  # Check if 'details' is a dictionary
                for detail_key, detail_value in audit_data['details'].items():
                    if isinstance(detail_value, dict) and 'displayValue' in detail_value:
                        print(f"   {detail_key}: {detail_value['displayValue']}")
            else:
                for detail_value in audit_data['details']:
                    if isinstance(detail_value, dict) and 'displayValue' in detail_value:
                        print(f"   {audit_key}: {detail_value['displayValue']}")


def print_performance_metrics(metrics):
    print(f"{'-' * 40}")
    print("Performance Metrics:")
    for metric_key, metric_data in metrics.items():
        if 'displayValue' in metric_data:
            print(f"{metric_key}: {metric_data['displayValue']} ({metric_data['percentile']} "
                  f"{metric_data.get('category', '')})")
        else:
            print(f"{metric_key}: {metric_data['percentile']} {metric_data.get('category', '')}")


def main():
    api_key = secret.api_key
    url_test = 'https://github.com/Ernestek/GeekHub-CRM/blob/main/CRM_Project/account/tasks.py'

    data = get_pagespeed_data(api_key, url_test)

    if data:
        # Обработка полученных данных
        page_title = data['lighthouseResult']['requestedUrl']
        print('Page Title: ', page_title)
        loading_status = data['loadingExperience']['overall_category']
        print('Loading Status: ', loading_status)

        # Показатели производительности
        if "metrics" in data["loadingExperience"]:
            print('DESKTOP')
            metrics = data["loadingExperience"]["metrics"]
            print_performance_metrics(metrics)

        # Показатели мобильной версии
        if "originLoadingExperience" in data:
            print('MOBILE')
            mobile_metrics = data["originLoadingExperience"]["metrics"]
            print_performance_metrics(mobile_metrics)

        # Print audit details
        audits = data["lighthouseResult"]["audits"]
        for audit_key, audit_data in audits.items():
            if audit_key == "screenshot-thumbnails":
                continue
            print("-" * 40)
            print("Audit Title:", audit_data["title"])
            if 'description' in audit_data:
                print("Description:", audit_data['description'])
            print("Score:", audit_data["score"])
            print("Display Value:", audit_data.get("displayValue"), "\n")
    else:
        print("Error")


if __name__ == "__main__":
    main()
