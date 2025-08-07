from flask import Flask, jsonify, render_template
import threading
import time
import praw

app = Flask(__name__)
latest_jokes = []

# Initialize Reddit client (USE YOUR ACTUAL KEYS HERE)
reddit = praw.Reddit(
    client_id="0u3QE0tPr80gMl4RdQP7zA",
    client_secret="SwMxdeoLIIbR5wkc5hdnPz0Ef-akwQ",
    user_agent="tooth-joke-bot by u/ian"
)

def fetch_reddit_jokes():
    global latest_jokes
    def grab_jokes():
        jokes = []
        subreddit = reddit.subreddit("dadjokes")
        for post in subreddit.search("tooth", sort="new", limit=10):
            title = post.title.strip()
            body = post.selftext.strip()
            if body:
                jokes.append(f"{title} — {body}")
            else:
                jokes.append(title)
        return jokes

    try:
        latest_jokes = grab_jokes()  # Get jokes immediately on start
    except Exception as e:
        latest_jokes = [f"Error fetching jokes: {e}"]

    while True:
        try:
            latest_jokes = grab_jokes()
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
