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


"""Module containing the wiki service (WikiService class).

This service is used to convert some text to HTML.  The converting
process, its rules, are described in the class documentation.

"""

import re

from ext.aboard.service import Service

class WikiService(Service):
    
    """Class describing the wiki service.
    
    This service is made to manipulate text and convert it to HTML format.
    The converting rules are highly customizable by inheriting from this
    class.  Most of the constants used to convert text to HTML
    are created in the constructor.  Therefore, others may be added
    very simply.
    
    Here is a short example that shows how to add a new markup
    to the wiki syntax.  You can add a new 'wiki.py' file in your
    'services' package placed in your bundle, and then paste the following
    code into the file:
    >>> from ext.aboard.service.default import WikiService
    >>> class wiki(WikiService)  # It's important to name -that class Wiki
    ...     def __init__(self):
    ...         Wikiservice.__init__(self)
    ...         self.add_markup("bold", "b", "<strong>{string}</strong>")
    
    You can also change the delimiters for the markup, add new regular
    expressions, delete markups, etc.  Have a look at the class methods.
    
    """
    
    name = "wiki"
    def __init__(self, start="&lt;", end="&gt;", close="/"):
        """Service constructor."""
        Service.__init__(self)
        self.markup_delimiter_start = start
        self.markup_delimiter_end = end
        self.markup_delimiter_close = close
        self.expressions = []
        self.exceptions = []
        
        # Add the exceptions
        self.add_except_expression("@", "@")
        self.add_except_markup("pre")
        
        
        # Add the expressions and markups
        self.add_expression("italic", "/(.*?)/", "<em>\\1</em>")
        self.add_expression("bold", r"\*(.*?)\*", "<strong>\\1</strong>")
        self.add_expression(
                "header1",
                r"^(\s*)h1\.\s+(.*?)\s*$",
                r"\1<h1>\2</h1>",
                re.MULTILINE
        )
        
        # Test (o delete)
        text = """
            h1. A test
            This is some text with *that* in bold,
            But @*this part* h1. should@ not be interpreted at all.
            <pre>
            This one is a *long*
            non /interpreted/ text, somehow.</pre>
            and, finally, /this should be in italic/ and *bold*.
            Well, @that *one* again@.
        """
        print("Convert", self.convert_text(text))
    
    def add_expression(self, name, regexp, replacement, options=0):
        """Add a new regular expression.
        
        This methods automatically compiles the given regular expression and
        adds the result to the self.expressions list.
        
        Expected arguments:
            name -- the name of the expression (see below)
            regexp -- the regular expression which will be compiled
            options [optionnal] -- the regular expression options.
        
        An expression name should be a unique identifier.  It's mostlu used
        to replace an expression (if a developer decides to change the
        rule to create bold text, for instance, he will use this identifier).
        
        """
        name = name.lower()
        names = [line[0] for line in self.expressions]
        if name in names:
            raise ValueError("the identifier {} already exists in the " \
                    "expression list.  Use the 'replace_expression' " \
                    "method to replace it".format(repr(name)))
        
        compiled = re.compile(regexp, options)
        self.expressions.append((name, compiled, replacement))
    
    def replace_expressions(self, name, regexp, replacement, options=0):
        """Replace an existing expression using its identifier.
        
        The expected arguments are the same as the 'add_expression' method.
        Instead of simply adding a new expression, though, it first delete
        the expression with the name.  This is very useful to define a new
        rule for certain formatting.
        
        """
        name = name.lower()
        names = [line[0] for line in self.expressions]
        if name not in names:
            raise ValueError("the identifier {} doesn't exists in the " \
                    "expression list.  Use the 'add_expression' " \
                    "method to add it".format(repr(name)))
        
        compiled = re.compile(regexp, options)
        exp_pos = names.find(name)
        del self.expressions[exp_pos]
        self.expressions.insert(exp_pos, (name, compiled, replacement))
    
    def remove_expression(self, name):
        """Remove the expression identified by its name."""
        name = name.lower()
        names = [line[0] for line in self.expressions]
        if name not in names:
            raise ValueError("the identifier {} doesn't exists in the " \
                    "expression list.".format(repr(name)))
        
        exp_pos = names.find(name)
        del self.expressions[exp_pos]
    
    def add_except_expression(self, start, end, options=0):
        """Add an expression for a Wiki exception.
        
        Exceptions are not interpreted.  If this expression is found, it is
        deleted and its content (the second group) is copied into a
        temporary field and paste in the original text, unchanged, at the end of the process.
        
        """
        self.exceptions.append((start, end, options))
        
    def add_markup(self, name, markup, html):
        """Add a new markup.
        
        A wiki markup is by default close to a HTML markup.  It should
        begin with &gt; (<), end with &lt; (>).  To close the markup
        after the text to select, it use another &gt; followed
        by /, the markup and the &lt; symbol.
        
        These three symbols (markup_delimiter_start, markup_delimiter_end
        and markup_delimiter_close) are instance attributes and can be
        set in the constructor of a subclass.  this allows to
        set new markup symbols, brackets for instance.
        
        Note: the 'html' parameter should contain the '{string}'
        sub-string to identify a replacement.  For instance:
        >>> wiki.add_markup("italic", "i", "<em>{string}</em>")
        That code will allow text like:
            We <i>made</i> it!
        To:
            We <em>made</em> it!
        
        """
        start = self.markup_delimiter_start
        end = self.markup_delimiter_end
        close = self.markup_delimiter_close
        regexp = start + markup + end + "(.*?)" + start + close + markup + end
        replacement = html.format(string="\\1")
        self.add_expression(name, regexp, replacement)
    
    def replace_markup(self, name, markup, html):
        """Replace the identified by markup.
        The expected arguments are the same ones as the 'add_markup' method.
        The markup name has to exist, though.
        
        """
        start = self.markup_delimiter_start
        end = self.markup_delimiter_end
        close = self.markup_delimiter_close
        regexp = start + markup + end + "(.*?)" + start + close + markup + end
        replacement = html.format(string="\\1")
        self.replace_expression(name, regexp, replacement)
    
    def remove_markup(self, name):
        """Remove the markup."""
        self.remove_expression(name)
    
    def add_except_markup(self, markup):
        """Add a markup exception."""
        start = self.markup_delimiter_start
        end = self.markup_delimiter_end
        close = self.markup_delimiter_close
        markup_start = start + markup + end
        markup_end = start + close + markup + end
        self.add_except_expression(markup_start, markup_end, re.DOTALL)
    
    def convert_text(self, text):
        """Return the HTML text converted from the text argument."""
        raw_text = self.get_raw_text(text)
        raw_text = raw_text.replace("{", "{{").replace("}", "}}")
        
        # First remove the exceptions
        raw_exceptions = {}
        tmp_exceptions = []
        def replace(match):
            name = "exp_" + str(i) + "_" + str(len(tmp_exceptions))
            tmp_exceptions.append(None)
            return "{" + name + "}"
        
        for i, (start, end, opts) in enumerate(self.exceptions):
            tmp_exceptions = []
            s_regexp = start + "(.*?)" + end
            r_regexp = "(" + start + ".*?" + end + ")"
            for j, content in enumerate(re.findall(s_regexp, raw_text, opts)):
                name = "exp_" + str(i) + "_" + str(j)
                raw_exceptions[name] = content
            
            raw_text = re.sub(r_regexp, replace, raw_text, flags=opts)
        
        for name, regexp, replacement in self.expressions:
            raw_text = regexp.sub(replacement, raw_text)
        
        return raw_text.format(**raw_exceptions)
    
    @staticmethod
    def get_raw_text(text):
        """Escape the HTML characters."""
        to_esc = {
            "<": "&lt;",
            ">": "&gt;",
        }
        for car, repl in to_esc.items():
            text = text.replace(car, repl)
        
        return text
