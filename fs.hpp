#ifndef __FS_HPP
#define __FS_HPP

using namespace __shedskin__;
namespace __fs__ {

extern str *const_0, *const_1, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;


typedef bytes *(*lambda0)(void *, void *, void *, void *, void *);
typedef bytes *(*lambda1)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda2)(void *, void *, void *, void *, void *);
typedef str *(*lambda3)(void *, void *, void *, void *, void *);
typedef __ss_int (*lambda4)(void *, void *, void *, void *, void *);
typedef bytes *(*lambda5)(void *, void *, void *, void *, void *);

extern str *__name__, *fmt, *helpmsg;
extern list<str *> *args;
extern void *f;


extern str * default_0;
extern str * default_1;
extern str * default_2;
extern str * default_3;
void *writeimg(str *filedir, str *imgfile);
void *readimg(str *filedir, str *imgfile);

} // module namespace
#endif
