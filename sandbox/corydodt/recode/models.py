"""A box for holding models."""
import yaml

from dispatch import dispatcher

class Signal(object):
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
                lambda sender,property,value: self.reify(property, value)
                         )
        dispatcher.connect(self.receiver, self)

    def dictify(self):
        return {'TYPE': self.__class__.__name__}

    def reify(self, attr, value):
        reifier = getattr(self, 'reify_%s' % (attr,), self.reifyDefault)
        reifier(attr, value)

    def reifyDefault(self, attr, value):
        setattr(self, attr, value)

    def present(self):
        """Called to notify the gui that the object is ready to be displayed.
        Might do nothing.  Implement in subclasses.
        """


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
    def present(self):
        # FIXME - assumes the model has a location i.e. is actually on the map
        dispatcher.send(signal=self, 
                        sender='presenting', 
                        property='location', 
                        old=None, 
                        value=self.location)


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

def lazyModel(id):
    from net import model_registry
    def _():
        return model_registry[id]
    return _

class Connector(Modelable):
    def __init__(self):
        self.widget = None
        self._endpoints = [None, None]
        # connectors listen for changes to the locations of their endpoints:
        box.registerObserver(self)

        Modelable.__init__(self)

    def dictify(self):
        m = Modelable.dictify(self)
        from net import model_registry
        
        assert type(self.endpoints[0]) is not str
        assert type(self.endpoints[1]) is not str
        m.update({ 'endpoints': map(model_registry.get, self.endpoints),
                  })
        return m

    def reify_endpoints(self, attr, endpoints):
        from net import model_registry
        self.endpoints = map(lazyModel, endpoints)
    def set_endpoints(self, endpoints):
        assert None not in endpoints
        self._endpoints = endpoints
        if hasattr(self, '_realized_endpoints'):
            del self._realized_endpoints
    def get_endpoints(self):
        # finally do evaluation of an endpoint to a model.
        # cache it in _realized_endpoints.
        if getattr(self, '_realized_endpoints', None) is None:
            self._realized_endpoints = []
            for ep in self._endpoints:
                try:
                    model = ep()
                    self._realized_endpoints.append(model)
                except KeyError:
                    # tried to evalute the endpoint before it
                    # was reified.  Don't set _realized_endpoints in this
                    # case!
                    del self._realized_endpoints
                    return [None, None]

        assert not callable(self._realized_endpoints[0])
        assert not callable(self._realized_endpoints[1])
        return self._realized_endpoints
    endpoints = property(get_endpoints, set_endpoints)

    def receiveNewModel(self, sender, model):
        """Not interesting."""
        

    def receiveDropModel(self, sender, model):
        """If model is one of the endpoints, I should be destroyed too"""
        if sender == 'gui':
            print 'connector committing suicide. sender was', sender
            if model in self.endpoints:
                dispatcher.send(signal=Drop,
                                sender='connector',
                                model=self)

    def receivePropertyChange(self, 
                              signal, 
                              sender, 
                              property, 
                              old, 
                              value):
        if signal in self.endpoints:
            locations = self.locations
            dispatcher.send(signal=self,
                            sender='connector',
                            property='locations',
                            old=None,
                            value=locations)

    def get_locations(self):
        eps = self.endpoints
        return list(eps[0].location) + list(eps[1].location)
    def set_locations(self, val): 
        pass
    locations = property(get_locations, set_locations)


class TargetArrow(Connector):
    pass


class FollowArrow(Connector):
    pass




class Loader:
    """Creator for instances of any Modelable from flat dict"""
    def __init__(self):
        self.model_classes = {}

    def registerModelType(self, klass, key=None):
        if key is None:
            key = klass.__name__
        self.model_classes[key] = klass

    def fromDict(self, dict_data):
        classname = dict_data.pop('TYPE')
        obj = self.model_classes[classname]()
        for k, v in dict_data.items():
            obj.reify(k, v)
        return obj

    _default = {}
    def typeByName(self, name, default=_default):
        # _default is a klooge so typeByName can obey dict.get's semantics
        # without having to catch any exceptions
        if default is Loader._default:
            return self.model_classes.get(name)
        return self.model_classes.get(name, default)


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
