#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

# Log File to URLs
def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++

  # The server_name is whatever follows the first underbar
  # filename: animal_code.google.com
  # _(\S +) | _([\w.]+) to extract server name
  match = ''
  regexp = ''
  regexp = r'_([\w.]+)'
  match = re.search(regexp, filename)
  server_name = match.group(1)

  # Open the filename and returns a file handle that can be
  # used to read, write or append a file.
  file = open(filename, 'rU')
  """for line in file:
    print line, # trailing ',' so print does not add an end-of-line
                # char since line already includes the end-of line"""
  # The file.read() method reads the whole file into a single
  # string.
  file_text = file.read()

  # Store all urls which contains 'puzzle' somewhere in the url
  puzzle_urls = []
  # \S (upper case S) matches any non-space char
  puzzle_urls = re.findall(r'GET\s(\S+puzzle\S+)', file_text)
  file.close()

  # Screen out urls that appear more than once
  unique_puzzle_urls = []
  for puzzle_url in puzzle_urls:
    if not puzzle_url in unique_puzzle_urls:
      unique_puzzle_urls.append(puzzle_url)

  # Combine the path from each url with the server name
  # to form a full url, e.g.
  # http://<server_name><puzzle_url>
  full_unique_urls = []
  full_url = ''
  full_url += 'http://' + server_name
  for puzzle_url in unique_puzzle_urls:
    full_unique_urls.append(full_url + puzzle_url)

  # Sort full_unique_urls and return it without
  # needing creating a new list using
  # full_unique_urls.sort() function.
  # For the first puzzle(animal), the urls can be
  # sorted alphabetically to order the images
  # correctly. In the sort, the whole url is used.
  # For second puzzle(place), if the url ends in the pattern
  # "-wordchars-wordchars.jpg",
  # e.g. "http://example.com/foo/puzzle/bar-abab-baaa.jpg",
  # then  the url should be represented by the second word
  # in the sort (e.g. "baaa").
  # That's why regular expression for filtering out the second word is:
  # \/\w+-\w+-(\w+).jpg
  # To differentiate 2 types of urls which are
  # 1)http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babe.jpg
  # 2)http://example.com/foo/puzzle/bar-abab-baaa.jpg (For the second puzzle)
  # \/\w+-\w+-\w+.jpg regular expression is used to check the ending whether the url belongs to
  # the second puzzle pieces or not. As a test full_unique_urls[0] is used.
  regexr = ''
  regexr = r'\/\w+-\w+-\w+.jpg'
  if re.search(regexr, full_unique_urls[0]):
    full_unique_urls.sort(key = sortCustomly)
  else:
    full_unique_urls.sort()
  return full_unique_urls

# Download Images Puzzle Chunks
def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++

  # Create a directory dest_dir if it does not exist
  # informing the user
  if os.path.exists(dest_dir):
    print 'Destination directory is validated!'
  else:
    print 'There was not specified destination directory but now created!'
    os.mkdir(dest_dir)

  # Make sure that dest_dir points to the inside of the
  # dest_dir. dest_dir[-1] is the last character of the
  # dest_dir.
  if not dest_dir[-1] == '/':
    dest_dir += '/'

  # Downloads the url data (jpg) with specified local image
  # file name as 'img#' where # represents img_count into the
  # dest_dir.
  img_count = 0
  for img_url in img_urls:
    # str(img_count) otherwise TypeError: cannot concatenate
    # 'str' and 'int' objects
    urllib.urlretrieve(img_url, dest_dir + 'img' + str(img_count))
    # Downloading could be slow and it is nice to
    # have some indication that the program
    # is working.
    print 'Retrieving... ' + 'img' + str(img_count) + ' to ' + dest_dir
    img_count += 1
  print 'Downloading puzzle images completed!'

  # Each image is a little vertical slice from the original.
  # To put the slices together to re-create the original
  # we need html file with img tag.
  # Create an index.html in the dest_dir to show each local image file.
  # The img tags should all be on one line together without seperation so
  # that the browser displays all the slices together seamlessly.
  # Create image files names list before creating html file otherwise
  # index.html file name also is added to the image files names list.
  img_files = []
  img_files = os.listdir(dest_dir)
  img_files.sort(key = sortHumanly)
  html_file = open(dest_dir + 'index.html', 'w')
  html_content = ''
  html_content = '<verbatim>\n<html>\n<body>\n'
  img_tag = ''
  img_source = ''
  for img_source in img_files:
    img_tag += '<img src=\"' + dest_dir + img_source + '\">'
  html_content += img_tag
  html_content += '\n</body>\n</html>'
  html_file.write(html_content)
  print 'index.html is created! Open it in a browser to reveal the puzzle!'
  html_file.close()

def sortHumanly(list_item):
    """
    Sort the given list in the way that humans expect.
    Otherwise img10 comes before img2.
    """
    regexp = ''
    # Parentheses are used to capture/include the digit
    # in the pattern. Otherwise digit is excluded.
    # '([0-9]+)' can also be used as a pattern.
    regexp = r'(\d+)'
    result = ''
    result = re.split(regexp, list_item)

    # Since each list_item is like img<#> after re.split
    # it returns a list like ['img', '<#>', ''] so result[1]
    # corresponds to # for comparing. The last element ('') in
    # the result list means that there is a match in the string
    # for given pattern group/parentheses.
    if result[1].isdigit():
        return int(result[1])
    else:
        return result

def sortCustomly(list_item):
  """
  Sort the given list which contains urls like
  http://example.com/foo/puzzle/bar-abab-baaa.jpg
  by the second word which is baaa.
  That's why regular expression for filtering out the second word is:
  \/\w+-\w+-(\w+).jpg
  """
  regexp = ''
  regexp = r'\/\w+-\w+-(\w+).jpg'
  result = ''
  result = re.search(regexp, list_item)
  return result.group(1)

def main():
  # sys.argv[0] is script name itself so
  # it is excluded from arguments.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  # todir represents destination directory.
  todir = ''
  args_count = len(args)
  if args[0] == '--todir':
    # Needed to add a check here not to get
    # IndexError: list index out of range if
    # no todir and/or log file(animal | place) are
    # specified after --todir option as followings:
    # 1)./logpuzzle.py --todir -> Missing todir and log file
    # 2)./logpuzzle.py --todir animal_code.google.com -> Missing todir
    # Since we need at most 3 arguments to be able to use --todir option
    # which are 1)--todir, 2)todir and 3)log file args_count is used.
    # For this project I have only two log files which are
    # 1)animal_code.google.com and 2)place_code.google.com
    # so to check the correct input for them I include args[2] which
    # corresponds to log file name.
    if args_count == 3 and (args[2] == 'animal_code.google.com' or
                            args[2] == 'place_code.google.com'):
      todir = args[1]
      del args[0:2]
      # args[0] contains log file.
      img_urls = read_urls(args[0])
      download_images(img_urls, todir)
    else:
      print 'Error! Options are not valid or in the correct order. \n usage: [--todir dir] logfile'
      sys.exit(1)
  # To prevent such case ./logpuzzle.py a animal_code.google.com which means
  # if --todir option is not specified there is only one option lefts which
  # listing the urls in the correct log file name.
  elif args_count == 1 and (args[0] == 'animal_code.google.com' or args[0] == 'place_code.google.com'):
    # args[0] contains log file.
    img_urls = read_urls(args[0])
    for img_url in img_urls:
      print img_url
  else:
    print 'Error! Options are not valid or in the correct order. \n usage: [--todir dir] logfile'
    sys.exit(1)

if __name__ == '__main__':
  main()
