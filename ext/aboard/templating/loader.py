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


"""Module containing the Jinja2 loader."""

from os.path import join, exists, getmtime

from jinja2 import BaseLoader, TemplateNotFound

class PAFileSystemLoader(BaseLoader):
    
    """Template loader for Python Aboard.
    
    It's almost a regular FileSystemLoader but, instead of getting
    all the templates from a common directory, it uses different
    directory.  Each directory in the structure is separated by
    dots (.), not slash (/).  Furthermore, the 'views' sub-directory
    is still implicit.  For isntance:
        main.user.view
    Is replaced by the path:
        bundles/main/views/user/view
    
    """
    
    def get_source(self, environment, template):
        """Try and get the template from the given pseudo-pathname.
        
        It uses, like the Jinja2 documentation example, the getmtime
        function to know whether a template file had been changed
        or not.
        
        """
        if "/" not in template:
            path = template.split(".")
            # The first part of the path must be a bundle name
            # The other parts are the hierarchy of directory after 'views'
            bundle = path[0]
            sub_hierarchy = "/".join(path[1:])
            path = "bundles/" + bundle + "/views/" + sub_hierarchy + ".jj2"
        else:
            path = template
        
        if not exists(path):
            raise TemplateNotFound(template)
        
        mtime = getmtime(path)
        with open(path, 'r') as file:
            source = file.read()
        
        return source, path, lambda: mtime == getmtime(path)
