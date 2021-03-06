from twisted.python.util import sibpath
from twisted.python import components
from twisted.internet import defer

from zope.interface import implements

from nevow import rend, loaders, athena, url, static, inevow, \
                  tags as T, guard, page

from webby import minchat, svgmap, parseirc, stainedglass, util, signup, \
                  gmtools, tabs, theGlobal, data
from webby import iwebby, RESOURCE


class IRCContainer(stainedglass.Enclosure, components.Componentized):
    """
    Contains all the IRC components: AccountManager, ConversationTabs,
    ChatEntry.
    """ 
    jsClass = u"WebbyVellum.IRCContainer"

    def __init__(self, accountManager, user, *a, **kw):
        super(IRCContainer, self).__init__(
                windowTitle="IRC", userClass="irc", *a, **kw)
        components.Componentized.__init__(self)
        self.accountManager = accountManager
        self.user = user

    def enclosedRegion(self, request, tag):
        cw = ConversationTabs(self.user)
        cw.setFragmentParent(self)
        self.setComponent(iwebby.IChatConversations, cw)
        cw.initServerTab()

        am = AccountManager(self.accountManager, cw, self.user)
        am.setFragmentParent(self)
        self.setComponent(iwebby.IChatAccountManager, am)
        return tag[am, cw]

    athena.renderer(enclosedRegion)


class TopicBar(util.RenderWaitLiveElement):
    """
    Text widget that sits above the channel window in a tab and displays the
    current channel topic.
    """
    implements(iwebby.ITopicBar)
    docFactory = loaders.xmlfile(RESOURCE('elements/TopicBar'))
    jsClass = u'WebbyVellum.TopicBar'

    def setTopic(self, topic):
        topic = unicode(topic)
        return self.callRemote('setTopic', topic)


class NameSelect(util.RenderWaitLiveElement):
    """
    <select> box that contains the list of names for a group conversation.
    """
    implements(iwebby.INameSelect)
    jsClass = u'WebbyVellum.NameSelect'
    docFactory = loaders.xmlfile(RESOURCE('elements/NameSelect'))

    def addName(self, name, flags):
        # TODO - parse flags
        name = unicode(name)
        return self.callRemote('addName', name, None)

    def removeName(self, name):
        name = unicode(name)
        return self.callRemote('removeName', name)

    def setNames(self, names):
        # TODO - flags?
        return self.callRemote('setNames', map(unicode, names))

NODEFAULT = object()

class ControlBar(page.Element):
    docFactory = loaders.xmlfile(RESOURCE('elements/ControlBar'))


class ChannelLayout(page.Element):
    docFactory = loaders.xmlfile(RESOURCE('elements/ChannelLayout'))
    def __init__(self, controlBar, topicBar, mapDiv, channelDiv, chatEntry):
        self.controlBar = controlBar
        self.topicBar = topicBar
        self.mapDiv = mapDiv
        self.channelDiv = channelDiv
        self.chatEntry = chatEntry

    def layout(self, req, tag):
        tag.fillSlots('controlBar', self.controlBar)
        tag.fillSlots('topicBar', self.topicBar)
        tag.fillSlots('mapDiv', self.mapDiv)
        tag.fillSlots('channelDiv', self.channelDiv)
        tag.fillSlots('chatEntry', self.chatEntry)
        return tag

    page.renderer(layout)


class ConversationEnclosure(stainedglass.Enclosure):
    jsClass = u'WebbyVellum.ConversationEnclosure'
    def __init__(self, conversationName, *a, **kw):
        super(ConversationEnclosure, self).__init__(*a, **kw)
        self.conversationName = conversationName

    def getInitialArguments(self):
        return (self.conversationName,)

