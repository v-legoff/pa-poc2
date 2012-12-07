# Copyright (c) 2012 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""This script tries to get and install the required dependencies.

You should run it as root.

"""

from setuptools.command import easy_install

def install_with_easyinstall(package):
    """Install the specified packages (in dry-run)."""
    easy_install.main(["-U", package])

install_with_easyinstall("http://pyyaml.org/download/pyyaml/" \
        "PyYAML-3.10.tar.gz")
install_with_easyinstall("https://bitbucket.org/cherrypy/cherrypy/downloads/" \
        "CherryPy-3.2.3dev-20121017.tar.gz")
install_with_easyinstall("http://pypi.python.org/packages/source/" \
        "J/Jinja2/Jinja2-2.6.tar.gz")

confirm = input(
    "Do you want to install the Pymongo module for MongoDB [y/n] ? [n] ")
if confirm.lower() == "y":
    install_with_easyinstall("http://pypi.python.org/packages/source/p/" \
            "pymongo/pymongo-2.4.1.tar.gz#md5=be358dece09bc57561573db35bc75eb0")

confirm = input(
    "Do you want to install the py-postgresql module for PostgreSQL [y/n] ? " \
    "[n]")
if confirm.lower() == "y":
    install_with_easyinstall("http://pypi.python.org/packages/source/p/" \
            "py-postgresql/py-postgresql-1.1.0.zip")
