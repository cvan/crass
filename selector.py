
class Selector(object):
    def pretty(self):
        return unicode(self)


class MultiSelector(Selector):

    def __init__(self, selectors):
        self.selectors = selectors

    def matches(self, element):
        return any(s.matches(element) for s in self.selectors)

    def __unicode__(self):
        return u','.join(unicode(s) for s in self.selectors)

    def pretty(self):
        return u',\n'.join(s.pretty() for s in self.selectors)


class SimpleSelector(Selector):
    def __init__(self, rules=None):
        self.rules = rules or []

    def matches(self, element):
        return all(r.match(element) for r in self.rules)

    def __unicode__(self):
        return u''.join(unicode(r) for r in self.rules)

    def pretty(self):
        return u''.join(r.pretty() for r in self.rules)


class DescendantSelector(Selector):
    def __init__(self, ancestor, descendant):
        self.ancestor = ancestor
        self.descendant = descendant

    def matches(self, element):
        if not element.parentNode or not self.descendant.matches(element):
            return False
        parent = element.parentNode
        while parent:
            if self.ancestor.matches(parent):
                return True
            parent = element.parentNode
        return False

    def __unicode__(self):
        return u'%s %s' % (self.ancestor, self.descendant)

    def pretty(self):
        return u'%s %s' % (self.ancestor.pretty(), self.descendant.pretty())


class DirectDescendantSelector(DescendantSelector):
    def matches(self, element):
        return (self.descendant.matches(element) and
                self.ancestor.matches(element.parentNode))

    def __unicode__(self):
        return u'%s>%s' % (self.ancestor, self.descendant)

    def pretty(self):
        return u'%s > %s' % (self.ancestor.pretty(), self.descendant.pretty())


class AdjacencySelector(Selector):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def matches(self, element):
        if not element.previousSibling:
            return False
        return (self.second.matches(element) and
                self.first.matches(element.previousSibling))

    def __unicode__(self):
        return u'%s+%s' % (self.first, self.second)

    def pretty(self):
        return u'%s + %s' % (self.first.pretty(), self.second.pretty())


class SiblingSelector(Selector):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def matches(self, element):
        if not element.previousSibling or not self.second.matches(element):
            return False
        previous = element.previousSibling
        while previous:
            if self.first.matches(previous):
                return True
            previous = element.previousSibling

        return False

    def __unicode__(self):
        return u'%s~%s' % (self.first, self.second)

    def pretty(self):
        return u'%s ~ %s' % (self.first.pretty(), self.second.pretty())
