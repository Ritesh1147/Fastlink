from flask import Flask, request, jsonify, redirect, render_template
from redis_client import get_redis_connection
from utils import generate_short_code
import time

app = Flask(__name__)
r = get_redis_connection()

@app.route('/')
def home():
    return render_template('index.html')

# ✅ Create short link
@app.route('/create', methods=['POST'])
def create_url():
    data = request.get_json()
    original = data.get('url')
    if not original:
        return jsonify({'error': 'Missing URL'}), 400

    code = generate_short_code()
    r.set(f'short:{code}', original)

    # Store metadata
    r.hset(f'meta:{code}', 'created_at', time.time())
    r.hset(f'meta:{code}', 'clicks', 0)

    # Keep track of all codes for listing
    r.lpush('all_codes', code)

    return jsonify({
        'short_code': code,
        'short_url': f'/{code}',
        'original_url': original
    }), 201

# ✅ Redirect
@app.route('/<code>')
def redirect_url(code):
    url = r.get(f'short:{code}')
    if not url:
        return jsonify({'error': 'Not found'}), 404
    r.hincrby(f'meta:{code}', 'clicks', 1)
    return redirect(url)

# ✅ Get info for one short link
@app.route('/read/<code>')
def read_url(code):
    url = r.get(f'short:{code}')
    meta = r.hgetall(f'meta:{code}')
    if not url:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'original_url': url, 'meta': meta})

# ✅ Get all links
@app.route('/all')
def get_all_links():
    codes = r.lrange('all_codes', 0, -1)
    links = []
    for code in codes:
        url = r.get(f'short:{code}')
        meta = r.hgetall(f'meta:{code}')
        if url:
            links.append({
                'code': code,
                'original_url': url,
                'clicks': meta.get('clicks', 0)
            })
    return jsonify(links)

# ✅ Update
@app.route('/update/<code>', methods=['PUT'])
def update_url(code):
    data = request.get_json()
    new_url = data.get('url')
    if not r.exists(f'short:{code}'):
        return jsonify({'error': 'Not found'}), 404
    r.set(f'short:{code}', new_url)
    r.hset(f'meta:{code}', 'updated_at', time.time())
    return jsonify({'message': 'URL updated', 'new_url': new_url})

# ✅ Delete
@app.route('/delete/<code>', methods=['DELETE'])
def delete_url(code):
    r.delete(f'short:{code}', f'meta:{code}')
    return jsonify({'message': 'URL deleted'})

if __name__ == '__main__':
    app.run(debug=True)
