import os
#from struct import pack, unpack
import struct
pack, unpack = struct.pack, struct.unpack
#import argparse
import sys
#cwd = os.path.dirname(__file__)


def get_str(inbytes, index=0):
    byte = inbytes[index]
    data = b""
    while byte != 0:
        index += 1
        data += bytes([byte])
        byte = inbytes[index]

    return data.decode("utf-8")


fmt = "=I"


def writeimg(filedir="testfiles", imgfile="pyfs.img"):
    cwd = os.getcwd()
    files = []
    os.chdir(filedir)
    for x in os.listdir('.'):
        try:
            with open(x, "rb") as f:
                read: bytes = f.read()
                files.append([bytes([ord(y) for y in x]) + b"\0",
                 pack(fmt, len(read)), read])
        except Exception as e:
            #print('PermissionError:',e)
            pass
    #print(files)

    binfiles = []
    for x in files:
        binfiles.append(b"".join(x))

    #print(binfiles)
    data = b"".join(binfiles)
    #print(data)
    os.chdir(cwd)
    with open(imgfile, "wb") as f:
        f.write(data)


def readimg(filedir="testread", imgfile="pyfs.img"):
    cwd = os.getcwd()
    files = []
    with open(imgfile, "rb") as f:
        read: bytes = f.read()
    #print(read)
    index: int = 0
    while True:
        try:
            filename: str = get_str(read[index:])
            # assert filename != ''
            index += len(filename) + 1
            length: int = unpack(fmt, read[index : index + 4])[0]
            index += 4
            data: bytes = read[index : index + length]
            index += length
            files.append([filename, length, data])
            # raise Exception()

        except Exception as e:
            # print(e)
            break
    #print(files)
    os.chdir(filedir)
    for x in files:
        with open(x[0], "wb") as f:
            f.write(x[2])
    os.chdir(cwd)

#parser = argparse.ArgumentParser(description="Read from and write to a pyfs image file")
#subparsers = parser.add_subparsers()
#read = subparsers.add_parser('read', help='read from an image file')
#read.add_argument('img',default='pyfs.img',help="image file to read from")
#read.add_argument('dir',default='testread',help="directory to write to")
#read.set_defaults(func=readimg)

#write = subparsers.add_parser('write', help='write to an image file')
#write.add_argument('img',default='pyfs.img',help="image file to write to")
#write.add_argument('dir',default='testfiles',help="directory to read from")
#write.set_defaults(func=writeimg)

#args = parser.parse_args()

#print(not not args.read,not not args.write)
#args.func(args.dir,args.img)
args=sys.argv[1:]
helpmsg = '''usage: pyfs.py [-h] {read,write} img dir

Read from and write to a pyfs image file

positional arguments:
  {read,write}
    read        read from an image file
    write       write to an image file
    img         image file to read/write from
    dir         directory to write/read to
options:
  -h, --help    show this help message and exit'''
if len(args) > 2:
    if args[0].lower() == 'read':
        print('read')
        readimg(args[2],args[1])
    elif args[0].lower() == 'write':
        writeimg(args[2],args[1])
    else:
        print(helpmsg)
else:
    print(helpmsg)
#print(args,len(args) > 2)
