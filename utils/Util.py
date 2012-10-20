import datetime 
import random


def slugify(string):
    return string.replace(' ','-').lower()
    
def nice_date(dt):
    return dt.strftime('%a %d %B %Y')
    
def a_wrap(content='', href='#', id=None, className=None):
    output = '<a href="%s"' % href
    if id: output += ' id="%s"' % id
    if className: output += ' className="%s"' % className
    output += '>'
    output += content
    output += '</a>'
    
    return output

def random_string_of_numbers():
	return str(random.random())[2:]