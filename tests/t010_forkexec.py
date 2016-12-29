#!/usr/bin/env python

import re, os
import subprocess as sp
from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'forkexec', """
# DURATION    TID     FUNCTION
            [ 9874] | main() {
  19.427 us [ 9874] |   readlink();
   1.841 us [ 9874] |   strrchr();
   0.911 us [ 9874] |   strcpy();
 142.145 us [ 9874] |   fork();
            [ 9874] |   waitpid() {
 473.298 us [ 9875] |   } /* fork */
            [ 9875] |   execl() {
            [ 9875] | main() {
   1.828 us [ 9875] |   atoi();
            [ 9875] |   a() {
            [ 9875] |     b() {
            [ 9875] |       c() {
   0.976 us [ 9875] |         getpid();
   1.992 us [ 9875] |       } /* c */
   2.828 us [ 9875] |     } /* b */
   3.658 us [ 9875] |   } /* a */
   7.713 us [ 9875] | } /* main */
   2.515 ms [ 9874] |   } /* waitpid */
   2.708 ms [ 9874] | } /* main */

""")

    def build(self, name, cflags='', ldflags=''):
        ret  = TestBase.build(self, 'abc', cflags, ldflags)
        ret += TestBase.build(self, self.name, cflags, ldflags)
        return ret

    def runcmd(self):
        return '%s -F main %s' % (TestBase.ftrace, 't-' + self.name)

    def fixup(self, cflags, result):
        r = result

        import platform
        if platform.machine().startswith('arm'):
            r = r.replace('readlink', """memset();
                                [ 9874] |   readlink""")

        return r
