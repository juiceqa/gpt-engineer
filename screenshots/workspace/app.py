import requests
import xml.etree.ElementTree as ET
from typing import List
from flask import Flask, render_template, request, send_file
from screenshot import ScreenshotManager, PDFGenerator
from database import DatabaseManager

app = Flask(__name__)
screenshot_manager = ScreenshotManager()
pdf_generator = PDFGenerator()
db_manager = DatabaseManager()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/screenshots', methods=['POST'])
def get_screenshots():
    sitemap_url = request.form['sitemap_url']
    screenshots = []
    for url in get_urls_from_sitemap(sitemap_url):
        screenshot = screenshot_manager.take_screenshot(url)
        screenshots.append(screenshot)
    pdf_generator.generate_pdf(screenshots, 'screenshots.pdf')
    return send_file('screenshots.pdf')


def get_urls_from_sitemap(sitemap_url: str) -> List[str]:
    try:
        response = requests.get(sitemap_url, timeout=5)
        response.raise_for_status()  # Raise an exception if the request was not successful
        sitemap_content = response.content
        root = ET.fromstring(sitemap_content)
        urls = []
        for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is not None and loc.text:
                urls.append(loc.text)
        return urls
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occurred during the request
        print(f"Error fetching sitemap from {sitemap_url}: {e}")
        return []


if __name__ == '__main__':
    app.run()
