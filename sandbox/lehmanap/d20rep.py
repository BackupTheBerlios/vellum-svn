from rep import *

class D20CharacterClass( CharacterClass ):
    def __init__( self, name, session, levels, hitdice, mods, feats ):
        mods[ 'EL' ] = mods.get( 'EL', [ 1 ] * 20 )
        self.hitdice = hitdice
        super( D20CharacterClass, self ).__init__( name, session, levels, mods, feats )
        self.leveltype = D20CharacterLevel

class D20CharacterLevel( CharacterLevel ):
    def __init__( self, character, levelnum, charlevelnum, characterclass, mods=None, feats=None ):
        super( D20CharacterLevel, self ).__init__( character, levelnum, charlevelnum, characterclass, mods, feats )
        from dice import Roller
        roller = Roller( )
        if charlevelnum == 1:
            rollstring = characterclass.hitdice[ levelnum ]
        else:
            rollstring = "1d%s" % characterclass.hitdice[ levelnum ]
        self.hp = D20HP( 'Hit Points', sum( roller.roll( rollstring ) ) )
        character.CON.modprovided.addTarget( self.hp, 'RANKS' )
        self.factories[ character.HP ] = ( self.hp.modprovided, 'Level Modifier', Conditions.compileCondition( ( ) ) )

class D20Stat( Stat ):
    def __init__( self, name, number, modsprovided=None, aggregator=None ):
        super( D20Stat, self ).__init__( name, number, modsprovided, aggregator )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20HP( D20Stat ):
    def __init__( self, name, number ):
        super( D20HP, self ).__init__( name, number )
        self.mod = lambda: max( 1, int( self ) )

class D20Race( Race ):
    def __init__( self, name, session, mods, feats ):
        mods[ 'EL' ] = mods.get( 'EL', [ 0 ] * 20 )
        super( D20Race, self ).__init__( name, session, 20, mods, feats )

