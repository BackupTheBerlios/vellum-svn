"""A box for holding models."""
import yaml

from dispatch import dispatcher

class Signal:
    pass


class New(Signal):
    """A new modelable has arrived"""

class Drop(Signal):
    """A modelable object is no longer interesting"""

class Modelable(Signal):
    def __init__(self):
        # FIXME? if receiver is a regular method, I get 
        # TypeError: unsubscriptable object from pydispatcher when
        # the Modelable is gc'd.
        # when it's a lambda held in an instance variable, no error.
        self.receiver = (
                lambda sender,property,value: setattr(self, property, value)
                         )
        dispatcher.connect(self.receiver, self)

    def dictify(self):
        return {'TYPE': self.__class__.__name__}


class BiDict(dict):
    """Simple bi-di dict.  Not exactly optimized,
    but probably fast enough.
    """
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        value = self[key]
        dict.__delitem__(self, key)
        dict.__delitem__(self, value)

    def values(self):
        assert 0, "Unsupported operation"
    iterkeys = itervalues = keys = values

    def items(self, keytype):
        """Return items(), filtering to get only
        tuples where the key is of type keytype.
        """
        return tuple([items for items in dict.items(self) 
                        if type(items[0]) is keytype])


    def iteritems(self, keytype):
        """Return iteritems(), filtering to get only
        tuples where the key is of type keytype.
        """
        for k,v in dict.iteritems(self):
            if type(k) is keytype:
                yield k,v


class Draggable(Modelable):
    def __init__(self):
        self.location = (40, 50)
        self.widget = None
        self.grabbed = self.selected = 0
        Modelable.__init__(self)
    def dictify(self):
        m = Modelable.dictify(self)
        m.update({ 'location': self.location, })
        return m


class Character(Draggable):
    def __init__(self):
        self.image = None
        Draggable.__init__(self)

class Note(Draggable):
    def __init__(self):
        self.text = 'NOTE'
        Draggable.__init__(self)
    def dictify(self):
        m = Modelable.dictify(self)
        m.update({ 'text': self.text, })
        return m

class Connector(Modelable):
    def __init__(self):
        self.widget = None
        self.endpoints = [None, None]
        Modelable.__init__(self)
    def dictify(self):
        m = Modelable.dictify(self)
        m.update({ 'endpoints': self.endpoints, })
        return m


class TargetArrow(Connector):
    pass


class FollowArrow(Connector):
    pass

class Loader:
    """Creator for instances of any Modelable from flat dict"""
    def __init__(self):
        self.models = {}

    def registerModelType(self, klass, key=None):
        if key is None:
            key = klass.__name__
        self.models[key] = klass

    def fromDict(self, dict_data):
        classname = dict_data.pop('TYPE')
        klass = self.models[classname]
        ret = klass()
        for k, v in dict_data.items():
            setattr(ret, k, v)
        return ret

    _default = {}
    def typeByName(self, name, default=_default):
        # _default is a klooge so typeByName can obey dict.get's semantics
        # without having to catch any exceptions
        if default is Loader._default:
            return self.models.get(name)
        return self.models.get(name, default)


loader = Loader()
# set up all Type names that appear in .yml files here
for klass in [ Character, 
               Note, 
               TargetArrow, 
               FollowArrow ]:
    loader.registerModelType(klass)


class BoxScore:
    """Event tracker.  One must exist on either side of the connection.
    The BoxScore keeps track of the actions of the players (observers) and
    the balls (models).

    In particular, the BoxScore will process New and Drop signals, keeping the
    local observers up to date on what models exist, and changes to the list
    of observers must be done through here by calling
    register/unregisterObserver.
    """
    def __init__(self):
        # these use strong references to avoid a warning when they are
        # garbage collected.
        dispatcher.connect(self.receiveNew, signal=New, weak=False)
        dispatcher.connect(self.receiveDrop, signal=Drop, weak=False)

        self.observers = []
        self.models = []

    def registerObserver(self, observer):
        for model in self.models:
            dispatcher.connect(observer.receivePropertyChange, signal=model)
        dispatcher.connect(observer.receiveNewModel, signal=New)
        dispatcher.connect(observer.receiveDropModel, signal=Drop)
        self.observers.append(observer)

    def unregisterObserver(self, observer):
        dispatcher.disconnect(observer.receiveDropModel, signal=Drop)
        dispatcher.disconnect(observer.receiveNewModel, signal=New)
        for model in self.models:
            dispatcher.disconnect(observer.receivePropertyChange, signal=model)
        self.observers.remove(observer)

    def receiveDrop(self, sender, signal, model):
        if sender is self:
            return
        for observer in self.observers:
            dispatcher.disconnect(observer.receivePropertyChange, signal=model)
        self.models.remove(model)

    def receiveNew(self, sender, signal, model):
        if sender is self:
            return
        self.models.append(model)
        for observer in self.observers:
            dispatcher.connect(observer.receivePropertyChange, signal=model)

box = BoxScore()
