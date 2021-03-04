import requests
from operator import itemgetter

from plotly.graph_objs import Bar
from plotly import offline

# Создание вызова API  и сохранение ответа.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Обработка информации о каждой статье.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # Создание отдельного вызова API для каждой статьи.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    # Построение словаря для каждой статьи.
    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
        }
    except KeyError:
        # Это специальный пост YC с отключенными комментариями.
        continue
    else:

        submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# Создание списков для построения графиков.

titles, num_comments, discus_links = [], [], []
for sd in submission_dicts:
    title = sd['title']
    num_comment = sd['comments']
    hn_link = sd['hn_link']
    discus_link = f"<a href='{hn_link}'>{title[:15]}</a>"

    titles.append(title)
    num_comments.append(num_comment)
    discus_links.append(discus_link)

# Построение визуализации.
data = [{
    'type': 'bar',
    'x': discus_links,
    'y': num_comments,
    'hovertext': titles,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
}]

my_layout = {
    'title': 'Most-Comments on Hacker News',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Discussions',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
    'yaxis': {
        'title': 'Number of Comments',
        'titlefont': {'size': 24},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='hn_python_disc_comm_vis.html')
