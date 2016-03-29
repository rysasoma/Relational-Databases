# Database access functions for the web forum.
# 

import time
import psycopg2
## Database connection


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    connection = psycopg2.connect("dbname=forum")
    c = connection.cursor()
    query = "SELECT time, content from posts ORDER BY time DESC"
    c.execute(query)
    posts = ({'content':str(row[1]), 'time':str(row[0])} for row in c.fetchall())
    connection.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    connection = psycopg2.connect("dbname=forum")
    c = connection.cursor()
    c.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
    connection.commit()
    connection.close()
