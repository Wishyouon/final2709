from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi as yta
from summa.summarizer import summarize
import re
import pytube

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/', methods=['POST'])
def process():
    # get data from HTML form
    url = request.form['vid_id']
    vid_id = re.findall(r'(?<=v=)[\w-]+', url)[0]
    summarization_percentage = int(request.form['summarization_percentage'])

    # use pytube to get video metadata
    yt = pytube.YouTube(url)
    title = yt.title
    thumbnail_url = yt.thumbnail_url

    try:
        # get transcript data
        data = yta.get_transcript(vid_id)

        # concatenate transcript text
        transcript = ''
        for value in data:
            for key, val in value.items():
                if key == 'text':
                    transcript += val + ' '

        # summarize the transcript using TextRank
        summary = summarize(transcript, ratio=summarization_percentage / 100)

        # execute Python code with data
        result = summary

        # render result as HTML
        return render_template('transcript.html', result=result, title=title, thumbnail_url=thumbnail_url, vid_id=vid_id, error_message=None)

    except Exception as e:
        # handle case where no transcript is available
        error_message = "Transcript not available for this video."
        return render_template('transcript.html', error_message=error_message, title=title, thumbnail_url=thumbnail_url, vid_id=vid_id, )

@app.route('/transcript')
def transcript():
    # get transcript data from query parameter
    final_tra = request.args.get('transcript')

    # get video ID and metadata from URL parameter
    vid_id = request.args.get('vid_id')
    title = request.args.get('title')
    thumbnail_url = request.args.get('thumbnail_url')

    # render transcript and video metadata on a new HTML page
    return render_template('transcript.html', transcript=final_tra, vid_id=vid_id, title=title, thumbnail_url=thumbnail_url, error_message=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

if __name__ == '__main__':
    app.run()

