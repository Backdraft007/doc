# -*- coding: utf-8 -*-
"""
    sphinx.domains.rust
    ~~~~~~~~~~~~~~~~~~

    The Rust language domain.

    :copyright: Copyright 2007-2010 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from copy import deepcopy

from docutils import nodes

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode
from sphinx.util.compat import Directive
from sphinx.util.docfields import TypedField

from sphinxextra.utils import fixup_index_entry

_identifier_re = re.compile(r'\b(~?[a-zA-Z_][a-zA-Z0-9_\.]*[\[\]]*)')
_whitespace_re = re.compile(r'\s+(?u)')

class DefinitionParser(object):
    def __init__(self, definition):
        self.definition = definition.strip()
        self.pos = 0
        self.end = len(self.definition)
        self.last_match = None
        self._previous_state = (0, None)

    def fail(self, msg):
        raise DefinitionError('Invalid definition: %s [error at %d]\n  %s' %
            (msg, self.pos, self.definition))

    def match(self, regex):
        match = regex.match(self.definition, self.pos)
        if match is not None:
            self._previous_state = (self.pos, self.last_match)
            self.pos = match.end()
            self.last_match = match
            return True
        return False

    def skip_string(self, string):
        strlen = len(string)
        if self.definition[self.pos:self.pos + strlen] == string:
            self.pos += strlen
            return True
        return False

    def skip_ws(self):
        return self.match(_whitespace_re)

    @property
    def eof(self):
        return self.pos >= self.end

    @property
    def current_char(self):
        try:
            return self.definition[self.pos]
        except IndexError:
            return 'EOF'

    @property
    def matched_text(self):
        if self.last_match is not None:
            return self.last_match.group()

    def parse_type(self):
        return self._parse_type()

    def _parse_type(self):
        self.skip_ws()
        ref = self.skip_string("&")
        mut = self.skip_string("mut")
        self.skip_ws()

        tup = self.skip_string("(")
        if tup:
            tuple_params = []
            while not self.skip_string(")"):
                tuple_params.append(self.parse_type())
                self.skip_string(",")
                self.skip_ws()
            return "{ref}{mut}({params})".format(ref='&' if ref else '', mut="mut" if mut else '', params=', '.join(tuple_params))

        array = self.skip_string("[")
        if array:
            element_type = self._parse_type()
            self.skip_ws()
            if not self.skip_string(";"):
                self.fail("Expected ';' (between element type and count of array type)")
            self.skip_ws()
            if self.match(re.compile("\d*")):
                element_count = self.matched_text
            else:
                self.fail('Expected element count of array type')
            if not self.skip_string("]"):
                self.fail("Expected ']' as end of array type")
            return "{ref}{mut}[{type}; {count}]".format(ref='&' if ref else '', mut="mut" if mut else '', type=element_type, count=element_count)
        
        type_ = ""

        while self.match(_identifier_re):
            type_ += self.matched_text
            if not self.skip_string("::"):
                break
            else:
                type_ += "::"

        if type_ == "":
            self.fail('Expected type (identifier)')            

        generic = self.skip_string("<")
        if generic:
            generic_params = []
            while not self.skip_string(">"):
                generic_params.append(self.parse_type())
                self.skip_string(",")
                self.skip_ws()
            return "{ref}{mut}{t}<{params}>".format(ref='&' if ref else '', mut="mut" if mut else '', t=type_, params=', '.join(generic_params))

        return "{ref}{mut}{t}".format(ref='&' if ref else '', mut="mut" if mut else '', t=type_)

    def _parse_param(self):
        self.skip_ws()
        if self.skip_string('&self'):
            return addnodes.desc_parameter("&self","&self")

        if self.skip_string('&mut self'):
            return addnodes.desc_parameter("&mut self","&mut self")

        if self.match(_identifier_re):
            param_name = self.matched_text
        else:
            self.fail('Expected parameter name (identifier)')
        
        if not self.skip_string(':'):
            self.fail('Expected ":"')
        self.skip_ws()
        param_type = self._parse_type()

        param_text = "{name}: {t}".format(name=param_name, t=param_type)
        return addnodes.desc_parameter(param_text,param_text)

    def parse_function(self):        
        if self.match(_identifier_re):
            bricklet_name = self.matched_text            
        else:
            self.fail('Expected device name (identifier)')

        if not self.skip_string('::'):
            self.fail('Expected "::"')
        
        if self.match(_identifier_re):
            fn_name = self.matched_text
        else:
            self.fail('Expected function name (identifier)')

        is_generic = self.skip_string('<')
        if is_generic:
            if self.match(re.compile(".*>\(")):
               type_params = '<' + self.matched_text[:-1]               
            else:
                self.fail('Could not find end of generic type parameters')
        if not is_generic and not self.skip_string('('):
            self.fail('Expected "(" as start of parameter list')

        params = []
        while not self.skip_string(')'):
            params.append(self._parse_param())
            self.skip_ws()
            self.skip_string(',')

        self.skip_ws()
        returns_something = self.skip_string('->')
        if returns_something:
            self.skip_ws()
            return_type = self._parse_type()
        
        result = addnodes.desc_signature("pub fn " + self.definition)
        result['device'] = bricklet_name.replace("Bricklet", "").replace("Brick", "")
        result['struct'] = bricklet_name + "::"
        result['fn'] = fn_name
        result += addnodes.desc_addname("pub fn ", "pub fn ")
        result += addnodes.desc_addname(bricklet_name + "::", bricklet_name + "::")        
        result += addnodes.desc_name(fn_name, fn_name)
        if is_generic:
            result += addnodes.desc_addname(type_params,type_params)
        paramList = addnodes.desc_parameterlist()
        for param in params:
            paramList += param
        result += paramList
        if returns_something:
            result += addnodes.desc_returns(return_type, return_type)        
        return result

    def parse_constant(self):
        if self.match(_identifier_re):
            device_name = self.matched_text            
        else:
            self.fail('Expected device name (identifier)')

        if not self.skip_string('::'):
            self.fail('Expected "::"')
        
        if self.match(_identifier_re):
            constant_name = self.matched_text
        else:
            self.fail('Expected constant name (identifier)')

        if not self.skip_string(':'):
            self.fail('Expected ":"')
        t = self._parse_type()
        
        result = addnodes.desc_signature("pub const " + self.definition)
        result += addnodes.desc_addname(device_name + "::", device_name + "::")
        result += addnodes.desc_name(constant_name, constant_name)
        result += addnodes.desc_type(t)
        result['device'] = device_name
        result['struct'] = device_name + "::"
        result['fn'] = constant_name
        return result

    def assert_end(self):
        self.skip_ws()
        if not self.eof:
            self.fail('expected end of definition, got %r' %
                      self.definition[self.pos:])


class RustObject(ObjectDescription):
    """Description of a Rust language object."""

    def get_index_text(self, name_cls):
        if self.objtype == 'function':
            return _('%s() (built-in function)') % name_cls            
        elif self.objtype == 'callback':
            return _('%s() (built-in callback)') % name_cls
        elif self.objtype == 'data':
            return _('%s (built-in variable)') % name_cls
        else:
            return ''

    def add_target_and_index(self, sigobj, sig, signode):
        objects = self.env.domaindata['rust']['objects']
        fullname = signode['struct'] + signode['fn']
        signode['ids'].append(fullname)
        self.state.document.note_explicit_target(signode) # has to happen _after_ the fullname is added to the signodes' ids, as note_explicit_target generates the html id-attributes (i.e. link anchors)
        if fullname in objects:
            self.env.warn(
                    self.env.docname,
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]) +
                    ', use :noindex: for one of them',
                    self.lineno)
        objects[fullname] = (self.env.docname, self.objtype, signode)

        indextext = self.get_index_text(fullname)
        if indextext:
            self.indexnode['entries'].append(fixup_index_entry(('single', indextext, fullname, fullname, 'foobar')))
   
    def parse_definition(self, parser):
        raise NotImplementedError()

    def describe_signature(self, signode, arg):
        raise NotImplementedError()

    def handle_signature(self, sig, signode):
        parser = DefinitionParser(sig)
        try:
            rv = self.parse_definition(parser)
            signode['device'] = rv['device']
            signode['struct'] = rv['struct']
            signode['fn'] = rv['fn']
            parser.assert_end()
        except DefinitionError, e:
            self.env.warn(self.env.docname,
                          e.description, self.lineno)
            raise ValueError
        self.describe_signature(signode, rv)

        return rv

class RustFunctionObject(RustObject):
    def parse_definition(self, parser):
        return parser.parse_function()

    def describe_signature(self, signode, func):
        for node in func:
            signode += node

class DefinitionError(Exception):
    def __init__(self, description):
        self.description = description

    def __unicode__(self):
        return self.description

    def __str__(self):
        return unicode(self.encode('utf-8'))

class RustCurrentNamespace(Directive):
    """This directive is just to tell Sphinx that we're documenting
    stuff in namespace foo.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        return
        env = self.state.document.settings.env
        if self.arguments[0].strip() in ('NULL', '0', 'nullptr'):
            env.temp_data['rust:prefix'] = None
        else:
            parser = DefinitionParser(self.arguments[0])
            try:
                prefix = parser.parse_type()
                parser.assert_end()
            except DefinitionError, e:
                self.env.warn(self.env.docname,
                              e.description, self.lineno)
            else:
                env.temp_data['rust:prefix'] = prefix
        return []