class ConversationTabs(tabs.TabsElement):
    """
    UI element - For each conversation, one tab.
    """
    ## jsClass = u"WebbyVellum.ConversationTabs"
    implements(iwebby.IChatConversations)

    def __init__(self, user, *a, **kw):
        super(ConversationTabs, self).__init__(*a, **kw)
        self.conversations = {}
        self.user = user

    def _joinConversation(self, conversationName, conversation):
        self.conversations[conversationName] = conversation
        if hasattr(conversation, 'group'):
            self.user.addRecentChannel(conversationName)

    def _partConversation(self, conversationName):
        del self.conversations[conversationName]
        self.user.removeRecentChannel(conversationName)

    def getConversation(self, id, default=NODEFAULT):
        """
        Get the IRC conversation object by the tab id
        """
        if default is NODEFAULT:
            return self.conversations[id]
        else:
            return self.conversations.get(id, default)
    
    def initServerTab(self):
        """
        Boilerplate for setting up an IRC tabs widget.

        This creates the server tab and null server conversation,
        connects them together, and sets up things so all of that will be sent
        together in the first render.
        """
        initialId = u'**SERVER**'

        nullconv = minchat.NullConversation(self.fragmentParent, initialId)

        # create a textarea around the conversation
        ta = stainedglass.TextArea()
        ta.setFragmentParent(self)
        ta.setInitialArguments(GREETING)

        nullconv.setComponent(iwebby.ITextArea, ta)

        self.conversations[initialId] = nullconv

        super(ConversationTabs, self).addInitialTab(initialId, initialId, ta)

    def showConversation(self, conversation, conversationName):
        """
        Bring a conversation to the foreground.

        This is called whenever someone says something in that conversation.
        TODO: instead of bringing it to the foreground, display a 
        highlight marker when the conversation exists already.
        """
        cn = unicode(conversationName)
        if cn not in self.conversations:
            # create an Enclosure to hold the contents of the tab
            enc = ConversationEnclosure(
                    conversationName,
                    decorated=False)
            enc.setFragmentParent(self)

            # create a textarea around the conversation
            ta = stainedglass.TextArea()
            ta.setFragmentParent(enc)
            # assign components
            conversation.setComponent(iwebby.ITextArea, ta)

            # the thing you can type at
            ce = ChatEntry(conversation)
            ce.setFragmentParent(enc)
            
            if hasattr(conversation, 'group'):
                # the userClass for the enclosure should annotate the
                # contents
                enc.userClassStan = "gameTab"
                # create the corresponding names list
                ns = NameSelect()
                ns.setFragmentParent(enc)
                conversation.setComponent(iwebby.INameSelect, ns)

                # space for the topic
                tb = TopicBar()
                tb.setFragmentParent(enc)
                conversation.setComponent(iwebby.ITopicBar, tb)

                # the MAP
                db = theGlobal['database']
                channel = db.findFirst(data.Channel, data.Channel.name==cn)
                mapw = svgmap.MapWidget(channel, ce)
                mapw.setFragmentParent(enc)
                conversation.setComponent(iwebby.IMapWidget, mapw)
                # the buttons etc.
                controlBar = ControlBar()
                
                mapdiv = T.div(_class="mapbox")[mapw]
            else:
                ns = []
                tb = []
                controlBar = []
                mapdiv = []

            # put the little widgets into the stan tree of the container
            layout = ChannelLayout(controlBar, tb, mapdiv,
                    T.div(_class="channel")[ta, ns], ce)
            enc = enc[layout]

            d = self.addTab(cn, cn)

            def _added(ignored):
                return self.setTabBody(cn, enc)

            d.addCallback(_added)

            self._joinConversation(cn, conversation)
        else:
            d = defer.succeed(None)

        def _conversationIsReady(_):
            if hasattr(conversation, 'group'):
                acct = self.page.chatui.onlineClients[0].account
                acct.client.sendLine(('MAPDIGEST %s' % (cn,)).encode('utf8'))
            return self.callRemote("show", cn)

        d.addCallback(_conversationIsReady)

        def _conversationFailed(e):
            self._partConversation(cn)
            return e

        d.addErrback(_conversationFailed)

        return d

    def hideConversation(self, conversation, conversationName):
        """
        Make a conversation disappear.
        """
        cn = unicode(conversationName)
        if cn in self.conversations:
            d = self.removeTab(cn)
            self._partConversation(cn)
        else:
            d = defer.succeed(None)
        # FIXME - we do not return this deferred.  Need to see whether
        # minchat deals with deferreds returned by this stack


