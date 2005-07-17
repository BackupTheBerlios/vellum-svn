from charmodel.generic.effect import CharacterLevel

class D20CharacterLevel( CharacterLevel ):
    def __init__( self, character, levelnum, charlevelnum, characterclass, mods=None, feats=None ):
        super( D20CharacterLevel, self ).__init__( character, levelnum, charlevelnum, characterclass, mods, feats )
        from dice import parse
        if charlevelnum == 1:
            rollstring = characterclass.hitdice[ levelnum ]
        else:
            rollstring = "1d%s" % characterclass.hitdice[ levelnum ]
        self.hp = D20HP( 'Hit Points', parse( rollstring ).sum( ) )
        character.CON.modprovided.addTarget( self.hp, 'RANKS' )
        self.factories[ character.HP ] = ( self.hp.modprovided, 'Level Modifier', ( ) )
