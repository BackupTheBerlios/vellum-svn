from charmodel.generic.effect import DamageEffect
from charmodel.generic.generator import CharacterClass, EffectGenerator, Race
from effect import D20CharacterLevel

class D20Attack( EffectGenerator ):
    def __init__( self, session, subject, object, rolls=None ):
        super( D20Attack, self ).__init__( 'Damage', session, { 'WOUNDS': 0 }, { }, DamageEffect )
        self.subject = subject
        self.object = object
        self.tool = self.subject.weapon
        self.rolls = rolls or [ ]
        self.dmg = None

    def resolve( self, roll=None, croll=None ):
        if self.isAHit( roll ): 
            if self.rolls[ 0 ] in self.tool.CRIT_RANGE and self.isACrit( croll ):
                self.dmg = self.getCrit( )
            else:
                self.dmg = self.getDamage( )
            self.object.effects.append( self.dmg )
            self.dmg.enable( )
        return self.dmg

    def isAHit( self, roll=None ):
        if roll:
            self.rolls.append( roll )
        if not self.rolls:
            from vellum.server.dice import parse
            self.rolls.extend( parse( "1d20" ).sum( ) )
        #This will need to be fixed for situations where the att or AC changes based on the defender or attacker
        return ( self.rolls[ 0 ] != 1 ) and ( ( self.rolls[ 0 ] + self.tool.ATT ) > self.object.AC or ( self.rolls[ 0 ] ) == 20 )

    def isACrit( self, croll=None ):
        if croll:
            self.rolls.append( croll )
        if len( self.rolls ) < 2:
            from vellum.server.dice import parse
            self.rolls.extend( parse( "1d20" ).sum( ) )
        #This will need to be fixed for situations where the att or AC changes based on the defender or attacker
        return ( self.rolls[ 1 ] != 1 ) and ( ( self.rolls[ 1 ] + self.tool.ATT ) > self.object.AC or ( self.rolls[ 1 ] ) == 20 )

    def getDamage( self, mods=None ):
        dmg = self.getEffect( self.object, mods )
        dmg.factories[ self.object.WOUNDS ] = ( self.subject.weapon.DAMAGE.mod, 'DAMAGE', ( ) )
        return dmg

    def getCrit( self, mods=None ):
        dmg = self.getEffect( self.object, mods )
        dmg.factories[ self.object.WOUNDS ] = ( self.subject.weapon.CRITICAL.mod, 'DAMAGE', ( ) )
        return dmg

    def __str__( self ):
        return "%s is doing something with %s using a(n) %s" % ( self.subject, self.object, self.tool )

class D20CharacterClass( CharacterClass ):
    def __init__( self, name, session, levels, hitdice, mods, feats ):
        mods[ 'EL' ] = mods.get( 'EL', [ 1 ] * 20 )
        self.hitdice = hitdice
        super( D20CharacterClass, self ).__init__( name, session, levels, mods, feats )
        self.leveltype = D20CharacterLevel

class D20Race( Race ):
    def __init__( self, name, session, mods, feats ):
        mods[ 'EL' ] = mods.get( 'EL', [ 0 ] * 20 )
        super( D20Race, self ).__init__( name, session, 20, mods, feats )
