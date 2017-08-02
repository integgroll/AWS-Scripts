import os
import re
import pip
import shutil
import zipfile
import argparse
import itertools
import virtualenv


# Here is the things for arguments I guess. 
parser = argparse.ArgumentParser(description="AWS Lambda Packager")

parser.add_argument("file", nargs = 1, help='Filename to package')
arguments = parser.parse_args()
file_name = arguments.file[0].split(".")[0]

import_list = []
import_patterns = [re.compile("^import (.*?)$"),re.compile("^from (.*?) import .*$")]
module = open(file_name+".py","r")
for line in module.readlines():
    for pattern in import_patterns:
        tested_pattern = pattern.search(line)
        if tested_pattern:
            import_list.append(tested_pattern.group(1).split('.')[0])

#Default libraries that are included in python as a whole (wow there are a lot of these... a hell of a lot) And also the libraries included on amazon lambda
default_library_array = list(itertools.chain.from_iterable([["string","re","struct","difflib","StringIO","cStringIO","textwrap","codecs","unicodedata","stringprep","fpformat"],
["datetime","calendar","collections","heapq","bisect","array","sets","sched","mutex","Queue","weakref","UserDict","UserList","UserString","types","new","copy","pprint","repr"],
["numbers","math","cmath","decimal","fractions","random","itertools","functools","operator"],
["os","fileinput","stat","statvfs","filecmp","tempfile","glob","fnmatch","linecache","shutil","dircache","macpath"],
["pickle","cPickle","copy_reg","shelve","marshal","anydmb","wichdb","dmb","gdmb","dbhash","bsddb","dumbdbm","sqlite3"],
["zlib","gzip","bz2","zipfile","tarfile"],
["csv","ConfigParser","robotparser","netrc","xdrlib","plistlib"],
["hashlib","hmac","md5","sha"],
["os","io","time","argparse","optparse","getopt","logging","getpass","curses","platform","errno","ctypes"],
["select","threading","thread","dummy_threading","dummy_thread","multiprocessing","mmap","readline","rlcompleter"],
["sumprocess","socket","ssl","signal","popen2","asyncore","asynchat"],
["email","json","mailcap","mailbox","mhlib","mimetools","mimetypes","MimeWriter","mimify","multifile","rfc882","base64","binhex","binascii","quopri","uu"],
["HTMLParser","sgmllib","htmllib","htmlentitydefs","xml"],
["webbrowser","cgi","cgtib","wsgiref","urllib","urllib2","httplib","ftplib","poplib","imaplib","nntplib","smtplib","smtpd","telnetlib","uuid","urlparse","SocketServer","BaseHTTPServer","SimpleHTTPServer","CGIHTTPServer","cookielib","Cookie","xmlrpclib","SimpleSMLRPCServer","DocXMLRPCServer"],
["audioop","imageop","aifc","sunau","wave","chunk","colorsys","imghdr","sndhdr","ossaudiodev"],
["gettext","locale"],
["cmd","shlex"],
["Tkinter","ttk","Tix","ScrolledText","turtle"],
["pydoc","doctest","unittest","test"],
["bdb","pdb","hotshot","timeit","trace"],
["distutils","ensurepip"],
["sys","sysconfig","__builtin__","future_builtins","__main__","warnings","contextlib","abc","atexit","traceback","__future__","gc","inspect","site","user","fpectl"],
["code","codeop"],
["rexec","Bastion"],
["imp","importlib","imputil","zipimport","pkgutil","modulefinder","runpy"],
["parser","ast","symtable","symbol","token","keyword","tokenize","tabnanny","pyclbr","py_compile","compileall","dis","pickletools"],
["formatter"],
["msilib","msvcrt","_winreg","winsound"],
["posix","pwd","spwd","grp","crypt","dl","termios","tty","pty","fcntl","pipes","posixfile","resource","nis","syslog","commands"],
["ic","MacOS","macostools","findertools","EasyDialogs","Framework","autoGIL","ColorPicker"],
["gensuitemodule","aetools","aepack","aetypes","MiniAEFrame"],
["al","AL","cd","fl","FL","flp","fm","gl","DEVICE","GL","imgfile","jpeg"],
["sunaudiodev","SUNAUDIODEV"],
["boto3"]]))

modules_to_localize = list(filter(lambda x: x not in default_library_array,import_list))


# Creates the actual virtual environment. this is going to be used for cool things in a bit, I think. 
virtual_directory = os.getcwd()+"\\"+file_name+"-lambda"
virtualenv.create_environment(virtual_directory)

#intstall each individual module that we are looking to deal with
for module in modules_to_localize:
    pip.main(["install","-t",virtual_directory+"\\Lib\\site-packages", module])

#Zipfile Section, shutil to cheat the folder addition to the zipfile and then proper python zip stuff for the individual file
shutil.make_archive(file_name+"-lambda","zip",root_dir=virtual_directory+"\\Lib\\site-packages")
with zipfile.ZipFile(file_name+"-lambda"+".zip","a") as myzip:
    myzip.write(file_name+".py")

# Delete all of the old stuff? I mean not the literal worst idea ever. 
shutil.rmtree(file_name+"-lambda")
