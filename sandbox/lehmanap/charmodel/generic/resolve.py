import new
import pdb
from zope.interface import interface, implements
from twisted.python import components
import types
import utils
tabbies = ""

#Zope specific
from zope.component import interfaces

class ICondition( interface.Interface ):
    """
    Represents a logical condition.
    """
    original=interface.Method("original", """The function representing the test condition.  Should take a context object.""")
    
    def andCondition( condition ):
        """
        Returns an ICondition that is equivalent to 'self and condition'
        """
        pass

    def orCondition( condition ):
        """
        Returns an ICondition that is equivalent to 'self or condition'
        """
        pass

    def notCondition( ):
        """
        Returns an ICondition that is equivalent to 'not self'
        """
        pass

    def __call__( context ):
        """
        Tests the condition with the given context
        """
        pass

class IResolveable( interface.Interface ):
    """
    An object that can be resolved by a Resolver.
    """

    condition=interface.Attribute("condition",
        """Callable that checks to determine if a resolveable should be resolved.""")
    function=interface.Attribute("function",
        """Base function to be resolved.""")
    func_name=interface.Attribute("func_name",
        """Name of the function to be resolved.""")
    name=interface.Attribute("name",
        """Name of the Resolveable.""")
    modifiers=interface.Attribute("modifiers",
        """Iterable of the resolveable that need to be resolved before this resolveable.""")

    def add( self, modifier ):
        """Add a modifier to the list."""
        pass

    def __call__( self, context ):
        """
        Calls the function under the given context.
        """
        pass

class IModifier( IResolveable ):
    """
    Wraps a function, altering the return value.  Maintains a link to its
    creator and its target.
    """
    modtype=interface.Attribute("type", """The type of modifier.""")
    parent=interface.Attribute("parent", """The creator of this modifier.""")
    target=interface.Attribute("target", """The target of this modifier.""")
    key=interface.Attribute("key", """The unique key of this modifier.""")

class IResolver( interface.Interface ):
    context=interface.Attribute( "context",
        """The context under which this resolver will operate.""" )
    filterfunction=interface.Attribute( "filterfunction",
        """The function that will be used to filter modifiers.""" )

    def filter( self, value ):
        """Filters modifiers based on type.  Might be subclassed for other filtering."""
        pass

    def resolveBase( node, condense, level, name=None ):
        """Resolve a particuler node."""
        pass

    def resolveTotal( self, target, condense, level, name=None ):
        """Resolve the total."""
        pass

    def resolveModifier( node, condense, level, name=None ):
        """Resolve a particuler modifier."""
        pass

    def getRequiredResults( results ):
        """Pull the results we want out of the total results."""
        pass

    def resolve( target, condense, level=0 ):
        """Resolve the target in the context of self.context."""
        pass

class IIntResolver( IResolver ):
    """A resolver that resolves to ints."""
    pass

class Resolver( object ):
    """
    Allows Resolveable objects to be resolved in different ways, in different
    contexts.  Basically, this is the View to the Resolveable's Model.
    """
    implements( IResolver )

    def __init__( self, context, evaluate=None, cap=None, identity=None, filterfunction=None ):
        self.context=context
        self.cap=cap
        self.identity=identity
        evaluate=evaluate or (lambda self, base, context: base.function( context ))
        if type(evaluate)==types.FunctionType:
            evaluate=new.instancemethod(evaluate, self, self.__class__)
        self.evaluate=evaluate
        filterfunction=filterfunction or (lambda self, value, modtype=None: value)
        self.modifiers = { }
        if type(filterfunction)==types.FunctionType:
            filterfunction=new.instancemethod(filterfunction, self, self.__class__)
        self.filterfunction=filterfunction

    def filter( self, value ):
        value=IModifier(value)
        key=(value.modtype, value.target)
        mods=self.modifiers.get(key, [])
        if self.cap is not None and len(mods) > self.cap:
            return self.identity
        else:
            self.modifiers[key]=mods
            self.modifiers[key].append(value)
            return self.filterfunction(value, type)

    def collect( self, target, modtype=None ):
        """Collect all resolveables that are relevant to the target."""
        def collectNode( node ):
            if IResolveable.providedBy( node ) and IResolveable.providedBy( node.function ):
                return [ self.collect( IResolveable( node.function ), type ) ] + [ self.collect( mod, type ) for mod in IResolveable(node).modifiers ]
            else:
                return node

        def buildDict( target, base, modifiers ):
            return {'condition': target.condition, 'base': base, 'modifiers': modifiers}

        base =  collectNode( target )
        modifiers = [ self.collect( node ) for node in IResolveable( target ).modifiers ]
        return buildDict( target, base, modifiers )

    def resolveBase( self, node, condense, level, name=None ):
        """Resolve the base."""
        raise NotImplementedError( )

    def resolveModifier( self, node, condense, level, name=None ):
        """Resolve the modifier."""
        raise NotImplementedError( )

    def resolveTotal( self, node, condense, level, name=None ):
        """Resolve the total."""
        raise NotImplementedError( )

    def getRequiredResults( self, results ):
        """Get required results."""
        return results[1:]

    def resolve( self, target, condense, level=0 ):
        if IResolveable(target).condition(self.context):
            total=[self.resolveTotal(target, condense, level)]
            base=[self.resolveBase(target, condense, level+1, 'Base')]
            mods=[self.resolveModifier(mod, condense, level+1) for mod in target.modifiers if self.filter(mod)]
            result=self.getRequiredResults(total + base + mods)
        else:
            result=[]
        return condense(result)

