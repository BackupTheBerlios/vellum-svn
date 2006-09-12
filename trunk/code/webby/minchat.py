"""Chat functionality"""

from twisted.words.im import basechat, baseaccount
from twisted.internet import defer, protocol, reactor

from twisted.words.im import ircsupport 

ACCOUNTS = {}

PROTOS = {}

IRCPORT = 6667

class AccountManager(baseaccount.AccountManager):
    """This class is a minimal implementation of the Acccount Manager.

    Most implementations will show some screen that lets the user add and
    remove accounts, but we're not quite that sophisticated.
    """

    def __init__(self, chatui):
        self.chatui = chatui

    def doConnection(self, host, username, password, channels):
        if username in ACCOUNTS and ACCOUNTS[username].isOnline():
            self.disconnect(ACCOUNTS[username])

        acct = ircsupport.IRCAccount("IRC", 1, username, password, host,
                IRCPORT, channels)
        ACCOUNTS[username] = acct
        dl = []
        for acct in ACCOUNTS.values():
            d = acct.logOn(self.chatui)
            def _addProto(proto, self, acct):
                PROTOS[acct.username] = proto
                return acct
            d.addCallback(_addProto, self, acct)
            dl.append(d)

        return defer.DeferredList(dl)
        
    def disconnect(self, username):
        PROTOS[username].transport.loseConnection()



class MinConversation(basechat.Conversation):
    """This class is a minimal implementation of the abstract Conversation class.

    This is all you need to override to receive one-on-one messages.
    """
    def __init__(self, widget, *a, **kw):
        basechat.Conversation.__init__(self, *a, **kw)
        self.webPrint = lambda m: widget.printclean(self.user.name, m) 

    def show(self):
        """If you don't have a GUI, this is a no-op.
        """
        if self.user.name in self.widget.conversations:
            self.widget.foregroundConversation = self
            self.widget.callRemote("show", unicode(self.user.name))
    
    def hide(self):
        """If you don't have a GUI, this is a no-op.
        """
    
    def showMessage(self, text, metadata=None):
        event = "<%s> %s" % (self.person.name, text)
        return self.webPrint(event)
        
    def contactChangedNick(self, person, newnick):
        basechat.Conversation.contactChangedNick(self, person, newnick)
        event = "-!- %s is now known as %s" % (person.name, newnick)
        return self.webPrint(event)


class MinGroupConversation(basechat.GroupConversation):
    """This class is a minimal implementation of the abstract
    GroupConversation class.

    This is all you need to override to listen in on a group conversation.
    """
    def __init__(self, widget, *a, **kw):
        basechat.GroupConversation.__init__(self, *a, **kw)
        self.widget = widget
        self.webPrint = lambda m: widget.printClean('#' + self.group.name, m)

    def show(self):
        """If you don't have a GUI, this is a no-op.
        """
        groupname = '#' + self.group.name
        if groupname in self.widget.conversations:
            self.widget.foregroundConversation = self
            self.widget.callRemote("show", unicode(groupname))

    def hide(self):
        """If you don't have a GUI, this is a no-op.
        """
        pass

    def showGroupMessage(self, sender, text, metadata=None):
        t = "<%s> %s" % (sender, text)
        return self.webPrint(t)

    def setTopic(self, topic, author):
        event = "-!- %s set the topic to: %s" % (author, topic)
        return self.webPrint(event)
                

    def memberJoined(self, member):
        basechat.GroupConversation.memberJoined(self, member)
        event = "-!- %s joined %s" % (member, self.group.name)
        return self.webPrint(event)

    def memberChangedNick(self, oldnick, newnick):
        basechat.GroupConversation.memberChangedNick(self, oldnick, newnick)
        event = "-!- %s is now known as %s in %s" % (oldnick, newnick,
            self.group.name)
        return self.webPrint(event)

    def memberLeft(self, member):
        basechat.GroupConversation.memberLeft(self, member)
        event = "-!- %s left %s" % (member, self.group.name)
        return self.webPrint(event)

class NoUIConnected(Exception):
    pass
    
class MinChat(basechat.ChatUI):
    """This class is a minimal implementation of the abstract ChatUI class.

    There are only two methods that need overriding - and of those two, 
    the only change that needs to be made is the default value of the Class
    parameter.
    """

    readyToChat = False

    def initUI(self, widget):
        self.readyToChat = True
        self.widget = widget
        self.groupClass = lambda *a, **kw: MinGroupConversation(widget, *a, **kw)
        self.convoClass = lambda *a, **kw: MinConversation(widget, *a, **kw)

    def getGroupConversation(self, group, Class=None, stayHidden=0):
        if not self.readyToChat:
            raise NoUIConnected()
        conv = basechat.ChatUI.getGroupConversation(self, group, self.groupClass, 
            stayHidden)
        return conv

    def getConversation(self, person, Class=None, stayHidden=0):
        if not self.readyToChat:
            raise NoUIConnected()
        conv = basechat.ChatUI.getConversation(self, person, self.convoClass, 
                stayHidden)
        return conv
