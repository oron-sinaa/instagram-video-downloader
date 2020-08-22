"""
InstaJet video downloader for instagram
by https://github.com/oron-sinaa
* Can download post/IGTV videos with copied "post" link. Post should contain a single video. *
Currently works only with public accounts, will add login to download private videos functionality soon.
"""

import urllib.request, urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup
import requests
import os
import sys
import time
#import re
#from inputimeout import inputimeout, TimeoutOccurred

# eg: https://www.instagram.com/p/CCGvtSgodOk/
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# fake user agent - no use now
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
ti = 'i n s t a J e t    -    I N S T A G R A M   D O W N L O A D E R'
for i in range(len(ti)):
    print('-',end='')
print("\n{}".format(ti))
for i in range(len(ti)):
    print('-',end='')
print('\n')

def downloader():

    # send GET/POST request to the entered website
    try:
        url = input("\nENTER THE INSTAGRAM POST/IGTV URL: ")
        if (len(url)) == 0:
            print("url cannot be empty!")
            downloader()
        print()
        print("Trying to retrieve \"{}{}".format(url,'"'))
        uh = urllib.request.urlopen(url)
        if uh.getcode() == '200':
            print("Succesfully connected to web server...")
        elif uh.getcode() == '404':
            print("Error 404: Page Not Found, terminating...")
            exit()
        elif uh.getcode() == '403':
            print("Access Denied, terminating...")
            exit()
    except:
        print("Some error occurred in connecting to the url. Exiting...")
        exit()
        # decode data to unicode for human readability
    data = uh.read().decode()
    #"""print('Retrieved', len(data), 'characters from the source code...')"""

    # check if page is private
    if ('instagram.com/p/') in url:
        private_check = True
    else:
        private_check = False
    print(private_check)
    exit()




    # add login if private here




    # parsing html for video link
    #"""print("Parsing direct video link from the source code...")"""
    soup = BeautifulSoup(data, "html.parser")
    link = soup.find('meta', attrs={"property": "og:video"})
    link_str = str(link)
    pre_link = link_str[15:-23]
    final_link = pre_link.replace('amp;', '')
    print("\n+ VIDEO LINK: ", final_link)

    # giving file name
    bname = str(soup.find('title'))
    pos_end = bname.find(' on')
    xname = bname[8:pos_end]
    zname = xname.replace(' ','')
    fname = zname + "_instaJet.mp4"

    # if file with same name already exists, prompt for rename
    rep_n_count = 1
    while os.path.isfile(fname) == True:
        new_name = zname + '(' + str(rep_n_count) + ')'
        rep_n_count+=1
        fname = new_name + "_instaJet.mp4"
    if rep_n_count > 1:
        print("\nFile with same name was found. Renamed.")
    print('+ FILE NAME: ', fname)

    try:
        # sending request for file access
        print("\nStarting download process...")

        # file size and confirmation
        x = requests.head(final_link)
        s = int(x.headers['Content-Length'])
        size = s / 1000000
        print('\n+ FILE SIZE: ', size, 'MiB')
        """
        try:
            print("Waiting 5 seconds before auto-download (if size < 25 Mib).")
            ch = inputimeout(prompt='CONTINUE DOWNLOADING? (y/Y) : ', timeout=5)
        except TimeoutOccurred:
            if int(size) < 25 :
                ch='y'
        """
        if int(size) <= 50:
            ch = 'y'
        elif int(size) > 50:
            ch = input('START DOWNLOADING {}{}'.format(int(size),' MiB? (y/Y) : '))

        # actual downloading
        if (ch == 'y' or ch == 'Y'):
            print('\n----------------------------------------------------')
            print("NOW DOWNLOADING:",end=' ')
            time.sleep(0.75)
            print(fname)
            time.sleep(0.25)
            with open(fname, 'wb') as f:
                r = requests.get(final_link, stream=True)
                total = s
                downloaded = 0
                for d in r.iter_content(chunk_size=max(int(total/1000), 2 * 2)):
                    downloaded += len(d)
                    f.write(d)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                    sys.stdout.flush()
                if downloaded == s:
                    time.sleep(0.5)
                    print("\nDownload complete! Check default directory.")
                elif downloaded != s:
                    print("Some or whole download interrupted.")
            print('----------------------------------------------------')
        else:
            print("\nDownload cancelled.")
            print('-----------------------------------------------')

        time.sleep(0.75)
        # ask user to continue downloading another video
        choice = input("\nWish to download another video? (y/Y) : ")
        if (choice == 'y' or choice=='Y'):
            print('----------------------------------------------------------------------------------------------')
            print('----------------------------------------------------------------------------------------------')
            downloader()
        else:
            input("\nThank you for using the tool, press any key to terminate...")
    except:
        print("Some error occurred in grabbing the file. Make sure the page is public has single video/IGTV in the link, nothing else compatible now :(")


""" 
----------------------------------
Calling the function for execution
----------------------------------
"""

downloader()
s_close = requests.session(config={'keep_alive': False}