from flask import Flask, request, render_template, jsonify, redirect
import requests
app = Flask(__name__, template_folder= 'views')


token= "XXX"'

@app.route("/app/facebook/home")
def home():
    return render_template('home.html')

@app.route("/app/facebook/all/posts" , methods=('GET', 'POST'))
def get_posts():
    if request.method == 'GET':    
        req= requests.get('http://127.0.0.1:5000/api/facebook/all/posts')
        res = req.json()
        return render_template('posts.html', posts=res)
    else:
        message = request.form['message']
        if message:
            api_url="http://127.0.0.1:5000/api/facebook/do/post"
            create_data = {'message': message}
            req1 = requests.post(url=api_url, data=create_data)
            res = req1.json()
            return redirect("/app/facebook/all/posts")
        else:
            return redirect("/app/facebook/all/posts")
    return render_template('posts.html')


@app.route("/app/facebook/all/photos", methods=('GET', 'POST'))
def get_photos():
    if request.method == 'GET': 
        req= requests.get('http://127.0.0.1:5000/api/facebook/all/photos')
        res = req.json()
        return render_template('photos.html', photos=res)
    else:
        url = request.form['url']
        published = 'true'
        if url and published:
            api_url="http://127.0.0.1:5000/api/facebook/load/photo"
            create_data = {'url':url, 'published':published}
            req1 = requests.post(url=api_url, data=create_data)
            res = req1.json()
            return redirect("/app/facebook/all/photos")
        else:
            return redirect("/app/facebook/all/photos")
    return render_template('photos.html')



@app.route("/app/facebook/all/conversations")
def get_conversations():
    if request.method == 'GET':    
        req= requests.get('http://127.0.0.1:5000/api/facebook/all/conversations')
        res = req.json()
        return render_template('conversations.html', conversations=res)


@app.route("/app/facebook/show/conversation/<id>" , methods=('GET', 'POST'))
def get_conversation_id(id):
    if request.method == 'GET':    
        api_url = "http://127.0.0.1:5000/api/facebook/show/conversation/"+ str(id)
        req= requests.get(api_url)
        res = req.json()
        return render_template('conversation_id.html', conversation=res)
    else:
        message = request.form['message']
        if message:
            api_url="http://127.0.0.1:5000/api/facebook/do/message/" + str(id)
            create_data = {'message': message}
            req1 = requests.post(url=api_url, data=create_data)
            res = req1.json()
            return redirect("/app/facebook/show/conversation/"+str(id))
        else:
            return redirect("/app/facebook/show/conversation/"+str(id))
    return render_template('conversation_id.html')


@app.route('/app/facebook/delete/post/<id>')
def delete_post(id):
    api_url= "http://127.0.0.1:5000/api/facebook/delete/post/"+ str(id)
    send = requests.delete(url=api_url, headers={'authorization': "Bearer " + token})
    response = send.json()
    return redirect("/app/facebook/all/posts")

@app.route('/app/facebook/delete/photo/<id>')
def delete_photo(id):
    api_url= "http://127.0.0.1:5000/api/facebook/delete/photo/"+ str(id)
    send = requests.delete(url=api_url, headers={'authorization': "Bearer " + token})
    response = send.json()
    return redirect("/app/facebook/all/photos")