def webClean(st):
    return unicode(st.replace('<','&lt;').replace('>','&gt;'))

GREETING = util.flattenMessageString(
u'''Vellum IRC v0.1
Click "Join!" to connect.''')


class AccountManager(athena.LiveElement):
    """
    UI element that handles changing of the nick and processing a login to the
    IRC server.
    """
    jsClass = u"WebbyVellum.AccountManager"
    docFactory = loaders.xmlfile(RESOURCE('elements/AccountManager'))
    implements(iwebby.IChatAccountManager)

    def __init__(self, accountManager, conversationTabs, user, *a, **kw):
        super(AccountManager, self).__init__(*a, **kw)
        self.accountManager = accountManager
        self.conversationTabs = conversationTabs
        self.user = user

    def getInitialArguments(self):
        nick = self.user.nick
        channels = self.user.recentChannels
        if nick and channels:
            # when both nick and channels are already set, log the irc user
            # straight in.
            self.onLogOnSubmit(nick, channels)
            # set autoHide = True on the widget because login will be
            # automatic
            return (nick, channels, True)
        return (nick, channels)

    def onLogOnSubmit(self, nick, channels):
        """
        Process by looking up the password for that nick and starting
        a login process on the IRC protocol.
        """
        host = 'localhost'.encode('utf8')
        password = self.user.password.encode('utf8')
        username = nick.encode('utf8')

        # SET the permanent nick to the nick we were provided, trust it.
        # We can trust the nick because use of AccountManager 
        # implies that the user is *already* authenticated, through
        # the web.  Users visiting using a regular IRC client will 
        # naturally have to supply their passwords the normal way.
        self.user.nick = unicode(nick)

        channels = channels.encode('utf8')
        d = self.accountManager.doConnection(host, username, password, channels)

        def _gotAccount(acct):
            # set up disconnection callback for browser close etc.
            def logOff(_ignored, acct):
                self.accountManager.disconnectAsNeeded(acct)
            self.page.notifyOnDisconnect().addBoth(logOff, acct)

            return u'connected %s@%s and joined %s' % (username, host, channels)

        d.addCallback(_gotAccount)
        return d
    athena.expose(onLogOnSubmit)


