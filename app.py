from flask import Flask, request, render_template
import instaloader
import urllib.request

app = Flask(__name__)

# create an instance of the Instaloader class
L = instaloader.Instaloader()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # get the post object from the URL of the Instagram post
    post_url = request.form['post_url']
    post = instaloader.Post.from_shortcode(L.context, post_url.split("/")[-2])

    # check if the post is a video or a reel
    if post.is_video:
        video_url = post.video_url
        thumbnail_url = post.url
    elif post.is_reel:
        video_url = post.video_url_with_version
        thumbnail_url = post.thumbnail_url
    else:
        return "Sorry, this post is not a video or a reel."

    # download the video
    L.context.log("Downloading video...")
    urllib.request.urlretrieve(video_url, f"{post.owner_username}_{post.shortcode}_video.mp4")

    # download the thumbnail
    L.context.log("Downloading thumbnail...")
    urllib.request.urlretrieve(thumbnail_url, f"{post.owner_username}_{post.shortcode}_thumbnail.jpg")

    # return the name of the downloaded file, a link to download it, and the thumbnail URL
    filename = f"{post.owner_username}_{post.shortcode}_video.mp4"
    return render_template('download.html', filename=filename, thumbnail_url=thumbnail_url, video_url=video_url)


if __name__ == '__main__':
    app.run(debug=True)
