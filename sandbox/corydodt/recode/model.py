"""A box for holding models."""

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



class Icon(Modelable):
    def __init__(self):
        self.location = (40, 50)
        self.image = self.widget = None
        self.grabbed = self.selected = 0
        Modelable.__init__(self)

class Box:
    def __init__(self):
        dispatcher.connect(self.receiveNew, signal=New) 
        dispatcher.connect(self.receiveDrop, signal=Drop)
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

