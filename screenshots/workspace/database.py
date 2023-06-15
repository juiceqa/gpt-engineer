"""
This module provides database connectivity
"""

import mysql.connector as mysql
from screenshot import Screenshot


class DatabaseManager:
    def __init__(self):
        self.connection = self._create_connection()

    def _create_connection(self):
        return mysql.connector.connect(
            host='localhost',
            user='gglick',
            password='gtgk*686',
            database='screenshots'
        )

    def store_screenshot(self, screenshot: Screenshot):
        cursor = self.connection.cursor()
        query = "INSERT INTO screenshots (url, image, width, height) VALUES (%s, %s, %s, %s)"
        values = (screenshot.url, screenshot.image, screenshot.width, screenshot.height)
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def get_screenshots(self):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT url, image, width, height FROM screenshots"
        cursor.execute(query)
        results = cursor.fetchall()
        screenshots = []
        for row in results:
            screenshot = Screenshot(
                url=row['url'],
                image=row['image'],
                width=row['width'],
                height=row['height']
            )
            screenshots.append(screenshot)
        cursor.close()
        return screenshots
