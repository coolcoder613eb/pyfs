import os
from struct import pack, unpack
import argparse


def get_bit(value, bit_index):
    return (value >> bit_index) & 1


def set_bit(value, bit_index):
    return value | (1 << bit_index)


def clear_bit(value, bit_index):
    return value & ~(1 << bit_index)


def toggle_bit(value, bit_index):
    return value ^ (1 << bit_index)


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
    for x in os.listdir():
        try:
            with open(x, "rb") as f:
                read = f.read()
                files.append([bytes(x, "utf-8") + b"\0", pack(fmt, len(read)), read])
        except PermissionError as e:
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
        read = f.read()
    #print(read)
    index = 0
    while True:
        try:
            filename = get_str(read[index:])
            # assert filename != ''
            index += len(filename) + 1
            length = unpack(fmt, read[index : index + 4])[0]
            index += 4
            data = read[index : index + length]
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


parser = argparse.ArgumentParser(description="Read from and write to a pyfs image file")
subparsers = parser.add_subparsers()
read = subparsers.add_parser('read', help='read from an image file')
read.add_argument('img',default='pyfs.img',help="image file to read from")
read.add_argument('dir',default='testread',help="directory to write to")
read.set_defaults(func=readimg)

write = subparsers.add_parser('write', help='write to an image file')
write.add_argument('img',default='pyfs.img',help="image file to write to")
write.add_argument('dir',default='testfiles',help="directory to read from")
write.set_defaults(func=writeimg)

args = parser.parse_args()

#print(not not args.read,not not args.write)
args.func(args.dir,args.img)