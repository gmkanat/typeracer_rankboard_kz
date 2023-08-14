import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import csv
import sys

URL = 'https://typeracerdata.com/leaders?min_races=300&min_texts=100&sort=wpm_top10&rank_start={start}&rank_end={end}'
USER_URL = "https://data.typeracer.com/users?id=tr:{username}&universe=play"

def write_header_to_csv():
    with open('data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['#', 'Name', 'Handle', 'Recent Average WPM', 'Best Game WPM', 'Certified WPM'])


def write_data_to_csv(data, counter):
    recent_avg_wpm = round(data['tstats']['recentAvgWpm'], 2)
    best_game_wpm = round(data['tstats']['bestGameWpm'], 2)
    cert_wpm = round(data['tstats']['certWpm'], 2)

    with open('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([counter[0], data['name'], data['id'][3:], recent_avg_wpm, best_game_wpm, cert_wpm])


def get_user_data(url, counter):
    response = requests.get(url)
    data = response.json()
    recent_avg_wpm = data['tstats']['recentAvgWpm']
    country = data['country']
    if country == 'kz':
        write_data_to_csv(data, counter)
        counter[0] += 1
        print(f"Recent Average WPM: {recent_avg_wpm}")


def get_data(url, step=100, max_range=40000):
    counter = [1]
    for start in range(1, max_range, step):
        end = start + step - 1
        print(start, end)
        sys.stdout.flush()
        response = requests.get(url.format(start=start, end=end))
        soup = BeautifulSoup(response.text, 'html.parser')
        username_tags = soup.find_all('a', href=True)
        for tag in username_tags:
            href = tag['href']
            parsed_url = urlparse(href)
            query_params = parse_qs(parsed_url.query)
            username = query_params.get('username', [''])[0]
            if username:
                get_user_data(USER_URL.format(username=username), counter)
                print(f"Username: {username}")


if __name__ == '__main__':
    write_header_to_csv()
    get_data(URL)

