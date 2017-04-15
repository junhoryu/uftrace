#!/usr/bin/env python

from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'dlopen', """1
# DURATION    TID     FUNCTION
   1.404 us [22207] | __cxa_atexit();
            [22207] | main() {
  70.963 us [22207] |   dlopen();
   1.546 us [22207] |   dlsym();
            [22207] |   lib_a() {
            [22207] |     lib_b() {
   0.678 us [22207] |       lib_c();
   1.301 us [22207] |     } /* lib_b */
   2.104 us [22207] |   } /* lib_a */
  14.446 us [22207] |   dlclose();
            [22207] |   dlopen() {
            [22207] |     _GLOBAL__sub_I_s_libfoo.cpp() {
  88.318 us [22207] |       __static_initialization_and_destruction_0();
  88.719 us [22207] |     } /* _GLOBAL__sub_I_s_libfoo.cpp */
 148.243 us [22207] |   } /* dlopen */
   0.844 us [22207] |   dlsym();
            [22207] |   foo() {
  19.601 us [22207] |     print_int();
  19.869 us [22207] |   } /* foo */
  13.391 us [22207] |   dlclose();
 274.723 us [22207] | } /* main */
""")

    def build(self, name, cflags='', ldflags=''):
        if TestBase.build_libabc(self, cflags, ldflags) != 0:
            return TestBase.TEST_BUILD_FAIL
        if TestBase.build_libfoo(self, 'foo', cflags, ldflags) != 0:
            return TestBase.TEST_BUILD_FAIL
        return TestBase.build_libmain(self, name, 's-dlopen.c', ['libdl.so'],
                                      cflags, ldflags)