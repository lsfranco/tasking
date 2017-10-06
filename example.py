import requests
from __init__ import TaskingManager

def process_urls(data):
    response = requests.get(data[1], allow_redirects=False, timeout=0.5)
    if response.status_code not in [200, 302]:
        return False
    return (response.status_code, response.elapsed.total_seconds())

def main():
    apps_urls = [
        ('google', 'https://google.com'),
        ('python', 'https://www.python.org'),
        ('example', 'http://httpstat.us/500'),
    ]

    get_names = lambda value: value[0]

    manager = TaskingManager(
        apps_urls, process_urls,
        threads=5, get_task_name=get_names,
        retries=3, retry_condition=False)
    result = manager.process_tasks()

    print result

if __name__ == '__main__':
    main()
