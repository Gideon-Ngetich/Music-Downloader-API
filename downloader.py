from flask import Flask, request, jsonify, send_file
from youtube_search_python import VideosSearch
from pytube import YouTube
import os

app = Flask(__name__)

# Endpoint to search for a song by name
@app.route('/search', methods=['GET'])
def search_song():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()['result'][0]
        return jsonify({
            'title': result['title'],
            'url': result['link']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['GET'])
def download_song():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'Video URL parameter is required'}), 400

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download()
        base, ext = os.path.splitext(out_file)
        mp3_file = base + '.mp3'
        os.rename(out_file, mp3_file)

        return send_file(mp3_file, as_attachment=True, download_name=f"{yt.title}.mp3")
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(mp3_file):
            os.remove(mp3_file)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
