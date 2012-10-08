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


"""Package containing the formatters for Python Aboard.

A formatter is a class which role is to take some informations and convert them in another format.  The input informations are given as objects and the output should be a string.  Python Aboard proposes a formatter for XML, YML and so forth.

Note that the templating system is hidden behind the formatters.  For instance:
*  A GET request is sent to the server on /images/1.xml
*  The controller calls its method 'render' with the user which id = 1
*  The 'render' method look for the requested format.  Here, the XML is required
*  The XMLFormatter takes the user and return a XML representation of
   this user.

If the requested format is some kind of template, then the formatter
redirects the user representation to the template itself.

To add a new formatter, simply create a class (in your bundle, for
instance) inheriting from Formatter.  This class has to be imported,
of course, but no other code is needed to add this class to the
possible formatters and your bundle (or even others) will be able
to use it.

"""

from ext.aboard.formatters.meta import formatters, formats

import ext.aboard.formatters.yaml
