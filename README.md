🔗 FastLink – Redis URL Shortener

A simple URL Shortener using Flask and Redis to demonstrate CRUD operations in a Key-Value NoSQL database.

⚙️ Setup Instructions
1️⃣ Prerequisites

Python 3.8+

Redis installed and running locally

Windows users:

winget install --id Redis.Redis
redis-server

2️⃣ Clone this Repository
git clone https://github.com/<your-username>/redis-url-shortener.git
cd redis-url-shortener

3️⃣ Install Required Packages
pip install flask redis

4️⃣ Project Structure
redis-url-shortener/
│
├── app.py               # Flask backend (CRUD routes)
├── redis_client.py      # Redis connection
├── utils.py             # Short code generator
└── templates/
    └── index.html       # Web interface (CRUD buttons + table)

5️⃣ Run Redis
redis-server

6️⃣ Run the Flask App
python app.py

7️⃣ Open in Browser

Go to → http://localhost:5000

You can now:

Create short URLs

View all links in a table

Update/Delete existing links using buttons

Click short links to increase the count

🧪 API Endpoints (Optional)
Method	Endpoint	Description
POST	/create	Create a short link
GET	/all	View all links
PUT	/update/<code>	Update link
DELETE	/delete/<code>	Delete link
✅ Example (Using Postman)

POST /create

{ "url": "https://www.google.com" }


Response:

{
  "short_code": "AbC123",
  "short_url": "/AbC123",
  "original_url": "https://www.google.com"
}


That’s it! 🎉
Your Redis URL Shortener with full CRUD functionality is ready.
Author
Ritesh k Reddy
