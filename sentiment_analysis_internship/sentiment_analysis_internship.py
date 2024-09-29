from flask import Flask, request, render_template
import pandas as pd
import os
import requests
import time

app = Flask(__name__)
GROQ_API_KEY = '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'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
@app.route('/')
def home():
    return render_template('upload.html', scores=None)  


def extract_Reviews(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return {"error": "Unsupported file format"}
        

        if 'Review' not in df.columns:
            return {"error": "Review column not found"}
        Reviews = df['Review'].tolist()  
        return Reviews
    except Exception as e:
        return {"error": str(e)}


def groq_sentiment_analysis(Reviews):
    sentiments = {"positive": 0, "negative": 0, "neutral": 0}
    
    for review in Reviews:
        try:
            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "mixtral-8x7b-32768",  # Use the correct model ID from Groq
                "messages": [{"role": "user", "content": review}],
                "max_tokens": 100
            }
            response = requests.post(GROQ_API_URL, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                message_content = result.get('choices', [{}])[0].get('message', {}).get('content', '').lower()
                if "positive" in message_content:
                    sentiments['positive'] += 1
                elif "negative" in message_content:
                    sentiments['negative'] += 1
                else:
                    sentiments['neutral'] += 1
            elif response.status_code == 429:
                print("Rate limit hit. Review skipped.")
            else:
                print(f"Error analyzing review: Status Code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error processing review: {e}")

    return sentiments

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return render_template('upload.html', scores=None, error="No file provided")   
    file = request.files['file']
    file_path = f'./{file.filename}'
    file.save(file_path)
    Reviews = extract_Reviews(file_path)
    if isinstance(Reviews, dict) and "error" in Reviews:
        return render_template('upload.html', scores=None, error=Reviews["error"])
    sentiment_result = groq_sentiment_analysis(Reviews)
    os.remove(file_path)
    return render_template('upload.html', scores=sentiment_result)  # Pass the scores back to the template
if __name__ == '__main__':
    app.run(debug=True)
