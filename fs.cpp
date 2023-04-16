#include "builtin.hpp"
#include "os/path.hpp"
#include "os/__init__.hpp"
#include "stat.hpp"
#include "sys.hpp"
#include "struct.hpp"
#include "fs.hpp"

namespace __fs__ {

str *const_0, *const_1, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;




list<str *> *args;
str *__name__, *fmt, *helpmsg;
void *f;

str * default_0;
str * default_1;
str * default_2;
str * default_3;


static inline list<__ss_int> *list_comp_0(pyseq<pyseq<pyobj *> *> *x);

static inline list<__ss_int> *list_comp_0(pyseq<pyseq<pyobj *> *> *x) {
    pyseq<pyobj *> *y;
    pyseq<pyseq<pyobj *> *> *__9;
    __iter<pyseq<pyobj *> *> *__10;
    __ss_int __11;
    pyseq<pyseq<__ss_int> *>::for_in_loop __12;

    list<__ss_int> *__ss_result = new list<__ss_int>();

    FOR_IN(y,x,9,11,12)
        __ss_result->append(ord(y));
    END_FOR

    return __ss_result;
}

void *writeimg(str *filedir, str *imgfile) {
    str *cwd;
    list<list<bytes *> *> *__13, *files;
    pyseq<pyseq<pyobj *> *> *x;
    void *__7, *__8, *read;
    list<bytes *> *binfiles;
    bytes *data;
    list<str *> *__3;
    __iter<str *> *__4;
    __ss_int __15, __5;
    list<str *>::for_in_loop __6;
    file_binary *f;
    __iter<list<bytes *> *> *__14;
    list<list<bytes *> *>::for_in_loop __16;

    cwd = __os__::getcwd();
    files = (new list<list<bytes *> *>());
    __os__::chdir(filedir);

    FOR_IN(x,__os__::listdir(const_0),3,5,6)
        try {
            WITH_VAR(open_binary(x, const_1),f,0)
                files->append((new list<bytes *>(3,(__bytes(list_comp_0(x)))->__add__(new bytes("\000", 1)),pack(1, __fs__::fmt, len(read)),read)));
            END_WITH
        } catch (Exception *e) {
        }
    END_FOR

    binfiles = (new list<bytes *>());

    FOR_IN(x,files,13,15,16)
        binfiles->append((new bytes(""))->join(x));
    END_FOR

    data = (new bytes(""))->join(binfiles);
    __os__::chdir(cwd);
    WITH_VAR(open_binary(imgfile, const_2),f,1)
        f->write(data);
    END_WITH
    return NULL;
}

void *readimg(str *filedir, str *imgfile) {
    str *cwd;
    list<list<void *> *> *__17, *files;
    void *data, *filename, *index, *length, *read;
    list<void *> *x;
    file_binary *f;
    __iter<list<void *> *> *__18;
    __ss_int __19;
    list<list<void *> *>::for_in_loop __20;

    cwd = __os__::getcwd();
    files = (new list<list<void *> *>());
    WITH_VAR(open_binary(imgfile, const_1),f,2)
    END_WITH

    while (True) {
        try {
            index = (index)->__iadd__((len(filename))->__add__(__ss_int(1)));
            index = (index)->__iadd__(__ss_int(4));
            index = (index)->__iadd__(length);
            files->append((new list<void *>(3,filename,length,data)));
        } catch (Exception *e) {
            break;
        }
    }
    __os__::chdir(filedir);

    FOR_IN(x,files,17,19,20)
        WITH_VAR(open_binary(x->__getfast__(__ss_int(0)), const_2),f,3)
            f->write(x->__getfast__(__ss_int(2)));
        END_WITH
    END_FOR

    __os__::chdir(cwd);
    return NULL;
}

void __init() {
    const_0 = __char_cache[46];
    const_1 = new str("rb");
    const_2 = new str("wb");
    const_3 = new str("=I");
    const_4 = new str("testfiles");
    const_5 = new str("pyfs.img");
    const_6 = new str("testread");
    const_7 = new str("usage: pyfs.py [-h] {read,write} img dir\n\nRead from and write to a pyfs image file\n\npositional arguments:\n  {read,write}\n    read        read from an image file\n    write       write to an image file\n    img         image file to read/write from\n    dir         directory to write/read to\noptions:\n  -h, --help    show this help message and exit");
    const_8 = new str("read");
    const_9 = new str("write");

    __name__ = new str("__main__");

    fmt = const_3;
    default_0 = const_4;
    default_1 = const_5;
    default_2 = const_6;
    default_3 = const_5;
    args = (__sys__::argv)->__slice__(__ss_int(1), __ss_int(1), __ss_int(0), __ss_int(0));
    helpmsg = const_7;
    if ((len(__fs__::args)>__ss_int(2))) {
        if (__eq((__fs__::args->__getfast__(__ss_int(0)))->lower(), const_8)) {
            print(1, NULL, NULL, NULL, const_8);
            readimg(__fs__::args->__getfast__(__ss_int(2)), __fs__::args->__getfast__(__ss_int(1)));
        }
        else {
            if (__eq((__fs__::args->__getfast__(__ss_int(0)))->lower(), const_9)) {
                writeimg(__fs__::args->__getfast__(__ss_int(2)), __fs__::args->__getfast__(__ss_int(1)));
            }
            else {
                print(1, NULL, NULL, NULL, __fs__::helpmsg);
            }
        }
    }
    else {
        print(1, NULL, NULL, NULL, __fs__::helpmsg);
    }
}

} // module namespace

int main(int __ss_argc, char **__ss_argv) {
    __shedskin__::__init();
    __stat__::__init();
    __os__::__path__::__init();
    __os__::__init();
    __struct__::__init();
    __sys__::__init(__ss_argc, __ss_argv);
    __shedskin__::__start(__fs__::__init);
}
