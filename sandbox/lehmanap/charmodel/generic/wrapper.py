import pdb
tabbies = ""

class Observer( object ):
    def __init__( self, label ):
        self.label = label

    def observed( self, obj, function ):
        print "%s observed %s" % ( self.label, function )

class ObservedMethod( object ):
    def __init__( self, meth ):
        self.method = meth
        self.observers = [ ]

    def __call__( self, *args, **kwargs ):
        for observer in self.observers:
            observer.observed( self.method )
        return self.method( *args, **kwargs )

    def add( self, observer ):
        self.observers.append( observer )

class ConditionalMethod( object ):
    def __init__( self, methods, conditionType ):
        try:
            self.method, self.altmethod = methods
        except:
            self.method, self.altmethod = [ methods, ( lambda *args, **kwargs: 0 ) ]
        self.condition = conditionType( )

    def __call__( self, *args, **kwargs ):
        return self.condition and self.method( *args, **kwargs ) or self.altmethod( *args, **kwargs )

    def add( self, condition ):
        try:
            self.condition.extend( condition )
        except:
            self.condition.append( condition )

class AndConditionalMethod( ConditionalMethod ):
    def __init__( self, meth ):
        super( AndConditionalMethod, self ).__init__( meth, AndCondition )

class OrConditionalMethod( ConditionalMethod ):
    def __init__( self, meth ):
        super( AndConditionalMethod, self ).__init__( meth, OrCondition )

class Wrappable( object ):
    def __init__( self, func, returntype=ObservedMethod ):
        self.func = func
        self.wrapped = { }
        self.returntype = returntype

    def __get__( self, obj, objtype=None ):
        if obj is None:
            return self.func
        return self.wrapped[ obj ]
    
    def __set__( self, obj, newfunc ):
        if obj is None:
            self.func = newfunc
        self.wrapped[ obj ] = self.returntype( newfunc )
    
    def __delete__( self, obj ):
        if obj is None:
            del self.func
        del self.wrapped[ obj ]

    def get__doc__( self ):
        return self.func.__doc__
    __doc__ = property( fget=get__doc__ )

class Observable( Wrappable ):
    def __init__( self, func ):
        super( Observable, self ).__init__( func, ObservedMethod )

class Conditionable( Wrappable ):
    def __init__( self, func, conditionalType=None ):
        conditionalType=conditionalType or AndCondition
        wrappertype = ( lambda meth, conditionalType=conditionalType: ConditionalMethod( meth, conditionalType ) )
        super( Conditionable, self ).__init__( func, wrappertype )

class WrappableObject( object ):
    def __new__( clss, *args, **kwargs ):
        obj = object.__new__( clss, *args, **kwargs )
        for methname, meth in [ ( m, getattr( clss, m ) ) for m in dir( clss ) if callable( getattr( clss, m ) ) ]:
            import new
            try:
                setattr( obj, methname, new.instancemethod( meth, obj, clss ) )
            except TypeError:
                pass
        return obj

class MyObject( WrappableObject ):
    def __str__( self ):
        return "%s.%s" % ( self.__class__.__module__, self.__class__.__name__ )

    def __repr__( self ):
        return "%s %s" % ( str( self ), super( MyObject, self ).__repr__( ) )

class Condition( MyObject, Observer ):
    def __init__( self, func=None ):
        self.func = func or ( lambda: True )

    def observed( self, func ):
        return self.func( func )

class MassCondition( Condition ):
    def __init__( self, conditions=None ):
        self.conditions = [ condition for condition in ( conditions or [ ] ) ]

    def __iter__( self ):
        return iter( self.conditions )

    def append( self, condition ):
        self.conditions.append( condition )

    def extend( self, conditions ):
        self.conditions.extend( conditions )

class AndCondition( MassCondition ):
    def observed( self, meth ):
        for condition in self.conditions:
            if not condition( meth.im_self, meth ):
                return False
        return True

class OrCondition( MassCondition ):
    def observed( self, meth ):
        for condition in self.conditions:
            if condition( meth.im_self, meth ):
                return True
        return False


