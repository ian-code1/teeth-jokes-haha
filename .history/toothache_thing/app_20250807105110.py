from flask import Flask, jsonify, render_template
import threading
import time
import requests

app = Flask(__name__)
latest_jokes = []

def fetch_reddit_jokes():
    global latest_jokes
    headers = {'User-Agent': 'ToothJokeBot/0.1 by someone with questionable humor'}
    while True:
        try:
            url = 'https://www.reddit.com/r/dadjokes/search.json?q=tooth&restrict_sr=1&sort=new'
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            jokes = [child['data']['title'] for child in data['data']['children']]
            latest_jokes = jokes[:10]  # You only deserve 10. For now.
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
    app.run(port=5000)