class IntResolver( Resolver ):
    """
    Convenience class.  Resolves all applicable Resolveables as ints.
    """
    implements( IIntResolver )

    def __init__( self, context, cap=1, identity=0, filterfunction=None ):
        super( IntResolver, self ).__init__( context, (lambda self, target: target.function(self)), cap, identity, filterfunction )

    def resolveBase(self, node, condense, level, name=None):
        n=IResolveable(node)
        resolved=self.evaluate(n)
        if IResolveable.providedBy(resolved):
            r=IResolveable(resolved)
            resolved=self.resolve(r, condense, level + 1)
        return resolved
    resolveModifier=resolveTotal=resolveBase

class IntResolverAdapter(IntResolver):
    """
    >>> context = Resolver( 5 )
    >>> int_context = IntResolver( 5 )
    >>> IIntResolver(context).__class__
    <class '__main__.IntResolverAdapter'>
    >>> IIntResolver(int_context).__class__
    <class '__main__.IntResolver'>
    """
    def __init__( self, context ):
        c=IResolver(context)
        super(IntResolverAdapter, self).__init__( c.context, c.cap, c.identity, new.function(c.filterfunction.im_func.func_code, globals()) )

components.registerAdapter(
    IntResolverAdapter,
    Resolver,
    IIntResolver)

class Resolveable( object ):
    """
    A Resolveable is a wrapper for a function, allowing it to be resolved
    conditionally, and under different contexts.  Basically, the Model to the
    Resolver's View.
    
    Create a couple of functions.
    >>> def function_add_10( self, x ):
    ...  return x + 10
    >>> def function_add_5( self, x ):
    ...  return x + 5

    Make Resolveables out of them.
    >>> resolveable5 = Resolveable( "add_5", function_add_5 )
    >>> resolveable10 = Resolveable( "add_10", function_add_10 )
    >>> resolveable_2layer = Resolveable( "resolveable10", resolveable10 )
    >>> resolveable_2layer.condition = resolveable_2layer.condition.andCondition( Condition(lambda context: context % 2 != 0) )

    Make Resolvers in different contexts.
    >>> int_context = IntResolver( 5 )

    >>> int_context.resolve( resolveable_2layer, sum )
    15

    """
    implements(IResolveable)

    def __init__(self, name, function, condition=None, modifiers=None):
        if callable(function):
            if type(function) == types.FunctionType:
                function=new.instancemethod(function, self, self.__class__)
            self.function=function
        else:
            self.function=new.instancemethod(lambda self, context:function, self, self.__class__)
        self.condition=ICondition( condition or (lambda context: True) )
        self.modifiers=modifiers or [ ]
        self._name=name

    def _getFuncName( self ):
        return self.function.func_name

    func_name=property(fget=_getFuncName, doc="""Name of the function to be resolved.""")

    def _getName( self ):
        return self._name

    def _setName( self, value ):
        self._name = value

    name=property(fget=_getName, fset=_setName, doc="""Name of the resolveable.""")

    def __call__( self, resolver ):
        return self.function( resolver.context )

