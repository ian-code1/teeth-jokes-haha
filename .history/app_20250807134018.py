from flask import Flask, jsonify, render_template
import threading
import time
import requests

app = Flask(__name__)
latest_jokes = []

def fetch_reddit_jokes():
    global latest_jokes
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

    while True:
        try:
            url = 'https://www.reddit.com/r/dadjokes/search.json?q=tooth&restrict_sr=1&sort=new'
            res = requests.get(url, headers=headers)
            data = res.json()
            jokes = []

            for post in data['data']['children']:
                post_data = post['data']
                title = post_data.get('title', '').strip()
                body = post_data.get('selftext', '').strip()

                if body:
                    jokes.append(f"{title} — {body}")
                else:
                    jokes.append(title)  # Some are one-liners

            latest_jokes = jokes[:10]  # Or however many you like
        except Exception as e:
            latest_jokes = [f"Error fetching jokes: {e}"]
        time.sleep(10)

@app.route('/jokes')
def get_jokes():
    return jsonify({'jokes': latest_jokes})
    
@app.route('/')
def serve_html():
    return render_template('toothache.html') 

if __name__ == '__main__':
    threading.Thread(target=fetch_reddit_jokes, daemon=True).start()
    app.run(debug=True)
