from flask import Flask, request, jsonify
from flask_restplus import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)
token = "XXX"


@api.route('/api/facebook/all/posts')
class FacebookPosts(Resource):
    def get(self):
        api_url = "https://graph.facebook.com/me?fields=posts"
        req = requests.get(api_url, headers={'authorization': "Bearer " + token})
        res = req.json()
        return res['posts']

@api.route('/api/facebook/all/photos')
class FacebookPhotos(Resource):
    def get(self):
        api_url = "https://graph.facebook.com/me?fields=albums.fields(photos.fields(source)) "
        req = requests.get(api_url, headers={'authorization': "Bearer " + token})
        res = req.json()
        list_photos=[]
        for i in res['albums']['data']:
            for j in i['photos']['data']:
                result = {'source':j['source'], 'id':j['id']}
                list_photos.append(result)
        return list_photos


@api.route('/api/facebook/do/post')
class FacebookDoPost(Resource):
    def post(self):
        api_url="https://graph.facebook.com/me/feed"
        message = request.form['message']
        create_data = {"message":message}
        send = requests.post(url=api_url, json=create_data, headers={'authorization': "Bearer " + token})
        response = send.json()
        return response


@api.route('/api/facebook/all/conversations')
class FacebookConversations(Resource):
    def get(self):
        api_url= "https://graph.facebook.com/me/conversations?fields=senders"
        req = requests.get(api_url, headers={'authorization': "Bearer " + token})
        res = req.json()
        list_conversation = []
        for i in res['data']:
            data= {'id_conversation': i['id'], 'participant': i['senders']['data'][0]['name']}
            list_conversation.append(data)
        return list_conversation

@api.route('/api/facebook/show/conversation/<id>')
class FacebookConversationId(Resource):
    def get(self, id):
        api_url= "https://graph.facebook.com/" +str(id)+ "?fields=messages{message,created_time,from}"
        req = requests.get(api_url, headers={'authorization': "Bearer " + token})
        res = req.json()
        list_message = []
        for i in res['messages']['data']:
            data = {'message': i['message'], 'time': i['created_time'], 'from': i['from']['name']}
            list_message.append(data)
        return list_message

@api.route('/api/facebook/do/message/<id>')
class FacebookDoMessage(Resource):
    def post(self, id):
        api_url="https://graph.facebook.com/" + str(id)+ "/messages"
        message = request.form['message']
        create_data = {"message":message}
        send = requests.post(url=api_url, json=create_data, headers={'authorization': "Bearer " + token})
        response = send.json()
        return response


@api.route('/api/facebook/load/photo')
class FacebookLoadPhoto(Resource):
    def post(self):
        api_url="https://graph.facebook.com/234670333835708/photos"
        url = request.form['url']
        create_data = {'url':url, 'published':'true'}
        send = requests.post(url=api_url, json=create_data, headers={'authorization': "Bearer " + token})
        response = send.json()
        return response

@api.route('/api/facebook/delete/post/<id>')
class FacebookDeletePhoto(Resource):
    def delete(self, id):
        api_url="https://graph.facebook.com/"+str(id)
        send = requests.delete(url=api_url, headers={'authorization': "Bearer " + token})
        response = send.json()
        return response


@api.route('/api/facebook/delete/photo/<id>')
class FacebookDeletePhoto(Resource):
    def delete(self, id):
        api_url="https://graph.facebook.com/"+str(id)
        send = requests.delete(url=api_url, headers={'authorization': "Bearer " + token})
        response = send.json()
        return response


if __name__ == '__main__':
    app.run(debug=True)
