import praw

def get_list(reddit, sub, time_filter = 'all', maximum = 100):
    listgen = reddit.subreddit(sub).top(time_filter)
    postlist = []
    for i in range(0,maximum):
        post = next(listgen)
        postlist.append(post)

    return(postlist)

def get_post_by_id(reddit, post_id):
    return(praw.models.Submission(reddit, id = post_id))

def get_post_content(post):
    if(post.is_self):
        return({'title': post.title, 'text':post.selftext, 'is_self': post.is_self})
    else:
        return({'title': post.title, 'url':post.url, 'is_self': post.is_self})

def submit_dict(reddit, sub, post, flair_id = None):
    if post['is_self']:
        post = reddit.subreddit(sub).submit(post['title'], selftext = post['text'])
        if not flair_id == None:
            post.flair.select(flair_id)
        return(post)
    else:
        post = reddit.subreddit(sub).submit(post['title'], url = post['url'])
        if not flair_id == None:
            post.flair.select(flair_id)
        return(post)

def repost(reddit, sub, post, flair_id = None):
    if(post.is_self):
        post = reddit.subreddit(sub).submit(post.title, selftext = post.selftext)
        if not flair_id == None:
            post.flair.select(flair_id)
        return(post)
    else:
        post = reddit.subreddit(sub).submit(post.title, url = post.url)
        if not flair_id == None:
            post.flair.select(flair_id)
        return(post)
