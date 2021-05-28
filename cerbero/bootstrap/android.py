# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import shutil

from cerbero.bootstrap import BootstrapperBase
from cerbero.bootstrap.bootstrapper import register_toolchain_bootstrapper
from cerbero.config import Distro, FatalError
from cerbero.utils import _, shell

NDK_VERSION = 'r22b'
NDK_BASE_URL = 'https://dl.google.com/android/repository/android-ndk-%s-%s-%s.zip'
NDK_CHECKSUMS = {
    'android-ndk-r22b-linux-x86_64.zip': 'ac3a0421e76f71dd330d0cd55f9d99b9ac864c4c034fc67e0d671d022d4e806b',
    'android-ndk-r22b-darwin-x86_64.zip': 'b05d2087a6346d66cd26a1dc89fcc877b59e49feab6269b665aa67c784a81512',
    'android-ndk-r22b-windows-x86_64.zip': '6d2fe8dbba8342634e88ecbaf321bcbfc07e579b6281f426639002dd35046d03',
}

class AndroidBootstrapper (BootstrapperBase):

    def __init__(self, config, offline, assume_yes):
        super().__init__(config, offline)
        self.prefix = self.config.toolchain_prefix
        url = NDK_BASE_URL % (NDK_VERSION, self.config.platform, self.config.arch)
        self.fetch_urls.append((url, NDK_CHECKSUMS[os.path.basename(url)]))
        self.extract_steps.append((url, True, self.prefix))

    def start(self, jobs=0):
        if not os.path.exists(self.prefix):
            os.makedirs(self.prefix)
        ndkdir = os.path.join(self.prefix, 'android-ndk-' + NDK_VERSION)
        if not os.path.isdir(ndkdir):
            return
        # Android NDK extracts to android-ndk-$NDK_VERSION, so move its
        # contents to self.prefix
        for d in os.listdir(ndkdir):
            dest = os.path.join(self.prefix, d)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.move(os.path.join(ndkdir, d), self.prefix)
        os.rmdir(ndkdir)


def register_all():
    register_toolchain_bootstrapper(Distro.ANDROID, AndroidBootstrapper)
