from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import boto3

app = Flask(__name__)

# Folder where screenshots are saved
SCREENSHOTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../screenshots'))
# S3 Setup
s3_client = boto3.client('s3', region_name='us-west-2')
BUCKET_NAME = "digital-diary"


@app.route('/generate-presigned-url', methods=['POST'])
def generate_presigned_url():
    try:
        data = request.json
        file_name = data.get('file_name')
        username = data.get('username')

        if not file_name or not username:
            return jsonify({"error": "Missing file_name or username"}), 400

        object_name = f"{username}/{file_name}"
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )

        return jsonify({"url": url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/')
def index():
    """Displays the latest screenshot from S3 using a pre-signed URL."""
    # List all files in the bucket with a specific prefix ("screenshot_")
    prefix = "ndevasia/screenshot_"
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    print(response)
    
    if 'Contents' in response:
        # Filter files with prefix "screenshot_"
        files = [file for file in response['Contents'] if file['Key'].startswith(prefix)]
        
        if files:
            # Sort the files by LastModified to get the latest one
            latest_file = sorted(files, key=lambda x: x['LastModified'], reverse=True)[0]['Key']
        else:
            latest_file = None
    else:
        latest_file = None

    if latest_file:
        # Generate a pre-signed URL for the latest file
        screenshot_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': latest_file},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return render_template('layout.html', screenshot_url=screenshot_url)
    else:
        return render_template('layout.html', screenshot_url=None)

@app.route('/screenshots/<filename>')
def get_screenshot(filename):
    """Serves the screenshot file."""
    return send_from_directory(SCREENSHOTS_FOLDER, filename)


# In a real app, you'd use a database. Here, we'll use a dict for simplicity, but you must replace this
users = {}
partners = {}
media_items = {}
games = {}
journal_entries = {}

# API Endpoints
# User Information
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    """
    Retrieves user details based on user_id.
    """
    if user_id in users:
         user = users[user_id]
         return jsonify({
            'user_id': user.user_id,
            'username': user.username
            #'password': user.password, # Never return the password!
        }), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/users/<int:user_id>/partners', methods=['GET'])
def get_partner_info(user_id):
    """
    Retrieves partners associated with a given user_id.
    """
    # **Implement logic to fetch partners associated with user_id**
    # For example, if partners are associated with a user through a separate table in the database you will need to query it here.
    # The sources do not define this relationship so you will need to determine how this association works
    # This is placeholder code:
    user_partners = [partner for partner in partners.values()]
    return jsonify([{'partner_id': p.partner_id, 'name': p.name} for p in user_partners if p]), 200
    #return jsonify({'message': 'Partners not found for user'}), 404

@app.route('/users/<int:user_id>/media', methods=['GET'])
def get_media(user_id):
    """
    Retrieves all media associated with a given user_id.
    """
    user_media = [media for media in media_items.values() if media.owner_user_id == user_id]
    return jsonify([{'media_id':m.media_id, 'type':m.type, 'media_url':m.media_url, 'timestamp': str(m.timestamp), 'owner_user_id': m.owner_user_id, 'members_present': m.members_present} for m in user_media]), 200
    #return jsonify({'message': 'Media not found for user'}), 404


@app.route('/users/<int:user_id>/partners/<int:partner_id>/media', methods=['GET'])
def get_partner_media(user_id, partner_id):
    """
    Retrieves media shared with a given partner_id by a user_id.
    """
    # **Implement logic to fetch media associated with a user and partner.**
    # The source does not specify how users are related to media, so you will need to define this relationship
    # This is placeholder code:
    user_partner_media = [media for media in media_items.values() if media.owner_user_id == user_id and partner_id in (media.members_present if media.members_present else [])]
    return jsonify([{'media_id':m.media_id, 'type':m.type, 'media_url':m.media_url, 'timestamp': str(m.timestamp), 'owner_user_id': m.owner_user_id, 'members_present': m.members_present} for m in user_partner_media]), 200
    #return jsonify({'message': 'Media not found for user and partner'}), 404


@app.route('/users/<int:user_id>/games', methods=['GET'])
def get_game(user_id):
    """
    Retrieves games associated with a given user_id.
    """
    user_games = [game for game in games.values() if game.owner_user_id == user_id]
    return jsonify([{'game_id': g.game_id, 'game_name': g.game_name, 'game_url': g.game_url, 'timestamp': str(g.timestamp), 'owner_user_id': g.owner_user_id} for g in user_games]), 200
    #return jsonify({'message': 'Games not found for user'}), 404

@app.route('/users/<int:user_id>/journal', methods=['GET'])
def get_journal(user_id):
    """
    Retrieves journal entries associated with a given user_id.
    """
    user_journal_entries = [entry for entry in journal_entries.values() if entry.owner_user_id == user_id]
    return jsonify([{'entry_id': j.entry_id, 'text': j.text, 'timestamp': str(j.timestamp), 'owner_user_id': j.owner_user_id} for j in user_journal_entries]), 200
    #return jsonify({'message': 'Journal entries not found for user'}), 404

# Journal Entry Editing
@app.route('/journal', methods=['POST'])
def create_journal_entry():
    """
    Creates a new journal entry.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'text' not in data:
          return jsonify({'message': 'Missing user_id or text in request'}), 400
    entry_id = len(journal_entries) + 1 # Replace with a proper id
    new_entry = JournalEntry(entry_id=entry_id, text=data['text'], timestamp=datetime.now(), owner_user_id=data['user_id'])
    journal_entries[entry_id] = new_entry
    return jsonify({'message': 'Journal entry created', 'entry_id': entry_id}), 201


@app.route('/journal/<int:entry_id>', methods=['PUT'])
def edit_journal_entry(entry_id):
    """
    Updates a journal entry's text given an entry_id.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'text' not in data:
        return jsonify({'message': 'Missing user_id or text in request'}), 400

    if entry_id in journal_entries and journal_entries[entry_id].owner_user_id == data['user_id']:
        journal_entries[entry_id].text = data['text']
        return jsonify({'message': 'Journal entry updated'}), 200
    return jsonify({'message': 'Journal entry not found or user not authorized'}), 404

@app.route('/journal/<int:entry_id>', methods=['DELETE'])
def delete_journal_entry(entry_id):
    """
    Deletes a journal entry given an entry_id.
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'message': 'Missing user_id in request'}), 400
    if entry_id in journal_entries and journal_entries[entry_id].owner_user_id == data['user_id']:
        del journal_entries[entry_id]
        return jsonify({'message': 'Journal entry deleted'}), 200
    return jsonify({'message': 'Journal entry not found or user not authorized'}), 404

# Media Deletion
@app.route('/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    """
    Deletes a media item given a media_id
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'message': 'Missing user_id in request'}), 400
    if media_id in media_items and media_items[media_id].owner_user_id == data['user_id']:
        del media_items[media_id]
        return jsonify({'message': 'Media deleted'}), 200
    return jsonify({'message': 'Media not found or user not authorized'}), 404

