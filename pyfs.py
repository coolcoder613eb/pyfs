import os
from struct import pack, unpack
import argparse

SEEK_CUR = 1

Gooey = lambda x: x

#from gooey import Gooey


def get_bit(value, bit_index):
    return (value >> bit_index) & 1


def set_bit(value, bit_index):
    return value | (1 << bit_index)


def clear_bit(value, bit_index):
    return value & ~(1 << bit_index)


def toggle_bit(value, bit_index):
    return value ^ (1 << bit_index)


def get_str(file, index=0):
    byte = file.read(1)
    assert byte != b""
    # inbytes[index]
    data = b""
    while byte != b"\0":
        index += 1
        data += byte
        byte = file.read(1)

    return data.decode("utf-8")


def isfinished(file):
    try:
        print(file.tell())
        file.read(20)
        print(file.tell())
        file.seek(-1, SEEK_CUR)
        print(file.tell())
        return False
    except Exception as e:
        print(e)
        return True


fmt = "=I"


def writeimg(filedir="testfiles", imgfile="pyfs.img"):
    cwd = os.getcwd()
    files = []
    os.chdir(filedir)
    for x in os.listdir():
        try:
            with open(x, "rb") as f:
                print(f"Adding {x}...")
                read = f.read()
                files.append([bytes(x, "utf-8") + b"\0", pack(fmt, len(read)), read])
        except OSError as e:
            # print('PermissionError:',e)
            pass
    # print(files)

    binfiles = []
    for x in files:
        binfiles.append(b"".join(x))

    # print(binfiles)
    data = b"".join(binfiles)
    # print(data)
    os.chdir(cwd)
    with open(imgfile, "wb") as f:
        print(f"Writing to {imgfile}...")
        f.write(data)


def readimg(filedir="testread", imgfile="pyfs.img"):
    cwd = os.getcwd()
    files = []
    with open(imgfile, "rb") as f:
        print(f"Reading from {imgfile}...")
        # read = f.read()
        # print(read)
        index = 0
        while True:
            try:
                filename = get_str(f)  # read[index:])
                assert filename != ""
                print(f"Reading {filename}...")
                index += len(filename) + 1
                length = unpack(fmt, f.read(4))[0]  # read[index : index + 4])[0]
                index += 4
                data = f.read(length)  # read[index : index + length]
                index += length
                files.append([filename, length, data])
                # print('Done')
                # raise Exception()

            except Exception as e:
                # print(e)
                break
    # print(files)
    os.chdir(filedir)
    print(f"Writing files to {filedir}...")
    for x in files:
        with open(x[0], "wb") as f:
            # print(f'Writing {x[0]}...')
            f.write(x[2])
    os.chdir(cwd)


def lsimg(imgfile="pyfs.img"):
    # cwd = os.getcwd()
    files = []
    with open(imgfile, "rb") as f:
        # print(f'Reading from {imgfile}...')
        while True:
            try:
                filename = get_str(f)  # read[index:])
                assert filename != ""
                length = unpack(fmt, f.read(4))[0]  # read[index : index + 4])[0]
                f.seek(length, SEEK_CUR)
                files.append(filename)
                # print(files)
                # if files == ['file.txt', 'that.bin']:
                #     print(f.read(1))

            except Exception as e:
                # print(e)
                break
    print("\n".join(files))


def getimg(file="file.txt", imgfile="pyfs.img"):
    cwd = os.getcwd()
    files = []
    with open(imgfile, "rb") as f:
        print(f"Reading from {imgfile}...")
        while True:
            try:
                filename = get_str(f)
                assert filename != ""
                length = unpack(fmt, f.read(4))[0]
                if filename == file:
                    print(f"Reading {filename}...")
                    data = f.read(length)
                    files.append([filename, length, data])
                else:
                    f.seek(length, SEEK_CUR)

            except Exception as e:
                # print(e)
                break
    # print(files)
    if not files:
        print(f"Could not find {file}!")
    else:
        for x in files:
            with open(x[0], "wb") as f:
                print(f"Writing {x[0]}...")
                f.write(x[2])


def putimg(file="file.txt", imgfile="pyfs.img"):
    # cwd = os.getcwd()
    files = []
    # os.chdir(filedir)

    try:
        with open(file, "rb") as f:
            print(f"Adding {x}...")
            read = f.read()
            files.append([bytes(x, "utf-8") + b"\0", pack(fmt, len(read)), read])
    except Exception as e:
        # print(e)

        pass
    # print(files)

    with open(imgfile, "rb") as f:
        # print(f"Reading from {imgfile}...")
        while True:
            try:
                filename = get_str(f)
                assert filename != ""
                length = unpack(fmt, f.read(4))[0]
                f.seek(length, SEEK_CUR)

            except Exception as e:
                # print(e)
                if isfinished(f):
                    f1 = open(imgfile, "ab")
                    print('ab')
                else:
                    f1 = open(imgfile, "r+b")
                    f1.seek(f.tell())
                    print('r+b')

                binfiles = []
                for x in files:
                    binfiles.append(b"".join(x))
                data = b"".join(binfiles)
                print(f"Writing to {imgfile}...")
                f1.write(data)
                break


@Gooey
def main():
    parser = argparse.ArgumentParser(
        description="Read from and write to a pyfs image file"
    )
    subparsers = parser.add_subparsers(dest="name")
    read = subparsers.add_parser("read", help="read from an image file")
    read.add_argument("img", default="pyfs.img", help="image file to read from")
    read.add_argument("dir", default="testread", help="directory to write to")
    read.set_defaults(func=readimg)

    write = subparsers.add_parser("write", help="write to an image file")
    write.add_argument("img", default="pyfs.img", help="image file to write to")
    write.add_argument("dir", default="testwrite", help="directory to read from")
    write.set_defaults(func=writeimg)

    write = subparsers.add_parser("ls", help="list files on an image")
    write.add_argument("img", default="pyfs.img", help="image file to read from")
    write.set_defaults(func=lsimg)

    get = subparsers.add_parser("get", help="get a file from an image")
    get.add_argument("img", default="pyfs.img", help="image file to write to")
    get.add_argument("file", default="file.txt", help="file to get")
    get.set_defaults(func=getimg)

    put = subparsers.add_parser("put", help="store a file onto an image")
    put.add_argument("img", default="pyfs.img", help="image file to write to")
    put.add_argument("file", default="file.txt", help="file to store")
    put.set_defaults(func=putimg)

    args = parser.parse_args()
    # print(args)

    # print(not not args.read,not not args.write)
    if args.name == "read" or args.name == "write":
        args.func(args.dir, args.img)
    elif args.name == "ls":
        args.func(args.img)
    elif args.name == "get" or args.name == "put":
        args.func(args.file, args.img)
    else:
        parser.print_help()


main()
