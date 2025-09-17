# YouTube Comment Analyzer

A web application that helps YouTube content creators analyze the sentiment of comments on their videos. The application scrapes comments from a YouTube video, analyzes them for positive and negative sentiment, and sends the results to the user's email.

## Features

- **Comment Scraping**: Fetches comments from any public YouTube video
- **Sentiment Analysis**: Classifies comments as positive or negative using NLP
- **Email Notifications**: Sends analysis results directly to the user's email
- **Interactive UI**: Clean and responsive web interface
- **Exportable Results**: Exports comments to Excel files for further analysis

## Prerequisites

- Python 3.8 or higher
- Google Account (for YouTube Data API)
- Gmail account (for sending emails)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd youtube-comment-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your credentials:
   - `YOUTUBE_API_KEY`: Get it from [Google Cloud Console](https://console.cloud.google.com/)
   - `EMAIL_USER`: Your Gmail address
   - `EMAIL_PASSWORD`: Your Gmail App Password (not your regular password)
   - `SECRET_KEY`: A secret key for Flask sessions

### 4. Get YouTube Data API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Add the API key to your `.env` file

### 5. Set Up Gmail for Sending Emails

1. Go to your Google Account settings
2. Navigate to Security > App passwords
3. Generate a new app password for your application
4. Use this password in the `.env` file as `EMAIL_PASSWORD`

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Enter a YouTube video URL and your email address to start the analysis

## How It Works

1. The application extracts the video ID from the provided YouTube URL
2. It uses the YouTube Data API to fetch comments from the video
3. Comments are processed and analyzed for sentiment using TextBlob
4. Results are categorized into positive and negative comments
5. The analysis results are sent to the provided email address as Excel attachments

## Project Structure

```
youtube-comment-analyzer/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
├── templates/             # HTML templates
│   ├── base.html
│   └── index.html
└── utils/                 # Utility modules
    ├── comment_analyzer.py  # Sentiment analysis
    ├── comment_scraper.py   # YouTube comment scraping
    └── mail_sender.py      # Email sending functionality
```

## Advanced Features

- **Custom Sentiment Analysis**: The application currently uses TextBlob for sentiment analysis, but you can easily integrate more advanced models like VADER or BERT
- **Batch Processing**: The code is designed to handle large numbers of comments efficiently
- **Responsive Design**: Works on both desktop and mobile devices

## Troubleshooting

- **API Quota Exceeded**: The YouTube Data API has daily quotas. If you exceed them, you'll need to wait or request a quota increase
- **Email Not Sending**: Ensure you've set up an App Password correctly and that your Gmail account allows less secure apps (if enabled)
- **No Comments Found**: Some videos have comments disabled or restricted

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [TextBlob](https://textblob.readthedocs.io/) - Sentiment analysis
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- [YouTube Data API](https://developers.google.com/youtube/v3) - For accessing YouTube data
