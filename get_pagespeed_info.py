import requests

import secret
from audits import dict_audits


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
            print(audit_data['id'])

            print("Audit Title:", audit_data["title"])
            if 'description' in audit_data:
                print("Description:", audit_data['description'])
            print("Score:", audit_data["score"])
            print("Display Value:", audit_data.get("displayValue"), "\n")
            print('Details:')
            try:
                dict_audits[audit_data["id"]](audit_data)
            except KeyError:
                continue
    else:
        print("Error")


if __name__ == "__main__":
    main()
