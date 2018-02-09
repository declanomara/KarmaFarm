import praw
import lib.functions as pe
import time
import pickle
import os
from random import randint
from datetime import datetime
from pytz import timezone


#Create reddit user
reddit = praw.Reddit('User', user_agent='BOT')


banned = {} #Initialize dictionary of lists of banned ids
subs_add = ['announcements', 'Art', 'AskReddit', 'askscience', 'aww', 'blog', 'books', 'creepy', 'dataisbeautiful', 'DIY', 'Documentaries', 'EarthPorn', 'explainlikeimfive', 'food', 'funny', 'Futurology', 'gadgets', 'gaming', 'GetMotivated', 'gifs', 'history', 'IAmA', 'InternetIsBeautiful', 'Jokes', 'LifeProTips', 'listentothis', 'mildlyinteresting', 'movies', 'Music', 'news', 'nosleep', 'nottheonion', 'OldSchoolCool', 'personalfinance', 'philosophy', 'photoshopbattles', 'pics', 'science', 'Showerthoughts', 'space', 'sports', 'television', 'tifu', 'todayilearned', 'UpliftingNews', 'videos', 'worldnews'] #Initialize list of subreddits to be added to loaded subreddits (Debugging)
subs = [] #Initialize a list of subs
subs_count = {} #Initialize dictionary to store count of posts in each sub
banned_subs = [] #Initialize a list of banned subs

#Attempt to load saved counts from file
try:
    with open('counts.pkl', 'rb') as f:
        banned = pickle.load(f)
except EOFError:
    print('No banned post list saved')
except IOError:
    with open('counts.pkl', 'wb+') as f:
        print('Created banned save file')

#Attempt to load banned post list frome file
try:
    with open('banned.pkl', 'rb') as f:
        banned = pickle.load(f)
except EOFError:
    print('No banned post list saved')
except IOError:
    with open('banned.pkl', 'wb+') as f:
        print('Created banned save file')

#Attempt to load subs list
try:
    with open('subs.pkl', 'rb') as f:
        subs = pickle.load(f)
except EOFError:
    print('No subs saved')
except IOError:
    with open('subs.pkl', 'wb+') as f:
        print('Created subs save file')

for sub in subs_add:
    if not sub in subs:
        subs.append(sub)
        print(f'Added {sub} to pool')

for sub in subs: #Make a key for each sub in the count dictionary and set each count to 0
    subs_count.update({sub : 0})

print(f'Current pool: {subs}')
print(f'Initial counts: {subs_count}')


for sub in subs:
    if not sub in banned:
        print(f'Added ban array for {sub}')
        banned.update({sub : []})
print(f'Banned: {banned}')

def repost_auto(reddit, sub, banned = None, flair_id = None):
    posts = pe.get_list(reddit, sub) #Get list of top 100 posts
    num = 0
    while True:
        num = randint(0,99)
        if not num in banned:
            break
    post = posts[num]
    #print(post.is_self)
    return(pe.repost(reddit, sub, post))

def gen_subs(subs_count):
    subs_notmax = []
    for sub in subs_count:
        if subs_count[sub] <3 and not sub in banned_subs:
            subs_notmax.append(sub)
    if len(subs_notmax) == 0:
        for sub in subs_count:
            if not sub in banned_subs:
                subs_count[sub] = 0
                subs_notmax.append(sub)
    return(subs_notmax)

def blank_lines(i = 1):
    for x in range(0,i):
        print('\n')

initial_message = '''

    __ __                           ______
   / //_/___ __________ ___  ____ _/ ____/___ __________ ___
  / ,< / __ `/ ___/ __ `__ \/ __ `/ /_  / __ `/ ___/ __ `__
 / /| / /_/ / /  / / / / / / /_/ / __/ / /_/ / /  / / / / / /
/_/ |_\__,_/_/  /_/ /_/ /_/\__,_/_/    \__,_/_/  /_/ /_/ /_/



Automatic Karma Farming Bot Version 1.1
by Declan O'Mara
'''
blank_lines(100)
print(initial_message)

while __name__ == '__main__':
    choice_subs = gen_subs(subs_count)
    choice_num = randint(0, len(choice_subs) - 1)
    sub = choice_subs[choice_num]
    print(choice_subs)
    #print(sub)
    error_posting = False
    try:
        repost = repost_auto(reddit, sub, banned[sub])
        repostlink = repost.shortlink
        if not repost == None:
            subs_count[sub] += 1
    except praw.exceptions.APIException:
        print(f'Error Posting: Potentially banned from {sub}')
        banned_subs.append(sub)
        repostlink = 'Error getting link'
        error_posting = True


    with open('banned.pkl', 'wb+') as f:
        pickle.dump(banned, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open('subs.pkl', 'wb+') as f:
        pickle.dump(subs, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open('counts.pkl', 'wb+') as f:
        pickle.dump(subs_count, f, protocol=pickle.HIGHEST_PROTOCOL)

    time_est = datetime.now(timezone('EST'))
    success = (f'''
    {time_est}
    Successfully reposted to: {sub}
    Post: {repostlink}
    Current Counts: {subs_count}

    Sleeping for 10 minutes
    ''')

    failure = (f'''
    {time_est}
    Failed to repost to: {sub}
    Post: Error Posting
    Current Counts: {subs_count}

    Trying again

    ''')

    if not error_posting:
        print(success)
        time.sleep(600)
    else:
        print(failure)