components.registerAdapter(
    Resolveable,
    types.FunctionType,
    IResolveable)

components.registerAdapter(
    Resolveable,
    types.IntType,
    IResolveable)

components.registerAdapter(
    Resolveable,
    types.StringType,
    IResolveable)

class Modifier( Resolveable ):
    implements( IModifier )

    def __init__( self, modtype, parent, target, function, condition ):
        super(Modifier, self).__init__(None, function, condition)
        self.modtype = modtype
        self.parent = parent
        self.target = target

    #Properties
    def getKey( self ):
        return self.parent.key
    key = property( fget=getKey, doc="The unique key for this Modifier's ModifierFactory" )

    def _getName( self ):
        return "Modifier for %s generated by %s" % (self.target.name, self.parent.name)
    name=property( fget=_getName, doc="The name of this modifier." )

class Condition( object ):
    """
    Represents a logical condition.

    Set up a couple simple Conditions.
    >>> values = [1]
    >>> odd = Condition(lambda *args, **kwargs: values[0] % 2 != 0)
    >>> even = Condition(lambda *args, **kwargs: values[0] % 2 == 0)

    Odd is odd, and Even is even.
    >>> values[0] = 1
    >>> odd(None)
    True
    >>> values[0]=0
    >>> odd(None)
    False
    >>> values[0] = 1
    >>> even(None)
    False
    >>> values[0]=0
    >>> even(None)
    True

    We can modify the conditions after they are set up via andCondition, orCondition, and notCondition methods.
    First, lets save the old ones, so we can reset for each test.
    >>> oldconditions = (even, odd)

    Notted odd is the same as even.
    >>> even, odd = oldconditions
    >>> odd = odd.notCondition( )
    >>> values[0] = 1
    >>> odd(None)
    False
    >>> values[0] = 0
    >>> odd(None)
    True

    Now odd is true if its odd, or divisible by 8.
    >>> even, odd = oldconditions
    >>> odd = odd.orCondition( lambda context: values[0] % 8 == 0 )
    >>> values[0] = 1
    >>> odd(None)
    True
    >>> values[0] = 8
    >>> odd(None)
    True

    But not otherwise.
    >>> values[0] = 2
    >>> odd(None)
    False

    Now odd is true if it is odd AND negative.
    >>> even, odd = oldconditions
    >>> odd = odd.andCondition( lambda context: values[0] < 0 )
    >>> values[0] = -1
    >>> odd(None)
    True

    But not if just one, or neither, is true
    >>> values[0] = 1
    >>> odd(None)
    False
    >>> values[0] = -2
    >>> odd(None)
    False
    >>> values[0] = 2
    >>> odd(None)
    False

    Wild and crazy types might even mix and match.  Now the value cannot be both odd and negative.
    >>> even, odd = oldconditions
    >>> odd = odd.andCondition( lambda context: values[0] < 0 ).notCondition( )
    >>> values[0] = -1
    >>> odd(None)
    False

    Either one will work, however
    >>> values[0] = 1
    >>> odd(None)
    True
    >>> values[0] =-2
    >>> odd(None)
    True

    """
    implements( ICondition )
    
    def __init__( self, original=True ):
        if callable(original):
            self.original=original
        else:
            self.original=lambda context: True
    
    def andCondition( self, condition ):
        """
        Returns an ICondition that is equivalent to 'self and condition'
        """
        condition=ICondition( condition )
        return Condition( lambda context: self( context ) and condition( context ) )

    def orCondition( self, condition ):
        """
        Returns an ICondition that is equivalent to 'self or condition'
        """
        condition=ICondition( condition )
        return Condition( lambda context: self( context ) or condition( context ) )

    def notCondition( self ):
        """
        Returns an ICondition that is equivalent to 'not self'
        """
        return Condition( lambda context: not self( context ) )

    def __call__( self, context ):
        """
        Tests the condition with the given context
        """
        return self.original( context )

components.registerAdapter(
    Condition,
    types.FunctionType,
    ICondition)

components.registerAdapter(
    Condition,
    types.ObjectType,
    ICondition)

def foo(context, resolveable, function):
    #import pdb; pdb.set_trace()
    return context.resolve( resolveable, function )

def _test():
    import doctest
    doctest.testmod(verbose=True)
    #doctest.testmod()

if __name__ == '__main__':
    _test()