class D20AbilityScore( D20Stat ):
    def __init__( self, name, number ):
        import math
        super( D20AbilityScore, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.mod = lambda: int( math.floor( ( int( self ) - 10 ) / 2 ) )

class D20Skill( D20Stat ):
    def __init__( self, name, number ):
        super( D20Skill, self ).__init__( name, number, aggregator=MaxAggregateModifier )

class D20Attribute( Attribute ):
    def __init__( self, name, number ):
        super( D20Attribute, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20Size( Continuum ):
    def __init__( self, magnitude ):
        super( D20Size, self ).__init__( magnitude, 'Size' )

class D20DamageRange( Continuum ):
    def __init__( self, magnitude, dieroll ):
        row = dict( [ ( dierow[ 4 ], rownum ) for rownum, dierow in enumerate( D20DamageRange.rankTable ) ] )[ dieroll ]
        ranks = dict( zip( range( -4, 5 ), self.rankTable[ row ] ) )
        super( D20DamageRange, self ).__init__( magnitude, 'Size', 
                                            ranks=ranks )
        from dice import Roller
        self.roller = Roller( )

    def roll( self ):
        return sum( self.roller.roll( self.ranks[ super( D20DamageRange, self ).__int__( ) ] ) )

    rankTable=[
[ '0',        '0',    '0',    '1',    '1d2',    '1d3',    '1d4',    '1d6',    '1d8' ],
[ '0',        '0',    '1',    '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6' ],
[ '0',        '1',    '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6',    '3d6' ],
[ '1',        '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6',    '3d6',    '4d6' ],
[ '1d2',    '1d3',    '1d4',    '1d6',    '2d4',    '2d6',    '3d6',    '4d6',    '6d6' ],
[ '1d2',    '1d3',    '1d4',    '1d6',    '1d8',    '2d6',    '3d6',    '4d6',    '6d6' ],
[ '1d3',    '1d4',    '1d6',    '1d8',    '1d10',    '2d8',    '3d8',    '4d8',    '6d8' ],
[ '1d4',    '1d6',    '1d8',    '1d10',    '1d12',    '3d6',    '4d6',    '6d6',    '8d6' ],
[ '1d4',    '1d6',    '1d8',    '1d10',    '2d6',    '3d6',    '4d6',    '6d6',    '8d6' ],
                ]

class D20Attribute( Attribute ):
    def __init__( self, name, number ):
        super( D20Attribute, self ).__init__( name, number, aggregator=MaxAggregateModifier )
        self.modifiers[ 'INNATE' ] = CappedAggregateModifier( 5, target=self )
        self.modifiers[ 'RANKS' ] = AggregateModifier( target=self )

class D20Damage( D20Stat ):
    def __init__( self, types, size=0, roll="1d8", range=None ):
        self.range = range or D20DamageRange( size, roll )
        self.types = types
        super( D20Damage, self ).__init__( 'Damage', 0, self.range.roll )
        self.mod.static = True

    def __str__( self ):
        return "%s + %s" % ( self.range, self.modifiers )

    #Properties
    def getNumber( self ):
        return int( self.range.roll( ) ) + super( D20Damage, self ).number
    number = property( fget=getNumber, fset=D20Attribute.number.fset, fdel=D20Attribute.number.fdel )

class D20CritRange( D20Attribute ):
    def __init__( self, rng ):
        super( D20Attribute, self ).__init__( 'Critical Hit Threat Range', len( range( rng[ 0 ], rng[ 1 ] + 1 ) ) )

    def __iter__( self ):
        return iter( range( 20, 0, -1 )[ :int( self ) ] )

    def __contains__( self, val ):
        return val in range( 20, 0, -1 )[ :int( self ) ]

    def __str__( self ):
        first = range( 1, 21 )[ -int( self ) ]
        return "%s%s" % ( first, first != 20 and "-20" or "" )

class D20Weapon( EquippedItem ):
    def __init__( self, damageroll, types, *args, **kwargs ):
        self.roll = damageroll
        super( D20Weapon, self ).__init__( *args, **kwargs )
        self.DAMAGE = D20Damage( damageroll, range=self.SIZE )
        self.TYPES = types

    def __str__( self ):
        return "%s %s %s" % ( self.name, self.TYPES, self.SIZE )

    def ready( self, character ):
        character.BAB.mod.addTarget( self.ATT, '' )
        self.getAtt( character ).addTarget( self.ATT, 'ABILITY' )
        self.getDmg( character ).addTarget( self.DAMAGE, 'ABILITY' )

    def unready( self, character ):
        character.BAB.mod.removeTarget( self.ATT )
        self.getAtt( character ).removeTarget( self.ATT )
        self.getDmg( character ).removeTarget( self.DAMAGE )

    def getAtt( self, character ):
        return character.STR.mod

    def getDmg( self, character ):
        return character.STR.mod

    def setSize( self, tag, name, letter, modsprovided=None ):
        try:
            self.attrs[ tag ].letter = letter
        except:
            self.attrs[ tag ] = D20DamageRange( letter, self.roll )

    def setAttribute( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20Attribute( name, number )

    def setCritRange( self, tag, name, number ):
        self.attrs[ tag ] = D20CritRange( number )

    attTypes =    { 
                    'SIZE' : ( setSize, 'Size Category', ( ), 0 ),
                    'CRIT_RANGE' : ( setCritRange, 'Critical Hit Threat Range', ( ), (19,20) ),
                    'CRIT_MULT' : ( setAttribute, 'Critical Hit Multiplier', ( ), 2 ),
                    'ATT' : ( setAttribute, 'Attack Bonus', ( ), -4 ),
                }

class D20RangedWeapon( D20Weapon ):
    def getAtt( self, character ):
        return character.DEX.mod

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
            self.dmg = self.getDamage( )
            if self.rolls[ 0 ] in self.tool.CRIT_RANGE and self.isACrit( croll ):
                self.dmg = MultipliedModifier( crit.dmg, self.subject.weapon.CRIT_MULT )
            self.object.effects.append( self.dmg )
            self.dmg.enable( )
        return self.dmg

    def isAHit( self, roll=None ):
        if roll:
            self.rolls.append( roll )
        if not self.rolls:
            from dice import Roller
            roller = Roller( )
            self.rolls.extend( roller.roll( "1d20" ) )
        #This will need to be fixed for situations where the att or AC changes based on the defender or attacker
        return ( self.rolls[ 0 ] != 1 ) and ( ( self.rolls[ 0 ] + self.tool.ATT ) > self.object.AC or ( self.rolls[ 0 ] ) == 20 )

    def isACrit( self, croll=None ):
        if croll:
            self.rolls.append( croll )
        if len( self.rolls ) < 2:
            from dice import Roller
            roller = Roller( )
            self.rolls.extend( roller.roll( "1d20" ) )
        #This will need to be fixed for situations where the att or AC changes based on the defender or attacker
        return ( self.rolls[ 1 ] != 1 ) and ( ( self.rolls[ 1 ] + self.tool.ATT ) > self.object.AC or ( self.rolls[ 1 ] ) == 20 )

    def getDamage( self, mods=None ):
        dmg = self.getEffect( self.object, mods )
        dmg.factories[ self.object.WOUNDS ] = ( self.subject.weapon.DAMAGE.mod, 'DAMAGE', Conditions.compileCondition( ( ) ) )
        return dmg

    def __str__( self ):
        return "%s is doing something with %s using a(n) %s" % ( self.subject, self.object, self.tool )

class D20Character( Character ):
    def __init__( self, name, race, attrs=None ):
        super( D20Character, self ).__init__( name, attrs )
        self.levels = LevelBox( )
        self.race = race
        self.FEATS = { }
        self.unarmed = D20Weapon( '1d3', [ 'MELEE', 'UNARMED', 'CORPORIAL' ], 'Unarmed', 0, { 'SIZE':0 , 'WEIGHT': 0 }, 'A barroom tradition', { } )
        self.grapple = D20Weapon( '1d8', [ 'MELEE', 'GRAPPLE', 'CORPORIAL' ], 'Grappling', 0, { 'SIZE':0, 'WEIGHT': 0 }, 'A barroom tradition', { } )
        self.weapon = None

    def addLevel( self, characterclass ):
        try:
            numlevels = int( self.levels[ characterclass.name ] )
        except KeyError:
            numlevels = 0
        classlevel = characterclass.getLevel( self, numlevels )
        racelevel = self.race.getLevel( self, numlevels, characterclass )
        self.levels.addLevel( classlevel )
        self.levels.addLevel( racelevel )
        classlevel.enable( )
        racelevel.enable( )

    def beginCombat( self ):
        self.DEX.mod.addTarget( self.AC, 'ATTRIBUTE', Conditions( ( ), "and" ) )

    def endCombat( self ):
        self.DEX.mod.removeTarget( self.AC )

    def attack( self, foe, weapon=None ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        if weapon:
            self.unreadyWeapon( )
            self.readyWeapon( weapon )
        weapon = self.weapon
        return D20Attack( None, self, foe )

    def readyWeapon( self, weapon ):
        weapon.ready( self )
        self.weapon = weapon

    def unreadyWeapon( self ):
        #This will need fixing.  It's just for testing purposes.  FIXME
        try:
            try:
                self.weapon.unready( self )
            except TypeError:
                pass
            if self.weapon != self.unarmed:
                self.readyWeapon( self.unarmed )
            else:
                self.weapon = None
        except AttributeError:
            pass

    #Properties
    def setAbilityScore( self, tag, name, number, modsprovided=None ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20AbilityScore( name, number )

    def setAttribute( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20Attribute( name, number )

    def setStat( self, tag, name, number ):
        try:
            self.attrs[ tag ].number = number
        except:
            self.attrs[ tag ] = D20Stat( name, number )

    def setSize( self, tag, name, letter, modsprovided=None ):
        try:
            self.attrs[ tag ].letter = letter
        except:
            self.attrs[ tag ] = D20Size( letter )

    def getATT( self ):
        try:
            return self.weapon.ATT
        except AttributeError:
            return self.BAB
    ATT = property( fget=getATT, doc="This character's Attack bonus" )

    def getLevel( self ):
        charlevelnum = 1
        try:
            for level in self.levels[ 'RACE' ].values( ):
                if level.enabled:
                    charlevelnum += 1
        except KeyError:
            pass
        return charlevelnum
    level = property( fget=getLevel, doc="This character's level" )

    attTypes = { 
                #Basic Attributes
                'STR' : ( setAbilityScore, 'Strength', ( ), 0 ),
                'DEX' : ( setAbilityScore, 'Dexterity', ( ), 0 ),
                'CON' : ( setAbilityScore, 'Constitution', ( ), 0 ),
                'INT' : ( setAbilityScore, 'Intelligence', ( ), 0 ),
                'WIS' : ( setAbilityScore, 'Wisdom', ( ), 0 ),
                'CHA' : ( setAbilityScore, 'Charisma', ( ), 0 ),
                #END Basic Attributes

                #Calculated Attributes
                'AC' : ( setAttribute, 'Armor Class', 
                    (
                        ( 'SIZE', '-1 SIZE', ( ) ),
                    ), 10 ),
                'BAB' : ( setStat, 'Base Attack Bonus', ( ), 0 ),
                'WILL' : ( setAttribute, 'Will Save', 
                    (
                        ( 'ABILITY', 'WIS', ( ) ),
                    ), 0 ),
                'FORT' : ( setAttribute, 'Fortitude Save', 
                    (
                        ( 'ABILITY', 'CON', ( ) ),
                    ), 0 ),
                'REF' : ( setAttribute, 'Reflex Save', 
                    (
                        ( 'ABILITY', 'DEX', ( ) ),
                    ), 0 ),
                'INIT' : ( setAttribute, 'Initiative', ( ), 0 ),
                'EL' : ( setAttribute, 'Effective Level', ( ), 0 ),
                'HP' : ( setAttribute, 'Hit Points', ( ), 0 ),
                'WOUNDS' : ( setAttribute, 'Wounds', ( ), 0 ),
                'SPEED' : ( setAttribute, 'Movement Speed', ( ), 30 ),
                'SIZE' : ( setSize, 'Size Category', ( ), 'M' )
                }

if __name__ == "__main__":
    sword = D20Weapon( '1d8', [ 'MELEE', 'SLASHING', 'PIERCING', 'CORPORIAL' ], 'Longsword', 15, { 'WEIGHT':4, 'HEIGHT':18, 'WIDTH':4, 'DEPTH':2, 'SIZE':0 }, 'A sturdy longsword', { } )
    bow = D20RangedWeapon( '1d10', [ 'RANGE', 'PIERCING', 'CORPORIAL' ], 'Heavy Cross Bow', 50, { 'WEIGHT':8, 'HEIGHT':12, 'WIDTH':30, 'DEPTH':6, 'SIZE':0 }, 'A heavy crossbow', { } )
    race = D20Race( 'Elf', None, 
                {
                    'DEX': [ 2 ] + [ 0 ] * 19,
                    'CON': [ -2 ] + [ 0 ] * 19
                }, { } )
    bob = D20Character( "Bob", race, { 'STR': 13, 'DEX':15, 'CON':12, 'INT':10, 'WIS':8, 'CHA':18, 'HEIGHT':72, 'WEIGHT':221, 'WIDTH':24, 'DEPTH':12 } )
    charclass = D20CharacterClass( 'Fighter', None, 20, [ "10" ] * 20,
                { 
                    'BAB': [ 1 ] * 20,
                    'FORT': ( [ 2 ] + [ 1, 0 ] * 10 )[ :20 ],
                    'WILL': ( [ 0, 0, 1 ] * 7 )[ :20 ],
                    'REF': ( [ 0, 0, 1 ] * 7 )[ :20 ]
                }, { } )
    print int( bob.levels )
    bob.addLevel( charclass )
    print bob.levels
    print bob.ATT
    bob.addLevel( charclass )
    print bob.levels
    print bob.ATT
    print "AC before Dex mod"
    print bob.AC
    bob.beginCombat( )
    print "After"
    print bob.AC
    print "ATT before weapon"
    print int( bob.ATT )
    bob.readyWeapon( sword )
    att = bob.attack( bob )
    dmg = att.resolve( 18 )
    bob.attack( bob, sword )
    print "After Sword"
    print int( bob.ATT )
    print "Sword Removed"
    print int( bob.ATT )
    bob.attack( bob, bow )
    print "With Bow"
    print bob.ATT
    strstone = Item( 'Strength Stone', 0, { 'WEIGHT':5, 'HEIGHT':6, 'WIDTH':6, 'DEPTH':6 }, 'A plain round stone', { 'CARRIER' : { 'STR' : ( 2, '' ) } } )
    strstone2 = Item( 'Strength Stone2', 0, { 'WEIGHT':5, 'HEIGHT':6, 'WIDTH':6, 'DEPTH':6 }, 'A plain round stone', { 'CARRIER' : { 'STR' : ( 5, '' ) } } )
    print "Sword + Strength Stone"
    bob.attack( bob, sword )
    bob.carry( strstone )
    print bob.ATT
    print "Sword + Strength Stone + Strength Stone 2"
    bob.attack( bob, sword )
    bob.carry( strstone2 )
    print bob.ATT
    bob.attack( bob, bob.grapple )
    print "Grappling"
    print int( bob.ATT )
    print bob.WILL
    print bob.FORT
    print bob.REF
