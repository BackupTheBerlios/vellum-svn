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
        dispatcher.connect(self.receivePropertyChange, self)
    def receivePropertyChange(self, property, value):
        setattr(self, property, value)


class Icon(Modelable):
    def __init__(self):
        self.location = (40, 50)
        self.image = self.widget = None
        self.grabbed = self.selected = 0
        Modelable.__init__(self)

class Box:
    def __init__(self):
        dispatcher.connect(self.receiveNew, New) 
        dispatcher.connect(self.receiveDrop, Drop)
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
            dispatcher.disconnect(observer.receiveDropModel, signal=Drop)
            dispatcher.disconnect(observer.receiveNewModel, signal=New)
            dispatcher.disconnect(observer.receivePropertyChange, signal=model)
        self.models.remove(model)

    def receiveNew(self, sender, signal, model):
        if sender is self:
            return
        self.models.append(model)
        for observer in self.observers:
            dispatcher.connect(observer.receivePropertyChange, signal=model)
            dispatcher.connect(observer.receiveNewModel, signal=New)
            dispatcher.connect(observer.receiveDropModel, signal=Drop)

