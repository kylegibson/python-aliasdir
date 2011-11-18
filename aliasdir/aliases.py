import yaml
import pipes
from __future__ import with_statement

class MetaAliases(type):
    def __getitem__(self, k):
        return self.aliases[k]

    def __setitem__(self, k, v):
        aliases = self.aliases
        aliases[k] = self.quote(v)
        self.aliases = aliases

    def __delitem__(self, k):
        aliases = self.aliases
        if k in aliases:
            del aliases[k]
            self.aliases = aliases
        else:
            raise KeyError

    def quote(self, s):
        return pipes.quote(s)

    @property
    def aliases(self):
        try:
            with open(Aliases.FILE) as f:
                return yaml.safe_load(f)
        except IOError:
            pass
        return {}

    @aliases.setter
    def aliases(self, value):
        try:
            with open(Aliases.FILE, "w") as f:
                return yaml.safe_dump(value, f, default_flow_style=False)
        except IOError:
            pass
        return self.aliases

class Aliases:
    __metaclass__ = MetaAliases

