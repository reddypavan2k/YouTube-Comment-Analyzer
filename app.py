import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from utils.comment_analyzer import analyze_comments
from utils.mail_sender import send_email_with_attachments
from utils.comment_scraper import get_video_comments
import pandas as pd
import tempfile
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# In-memory storage for analysis results (in production, use a database)
analysis_results = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form.get('video_url')
    email = request.form.get('email')
    
    if not video_url or not email:
        return jsonify({'error': 'Please provide both YouTube URL and email address'}), 400
    
    # Start a background task for comment scraping and analysis
    thread = threading.Thread(
        target=process_comments,
        args=(video_url, email)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'message': 'Analysis started! You will receive an email when it\'s complete.',
        'status': 'processing'
    })

def process_comments(video_url, email):
    try:
        # Scrape comments
        comments_df = get_video_comments(video_url)
        
        if comments_df is None or comments_df.empty:
            raise Exception("No comments found or error in scraping comments")
        
        # Analyze comments
        results = analyze_comments(comments_df)
        
        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            all_comments_path = os.path.join(temp_dir, 'all_comments.xlsx')
            positive_comments_path = os.path.join(temp_dir, 'positive_comments.xlsx')
            negative_comments_path = os.path.join(temp_dir, 'negative_comments.xlsx')
            
            # Save DataFrames to Excel files
            results['all_comments'].to_excel(all_comments_path, index=False)
            results['positive_comments'].to_excel(positive_comments_path, index=False)
            results['negative_comments'].to_excel(negative_comments_path, index=False)
            
            # Prepare email
            subject = f"YouTube Comments Analysis for {video_url}"
            body = """
            <h2>YouTube Comments Analysis Report</h2>
            <p>Please find attached the analysis of the YouTube video comments you requested.</p>
            <p>Summary:</p>
            <ul>
                <li>Total Comments: {}</li>
                <li>Positive Comments: {}</li>
                <li>Negative Comments: {}</li>
                <li>Neutral Comments: {}</li>
            </ul>
            <p>Thank you for using our service!</p>
            """.format(
                len(results['all_comments']),
                len(results['positive_comments']),
                len(results['negative_comments']),
                len(results['all_comments']) - len(results['positive_comments']) - len(results['negative_comments'])
            )
            
            # Send email with attachments
            attachments = [
                (all_comments_path, 'all_comments.xlsx'),
                (positive_comments_path, 'positive_comments.xlsx'),
                (negative_comments_path, 'negative_comments.xlsx')
            ]
            
            send_email_with_attachments(
                to_email=email,
                subject=subject,
                html_content=body,
                attachments=attachments
            )
            
    except Exception as e:
        print(f"Error processing comments: {str(e)}")
        # In a production app, you might want to send an error email

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    
    # Run the app
    app.run(debug=True, port=5001)
