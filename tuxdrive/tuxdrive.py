#!/usr/bin/env python3
##
# Tuxdrive A linux console implementation of Google Drive API
#
import os, httplib2, site
from apiclient import discovery
from apiclient.http import MediaIoBaseDownload, MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from tuxdrive import __version__, __license__, __author__

APPLICATION_NAME = "Tux Drive"
APP_PATH = os.getcwd()
REF_PATH = os.getcwd() #useful in downloading directories
BANNER = """Tux Drive version """ + __version__ + """
Copyright (c) 2017 Prahlad Yeri. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""

store = None 
creds = None 
remote_dir = "/"
remote_dir_id = "root"
remote_dir_cache = {}
remote_file_cache = {}
remote_contents = []

def fetch(query, sort='modifiedTime desc'):
    http = creds.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    results = service.files().list(
        q=query,orderBy=sort,pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


def get_credentials():
    global store
    #credential_path = site.getuserbase() + os.sep + 'credentials.json'
    credential_path = os.getcwd() + os.sep + 'credentials.json'
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("Credentials not found. Calling oauth2callback().")
        return oauth2callback()
    else:
        print("Credentials fetched successfully.")
        return credentials

def oauth2callback():
    helpstr = """Credentials file (client_id.json) not found on path:

%s

(For information on how to register a new google app, enable drive api and obtain client credentials, refer to this article:
https://prahladyeri.com/blog/2016/12/how-to-create-google-drive-app-python-flask.html    
"""
    global store
    fname = 'client_id.json'
    #if not os.path.isfile(fname): fname = "/etc/tuxdrive/client_id.json"
    if not os.path.isfile(fname): 
        print(helpstr % os.getcwd())
        return False
    flow = client.flow_from_clientsecrets( fname,
            scope='https://www.googleapis.com/auth/drive') #,
    flow.user_agent = APPLICATION_NAME #"Tux Client"
    credentials = tools.run_flow(flow, store)
    return credentials
    
def list_contents(silent = False):
    global creds, remote_contents, remote_dir_cache
    creds = get_credentials()
    if not creds: return
    
    remote_contents = []
    pstr = remote_dir_id
    #print(pstr)
    if not silent: print("")
    items = fetch("'" + pstr + "' in parents and mimeType = 'application/vnd.google-apps.folder'", sort='modifiedTime desc')
    for item in items:
        remote_contents.append({'name':item['name'], 'type':'DIRECTORY', 'id':item['id']})
        tdirname = remote_dir + ("" if remote_dir=="/" else "/") + item['name']
        remote_dir_cache[tdirname] = item['id']
        #print("Added dir to cache: %s" % tdirname)
        if not silent: print("%s %s" % ("DIRECTORY", item['name'] ))
    if not silent: print("%s %s" % ("DIRECTORY", ".." ))
    foldercnt = len(items)
    if not silent: print("")
    items = fetch("'" + pstr + "' in parents and mimeType != 'application/vnd.google-apps.folder'", sort='modifiedTime desc')
    for item in items:
        remote_contents.append({'name':item['name'], 'type':'FILE', 'id':item['id']})
        remote_file_cache[remote_dir + ("" if remote_dir=="/" else "/") + item['name']] = item['id']
        if not silent: print("%s %s" % ("FILE", item['name'] ))
    filecnt = len(items)
    
    #print("\n%d folders and %d files found." % (foldercnt, filecnt))
    if not silent: 
        print("\n%d items found.\n" % (foldercnt + filecnt))
        print("Remote Working Directory is %s(%s)" % (remote_dir, remote_dir_id) )
        
def share(file_id, email=None):
    creds = get_credentials()
    http = creds.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    ll = list_permissions(file_id, True) #check existing permissions
    #for item in ll: print(item)
    if len(ll) > 0: 
        #print(ll)
        print("Permissions already exist for this file. Run clear permissions to clear them first.")
        return

    body = {
        'role':'writer', #reader/writer/owner/organizer
        'type':'anyone' if email==None else "user", #user/group/domain/anyone
        'value': email, #email address if applicable, None otherwise
        'emailAddress': email,
    }
    permissions = service.permissions().create(fileId = file_id, body=body).execute()
    print("Shared successfully.")
    the_file = service.files().get(fileId=file_id, fields= 'webContentLink').execute()
    #print("URL is %s" % the_file['alternateLink']) #webContentLink
    print(the_file)

def clear_permissions(file_id): 
    creds = get_credentials()
    http = creds.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    ll = list_permissions(file_id, True) #check existing permissions
    #[{'id': '02374398500541929744', 'kind': 'drive#permission', 'role': 'owner', 'type': 'user'}]
    if len(ll) > 0:
        for item in ll:
            service.permissions().delete(fileId=file_id, permissionId=item['id']).execute()
        print("Cleared all permissions on %s." % file_id)
    else:
        print("No permissions to clear.")

# Returns all permissions except the owner permission       
def list_permissions(file_id, silent=False):
    #global creds, remote_contents, remote_dir_cache
    creds = get_credentials()
    http = creds.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    #service.files().delete(fileId=file_id).execute()
    permissions = service.permissions().list(fileId = file_id).execute()
    #ll = permissions.get('items', [])
    ll = permissions.get('permissions', [])
    for item in ll[:]:
        if item['role'] == 'owner': ll.remove(item)
    #ll = [item['role'] != 'owner': item ]
    
    if not silent:
        if len(ll) == 0:
            print("No permissions exist.")
        else:
            for item in ll: print(item)
        #print(permissions)
    else:
        return ll

def delete_file(file_id):
    """Permanently delete a file, skipping the trash."""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    service.files().delete(fileId=file_id).execute()
    print("Item %s deleted." % file_id)


# /docs     
def download_directory(path):
    global remote_dir, remote_dir_id

    #create local folder if doesn't exist
    #~ dirname = path.split("/")[-1]
    #~ if dirname == "" or dirname == "/":
        #~ dirname = "root"
    #~ fullpath = os.getcwd() + os.sep + dirname
    print("joining: ", REF_PATH, path[1:])
    fullpath = os.path.join(REF_PATH, path[1:])
    print("fullpath: ", fullpath)
    
    if not os.path.isdir(fullpath): os.mkdir(fullpath)
    
    #change local directory to that folder
    #os.chdir(fullpath)
    
    #change remote directory
    remote_dir = path
    #print("Changing remote directory to %s" % remote_dir)
    remote_dir_id =  remote_dir_cache[remote_dir]
    #print("Listing contents.")
    list_contents(True)
    #print("Changed.")

    #start downloading files
    for item in remote_contents:
        if item['type'] == 'FILE':
            download_file(item['id'], fullpath + os.sep + item['name'])
    
    #start downloading directories recursively
    tremote_dir = remote_dir #save it as the recursive function mutates the remote_dir
    for item in remote_contents[:]:
        if item['type'] == 'DIRECTORY':
            remote_dir = tremote_dir
            #remote_dir_id = ("" if remote_dir=="/" else remote_dir_cache[remote_dir])
            #print("Processing directory: %s" % remote_dir + "/" + item['name'])
            download_directory(remote_dir + "/" + item['name'])
    
    #childs = [key for key in remote_dir_cache.keys()]
    #dname = remote_dir_cache[path]
    
def upload_directory(input_path):
    global remote_dir, remote_dir_id
    #if remote_parent_path == "": remote_parent_path = remote_dir
    dirname  = input_path.split(os.sep)[-1]
    print("current_directory, input_path, dirname is %s, %s, %s" % (os.getcwd(), input_path, dirname))
    #make sure the remote path folder exists.
    rpath = remote_dir + ("" if remote_dir=="/" else "/") + dirname
    print("rpath is %s" % rpath)
    if rpath not in remote_dir_cache.keys():
        print("Creating remote directory: %s" % rpath)
        upload_file(dirname, True) #create directory remotely
        list_contents(True)
    else:
        print("Remote directory exists: %s" % rpath)
        
    remote_dir = rpath
    remote_dir_id = remote_dir_cache[rpath]
    list_contents(True)
    
    #upload all files on input_path one by one to the remote path.
    print("items:")
    print(os.listdir(input_path))
    for item in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path,item)):
            print("Uploading local file: %s" % item)
            upload_file(os.path.join(input_path, item))
    print("Uploaded all files on %s" % rpath)
    
    
    #scan each folder on input_path and recursively run upload_directory to each.
    trdir, trid = remote_dir, remote_dir_id #save as the recursion mutates these
    for item in os.listdir(input_path):
        if os.path.isdir(os.path.join(input_path,item)):
            remote_dir, remote_dir_id = trdir, trid
            upload_directory(os.path.join(input_path, item))
    print("Uploaded all folders on %s" % rpath)
    
    
#uploads/creates this file/folder to the remote_dir
def upload_file(input_file, is_folder=False):
    global remote_dir
    print("Uploading %s" % input_file)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    fname, found = input_file.split(os.sep)[-1], False
    typestr = 'FILE' if not is_folder else 'DIRECTORY'
    for item in remote_contents:
        if item['type'] == typestr and item['name'] == fname:
            found = True
            break
    if found: #update existing
        if not is_folder:
            print("File already exists, hence updating")
            #the_file = service.files().get(fileId=item['id']).execute()
            media_body = MediaFileUpload(input_file, resumable=True)
            updated_file = service.files().update(
                fileId=item['id'],
                #body=file,
                #newRevision=True,
                media_body=media_body).execute()
        else:
            print("Folder already exists.")
    else: #new upload
        #the_file = service.files().get(fileId=item['id']).execute()
        #print("Fname: " + fname)
        body = {'name': fname, "parents": [remote_dir_id ]} # 'mimeType': 'application/vnd.google-apps.document'
        if is_folder:
            body.update({'mimeType': "application/vnd.google-apps.folder"})
            #todo: what does fields='id' do?
            service.files().create(body=body, fields='id').execute() #newRevision=True,
        else:
            if os.stat(input_file).st_size == 0:
                print("Zero size file found: %s, skipping." % input_file)
                return
            media_body = MediaFileUpload(input_file, resumable=True)
            service.files().create(body=body, media_body=media_body).execute() #newRevision=True,
    print("Upload successful")
        
def download_file(file_id, output_file):
    global creds, remote_contents
    creds = get_credentials()
    if not creds: return
    
    print("Downloading: %s(%s)" % (file_id, output_file.split(os.sep)[-1]))
    http = creds.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    #file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
    #request = service.files().export_media(fileId=file_id,mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    request = service.files().get_media(fileId=file_id)
    
    fh = open(output_file,'wb') #io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        try:
            status, done = downloader.next_chunk()
        except Exception as ee:
            if ("Only files with binary content can be downloaded." in str(ee)):
                print("File not in binary content. Trying the export method.")
                request = service.files().export_media(fileId=file_id,mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                fh = open(output_file,'wb') #io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                continue
            else:
                print("Unknown error occurred: %s" % str(ee))
                return False
            
        #print ("Download %d%%." % int(status.progress() * 100))
    fh.close()
    print("Downloaded successfully to %s" % output_file)
    return output_file

    
        
def main():
    global remote_dir_id
    #~ print("%s version %s" % (APPLICATION_NAME, __version__))
    #~ print("Copyright (c) %s 2017.\n" % __author__)
    #print("License: %s.\n" % __license__)
    print(BANNER)
    global remote_dir
    HELP_STRING = """Commands:

help (or ?): Shows this help facility.
dir (or ls): Lists all files and folders on drive.
!dir (or !ls): Lists all files and folders in current directory.
get (or pull) <item>: Pulls the named file/folder from drive to current working directory.
put (or push) <item>: Pushes the named file/folder from current working directory to drive.
rm <item>: Delete the named file/folder on remote path.
pwd: Print working directory (remote/drive).
cd: Change working directory (remote/drive).
lpwd: Print working directory (local).
lcd: Change working directory (local).
mkdir: Create a directory on remote path.
list permissions <item>: Lists the permissions on specific file/directory.
clear permissions <item>: Clears permissions on specific file/directory.
share <item>: Shares the specific file/directory in remote drive publicly.
share <item> <email>: Shares the specific file/directory in remote drive to specified email.
exit: Exits this program.
rdcache: Show remote directory mapping of id and folder paths.
rfcache: Show remote files mapping of id and folder paths.

Examples:

get alice.txt (Pulls the file alice.txt to local directory).
share bob.txt (Shares the file bob.txt publicly).
share joe.txt alice@gmail.com (Shares the file joe.txt with Alice).
list permissions alice.txt (Lists the current permissions available on alice.txt)

"""
    #repl
    PROMPT = "tux_drive> "
    list_contents(True)
    while(True):
        try:
            cli = str(input(PROMPT))
        except KeyboardInterrupt:
            print("Bye.")
            break
        if cli == "help":
            print(HELP_STRING)
        elif cli == "exit":
            print("Bye.")
            break
        elif cli == "ls" or cli == "dir" or cli == "ls remote":
            list_contents()
        elif cli == "!ls" or cli == "!dir" or cli == "ls local":
            cnt = 0
            for item in os.listdir():
                print(("FILE " if os.path.isfile(item) else "DIRECTORY ") + item)
                cnt += 1
            print("\n%d items found.\n" % cnt)
            print("\nLocal Working Directory is %s" % os.getcwd())
        elif cli.startswith("rcd ") or cli.startswith("cd "):
            #ss = cli[4:]
            ss = cli[cli.index(' ')+1:]
            #if len(remote_contents) == 0: list_contents(True)
            found = True
            
            if ss == "/":
                remote_dir = "/"
                remote_dir_id = "root"
                list_contents(True)
            elif ss == "..":
                remote_dir = "/".join(remote_dir.split("/")[0:-1])
                #remote_dir_id = last_remote_dir_id
                if remote_dir == "": 
                    remote_dir = "/"
                    remote_dir_id = "root"
                else:
                    remote_dir_id = remote_dir_cache[remote_dir]
                list_contents(True)
            else:
                if remote_dir + ("" if remote_dir=="/" else "/") + ss in remote_dir_cache.keys():
                    remote_dir += ("" if remote_dir=="/" else "/") + ss
                    remote_dir_id = remote_dir_cache[remote_dir]
                    list_contents(True)
                else:
                    found = False
                #found = False
                #~ for item in remote_contents:
                    #~ if item['name'] == ss:
                        #~ found = True
                        #~ remote_dir += ("" if remote_dir=="/" else "/") + ss
                        #~ #last_remote_dir_id = remote_dir_id
                        #~ remote_dir_id = item['id']
                        #~ list_contents(True)
            if not found:
                print("Directory not found on remote drive.")
            else:
                print("Remote directory changed to " + remote_dir + " (%s)" % remote_dir_id)
        elif cli.startswith("lcd "): #change local directory
            ss = cli[4:]
            if os.path.isdir(ss):
                os.chdir(ss)
                print("Directory changed to %s\n" % ss)
            else:
                print("Directory does not exist.\n")
        elif cli == "lpwd" or cli == "lwd":
            print("Local Working Directory is %s" % os.getcwd()) #os.chdir(..), 
        elif cli == "pwd" or cli == "rwd":
            print("Remote Working Directory is %s(%s)" % (remote_dir, remote_dir_id))
        elif cli == "rdcache":
            for key in remote_dir_cache:
                print(key, remote_dir_cache[key])
            print("")
        elif cli == "rfcache":
            for key in remote_file_cache:
                print(key, remote_file_cache[key])
            print("")
        elif cli.startswith("pull ") or cli.startswith("get "):
            #ss = cli[5:]
            ss = cli[cli.index(' ')+1:]
            fname = remote_dir + ("" if remote_dir=="/" else "/") + ss
            if fname in remote_file_cache.keys():
                print("File found: %s" % fname)
                rr = download_file(remote_file_cache[fname], os.getcwd() + os.sep + ss)
            elif fname in remote_dir_cache.keys():
                print("Directory found: %s" % fname)
                #save current settings
                trd, trd_id = remote_dir, remote_dir_id
                #tld = os.getcwd()
                REF_PATH = os.getcwd()
                #download directory
                download_directory(fname)
                #revert old settings
                remote_dir, remote_dir_id = trd, trd_id
                #os.chdir(tld)
                list_contents(True)
            else:
                print("Item not found on remote drive.")
        elif cli.startswith("push ") or cli.startswith("put "):
            #ss = cli[5:]
            ss = cli[cli.index(' ')+1:]
            if os.path.isfile(ss):
                upload_file(ss)
            elif os.path.isdir(ss): #upload directory
                trd, trd_id = remote_dir, remote_dir_id
                upload_directory(ss)
                remote_dir, remote_dir_id = trd, trd_id
                list_contents(True)
            else:
                print("Item not found on local drive.")
            list_contents(True) #repoll
        elif cli.startswith("mkdir"):
            ss = cli[6:]
            upload_file(ss, True)
            list_contents(True) #repoll
        elif cli.startswith("list permissions"):
            ss = " ".join(cli.split(" ")[2:])
            fname = remote_dir + ("" if remote_dir=="/" else "/") + ss
            #print(ss, len(ss))
            ##print(remote_file_cache.keys())
            if fname in remote_dir_cache.keys():
                theid = remote_dir_cache[fname]
            elif fname in remote_file_cache.keys():
                theid = remote_file_cache[fname]
            else:
                print("Item not found on remote drive.")
                continue
            list_permissions(theid)
        elif cli.startswith("clear permissions"):
            ss = " ".join(cli.split(" ")[2:])
            fname = remote_dir + ("" if remote_dir=="/" else "/") + ss
            if fname in remote_dir_cache.keys():
                theid = remote_dir_cache[fname]
            elif fname in remote_file_cache.keys():
                theid = remote_file_cache[fname]
            else:
                print("Item not found on remote drive.")
                continue
            clear_permissions(theid)
        elif cli.startswith("share "):
            #ss = " ".join(cli.split(" ")[1:])
            ss = cli.split(" ")[1:]
            fname = remote_dir + ("" if remote_dir=="/" else "/") + ss[0]
            if fname in remote_dir_cache.keys():
                theid = remote_dir_cache[fname]
            elif fname in remote_file_cache.keys():
                theid = remote_file_cache[fname]
            else:
                print("Item not found on remote drive.")
                continue
            if len(ss) == 1: #globally
                share(theid)
            elif len(ss) > 1: #with specific email
                share(theid, ss[1])
            else:
                print("Incorrect arguments.")
                continue
        elif cli.startswith("rm"):
            ss, found = cli[3:], False
            for item in remote_contents:
                if item['name'] == ss and item['type'] == 'DIRECTORY':
                    found = True
                    rr = input("%s is a directory. Are you sure you want to delete it? (Y/n)" % item['name']).lower()
                    if rr == "y":
                        delete_file(item['id'])
                elif item['name'] == ss and item['type'] == 'FILE':
                    found = True
                    delete_file(item['id'])
            if not found: print("Item not found on remote drive.")
        else:
            print("Unrecognized verb.")

if __name__ == "__main__":
    main()