# Game Deletion
@app.route('/game/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    """
    Deletes a game given a game_id
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
         return jsonify({'message': 'Missing user_id in request'}), 400
    if game_id in games and games[game_id].owner_user_id == data['user_id']:
        del games[game_id]
        return jsonify({'message': 'Game deleted'}), 200
    return jsonify({'message': 'Game not found or user not authorized'}), 404

# Authentication
@app.route('/login', methods=['POST'])
def login():
    """
    Authenticates user credentials.
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
          return jsonify({'message': 'Missing username or password in request'}), 400
    username = data['username']
    password = data['password']

    for user in users.values():
        if user.username == username and user.password == password:
           return jsonify({'message': 'Login successful', 'user_id': user.user_id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """
    Logs out a user given a user_id
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({'message': 'Missing user_id in request'}), 400
    # In a real app you would manage user sessions here.
    return jsonify({'message': 'Logged out'}), 200


# Overlays and Recordings
@app.route('/screenshot', methods=['POST'])
def screenshot():
    """
    Handles a screenshot.
    """
    data = request.get_json()
    if not data or 'user_id' not in data or 'media' not in data:
          return jsonify({'message': 'Missing user_id or media in request'}), 400
    # Implement saving the screenshot and associate it with the user.
    media_id = len(media_items)+1 # Replace with proper logic for generating the media id
    new_media = Media(media_id=media_id, type='screenshot', media_url = data['media'], timestamp = datetime.now(), owner_user_id = data['user_id'])
    media_items[media_id] = new_media

    return jsonify({'message': 'Screenshot recorded'}), 201

@app.route('/recordAudio', methods=['POST'])
def record_audio():
    """
    Handles audio recording.
    """
    data = request.get_json()
    if not data or 'user_id' not in data:
          return jsonify({'message': 'Missing user_id in request'}), 400
    # Implement saving the audio and associate it with the user.
    media_id = len(media_items) + 1 # Replace with proper logic for generating media_id
    new_media = Media(media_id=media_id, type='audio', media_url = "/path/to/recorded.mp3", timestamp = datetime.now(), owner_user_id = data['user_id']) #  you will need to figure out how to get and store the file
    media_items[media_id] = new_media

    return jsonify({'message': 'Audio recorded'}), 201


if __name__ == '__main__':
    # Create some dummy data for testing purposes
    users[1] = User(user_id=1, username="testuser", password="password123")
    users[2] = User(user_id=2, username="testuser2", password="password456")
    partners = Partner(partner_id=101, name="Alice")
    media_items = Media(media_id=201, type="screenshot", media_url="/path/to/image.png", timestamp=datetime.now(), owner_user_id=1, members_present=)
    games = Game(game_id=301, game_name="Cool Game", game_url="game.url.com", timestamp=datetime.now(), owner_user_id=1)
    journal_entries = JournalEntry(entry_id=401, text="My first journal entry", timestamp=datetime.now(), owner_user_id=1)
    app.run(debug=True)