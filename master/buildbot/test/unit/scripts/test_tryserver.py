# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

import os
import sys
from io import StringIO

from twisted.trial import unittest

from buildbot.scripts import tryserver
from buildbot.test.util import dirs


class TestStatusLog(dirs.DirsMixin, unittest.TestCase):

    def setUp(self):
        self.newdir = os.path.join('jobdir', 'new')
        self.tmpdir = os.path.join('jobdir', 'tmp')
        self.setUpDirs("jobdir", self.newdir, self.tmpdir)

    def test_trycmd(self):
        config = {"jobdir": 'jobdir'}
        inputfile = StringIO('this is my try job')
        self.patch(sys, 'stdin', inputfile)

        rc = tryserver.tryserver(config)

        self.assertEqual(rc, 0)

        newfiles = os.listdir(self.newdir)
        tmpfiles = os.listdir(self.tmpdir)
        self.assertEqual((len(newfiles), len(tmpfiles)),
                         (1, 0))
        with open(os.path.join(self.newdir, newfiles[0]), 'rt', encoding='utf-8') as f:
            self.assertEqual(f.read(), 'this is my try job')
