
import requests
import sqlite3

from dotenv import load_dotenv
import os

def save_user_data(access_token):
    url = f"https://graph.facebook.com/v22.0/me?fields=id%2Cname%2Cposts%2Cpicture&access_token={access_token}"
    response = requests.get(url)

    posts = response.json()['posts']['data'][:25]
    picture = response.json()['picture']['data']['url']

  
    
    comments = {}
    for i in posts:
        comments_response = requests.get(f"https://graph.facebook.com/v22.0/{i['id']}?fields=comments&access_token={access_token}")
        comments[i['id']] = comments_response.json()
    id = response.json()['id']
    name = response.json()['name']

    followers_url = f"https://graph.facebook.com/v22.0/me/friends?access_token={access_token}"
    followers_response = requests.get(followers_url)
    followers = followers_response.json()['summary']['total_count']

    likes_url = f"https://graph.facebook.com/v22.0/me/likes?access_token={access_token}"
    likes_url = requests.get(likes_url)
    likes = [i['name'] for i in likes_url.json()['data']]

    # saving all user related data to the database
    conn = sqlite3.connect('users.db')
    
    cursor = conn.cursor()

    table ="""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        picture TEXT,
        followers INTEGER,
        likes TEXT,
        posts TEXT,
        comments TEXT
    )"""

    cursor.execute(table)

    cursor.execute("INSERT INTO users (id, name, picture, followers, likes, posts ,comments) VALUES (?, ?, ?, ?, ?,?,?)", (id, name, picture, followers, str(likes),str(posts),str(comments)))
    print("Data Inserted in the table: ") 
 
    conn.commit() 
    conn.close()


def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    column_name = []
    for column in cursor.execute("SELECT * FROM users").description:
        column_name.append(column[0])
        

    conn.close()
    return column_name,users

def get_user_data(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


if __name__ == '__main__':  
    save_user_data('EAAQ30YZAm2K4BOzfkePMr8T5pBNAI5PZBiuMw0nJ4lpudFvNRQY2HnH4fejQhZCsJSSZBepoPOlRZAMmEVBXvy4p9kWRazI8xsfBQUsj9NH6V4349sEyKdcNIYGOrrlJo4XFE9ZC4jZBwfkbxreZBQZBHzlk5gRrHgRPpMFmXXOlzZC6ZB4qUKmy2lZCfkAqZBnSpfFSDDe3JU0W1j8QesVCx2QPpQAOH81JQqIxLPCMRPePTZC30mAWetSZAiF')