class RustConstantObject(RustObject):
    def get_index_text(self, name):
        if self.objtype == 'constant':
            return _('%s (Rust constant)') % name
        return ''

    def parse_definition(self, parser):
        return parser.parse_constant()

    def describe_signature(self, signode, obj):
        for node in obj:
            signode += node

class RustXRefRole(XRefRole):
    def _fix_parens(self, env, has_explicit_title, title, target):
        if not has_explicit_title:
            if title.endswith('()'):
                # remove parentheses
                title = title[:-2]
            if env.config.add_function_parentheses:
                # add them back to all occurrences if configured
                #title += '()' # Matthias: dont add them back
                pass
        # remove parentheses from the target too
        if target.endswith('()'):
            target = target[:-2]
        return title, target


    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['rust:parent'] = env.temp_data.get('rust:parent')
        if not has_explicit_title:
            target = target.lstrip('~') # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[:1] == '~':
                title = title[1:]
                dcolon = title.rfind('::')
                if dcolon != -1:
                    title = title[dcolon + 2:]
        #return title, "AccelerometerBricklet::get_acceleration"
        return title, target


class RustDomain(Domain):
    """Rust language domain."""
    name = 'rust'
    label = 'Rust'
    object_types = {
        'function': ObjType(l_('function'), 'func')
    }

    directives = {
        'function':     RustFunctionObject,     
        'constant':     RustConstantObject,   
    }
    roles = {
        'func' :  RustXRefRole(fix_parens=True),
        'const' :  RustXRefRole(fix_parens=True)
     }
    initial_data = {
        'objects': {},  # fullname -> docname, objtype
    }

    def clear_doc(self, docname):
        for fullname, (fn, _, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]

    def _under_to_camel(self, string):
        splt = string.split("_")
        return "".join(x.title() for x in splt)

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        name, obj, node = self.data['objects'][target]

        return make_refnode(builder, fromdocname, name, target,
                                contnode, target)
    def get_objects(self):
        for refname, (docname, type, sig_node) in self.data['objects'].iteritems():
            yield (refname, refname, type, docname, refname, 1)

def setup(app):
    app.add_domain(RustDomain)