class ChatEntry(athena.LiveElement):
    docFactory = loaders.xmlfile(RESOURCE('elements/ChatEntry'))
    jsClass = u"WebbyVellum.ChatEntry"

    def __init__(self, conversation, *a, **kw):
        super(ChatEntry, self).__init__(*a, **kw)
        self.conversation = conversation

    def chatMessage(self, message):
        conv = self.conversation

        parsed = parseirc.line.parseString(message)
        if parsed.command:

            def irccmdFallback(message, conv):
                strCommand = parsed.commandWord.encode('utf8').upper()
                message = '%s %s' % (strCommand, message)
                return self.irccmd_raw(message, conv)
                
            m = getattr(self, 
                        'irccmd_%s' % (parsed.commandWord,),
                        irccmdFallback)
            m(parsed.commandArgs.encode('utf8'), conv)
        else:
            self.say(parsed.nonCommand[0].encode('utf8'), conv)

        return u'ok'

    athena.expose(chatMessage)

    def say(self, message, conv):
        return conv.sendText(message)

    def irccmd_me(self, args, conv):
        return conv.sendText(args, metadata={'style':'emote'})

    def irccmd_join(self, args, conv):
        groups = args.split()

        ## acct = conv.group.account
        # We're using this way to get the account because I can't figure out a
        # way to make it so all conversations have access to the account.  I
        # don't know if this will work.  FIXME
        acct = self.page.chatui.onlineClients[0].account

        if groups:
            args = args[len(groups[0])-1:].lstrip()
            groups = groups[0].split(',')

        acct.joinGroups(groups)

    irccmd_j = irccmd_join

    def irccmd_topic(self, args, conv):
        client = self.page.chatui.onlineClients[0]

        channel = None

        # see if the user is trying to see/set the topic for some other 
        # channel.  This applies if the first word begins with a hash #.
        if args.strip() != '':
            firstArg = args.split()[0]
            if firstArg[0] == '#':
                # remove the channel.
                args = args[len(firstArg):]
                args = args.lstrip()
                channel = firstArg

        if channel is None:
            if hasattr(conv, 'group'):
                channel = conv.group.name
            else:
                return conv.sendText("Cannot set or view topic of SERVER tab")

        channel = channel.lstrip('#')

        if args.strip() == '':
            args = None
        
        client.topic(channel, args)

    def irccmd_part(self, args, conv):
        groups = args.split()

        ## acct = conv.group.account
        # We're using this way to get the account because I can't figure out a
        # way to make it so all conversations have access to the account.  I
        # don't know if this will work.
        acct = self.page.chatui.onlineClients[0].account

        if groups:
            args = args[len(groups[0])-1:].lstrip()
            groups = groups[0].split(',')
        else:
            if hasattr(conv, 'group'):
                groups.append(conv.group.name.lstrip('#'))
            else:
                return conv.sendText("Cannot /part from SERVER tab")

        # TODO: Find out how to support parting messages
        acct.leaveGroups(groups)

    irccmd_leave = irccmd_part

    def irccmd_raw(self, args, conv):
        ## acct = conv.group.account
        # We're using this way to get the account because I can't figure out a
        # way to make it so all conversations have access to the account.  I
        # don't know if this will work.
        acct = self.page.chatui.onlineClients[0].account
        return acct.client.sendLine(args)

    def irccmd_notice(self, args, conv):
        client = self.page.chatui.onlineClients[0]
        recipient, rest = args.split(None, 1)
        r = client.notice(recipient, rest)
        iwebby.ITextArea(conv).printClean(u'>%s< %s' % (recipient, rest))
        return r

    def irccmd_query(self, args, conv):
        try:
            personName = args.split()[0]
            mesg = args[len(personName):].lstrip()
            chatui = self.page.chatui
            client = chatui.onlineClients[0]
            newConv = chatui.getConversation(chatui.getPerson(personName, client))
            newConv.show()
            if mesg:
                newConv.sendText(mesg)
        except:
                conv.sendText("Problems with /query, bailing out.")


class IRCPage(athena.LivePage):
    """
    Page container for the IRC UI and the maps UI
    """
    addSlash = True

    docFactory = loaders.xmlfile(RESOURCE('templates/webby.xhtml'))

    def renderHTTP(self, ctx):
        """Set XHTML as the mime type so SVG can be rendered."""
        req = inevow.IRequest(ctx)
        req.setHeader('content-type', 'application/xhtml+xml')
        return super(IRCPage, self).renderHTTP(ctx)

    def __init__(self, *a, **kw):
        super(IRCPage, self).__init__(*a, **kw)
        self.chatui = minchat.MinChat()

    def render_chat(self, ctx, _):
        accountManager = minchat.MinAccountManager(self.chatui)
        ss = inevow.ISession(ctx)
        irc = IRCContainer(accountManager, ss.user)
        irc.setFragmentParent(self)

        self.chatui.initUI(irc)

        return ctx.tag[irc]

    def render_gmtools(self, ctx, _):
        ss = inevow.ISession(ctx)
        gmt = gmtools.GMTools(ss.user)
        enc = stainedglass.Enclosure(windowTitle="GM Tools", 
                userClass="gmtools draggable")
        enc.setFragmentParent(self)
        gmt.setFragmentParent(enc)

        return ctx.tag[enc[gmt]]

    def render_topLinks(self, ctx, _):
        ss = inevow.ISession(ctx)
        ctx.tag.fillSlots('email', ss.user.email)
        ctx.tag.fillSlots('logoutHref', url.root.child(guard.LOGOUT_AVATAR))
        ctx.tag.fillSlots('adminLink', T.a['Admin (TODO)'])
        return ctx.tag
