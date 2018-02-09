import praw
import lib.functions as pe
reddit = praw.Reddit('CarpCS', user_agent='CarpCS BOT')
pe.get_list(reddit, 'mildyinteresting')
pe.get_post_content('hey')
