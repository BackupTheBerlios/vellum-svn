

// import Nevow.Athena
// import Divmod

WebbyVellum.AccountManager = Nevow.Athena.Widget.subclass('WebbyVellum.AccountManager');
WebbyVellum.AccountManager.methods(
    function onLogOnSubmit(self, node, event) {
        Divmod.debug("AccountManager", "logon clicked");
        host = node.host.value;
        username = node.username.value;
        password = node.password.value;
        channels = node.channels.value;
        self.callRemote("onLogOnSubmit", username, password, host, channels);
    }
);



WebbyVellum.ConversationWindow = Nevow.Athena.Widget.subclass('WebbyVellum.ConversationWindow');
WebbyVellum.ConversationWindow.methods(
    function showChatEvent(self, text) {
        self.node.innerHTML = self.node.innerHTML + text + "<br />";
    });

WebbyVellum.ChatEntry = Nevow.Athena.Widget.subclass('WebbyVellum.ChatEntry');
WebbyVellum.ChatEntry.methods(
    function checkEnter(self, node, event) {
        Divmod.debug("ChatEntry", event);
        if (event.keyCode == 13)
        {
            var input = Nevow.Athena.FirstNodeByAttribute(node,
                'class', 'chatentry')
            self.callRemote("chatMessage", input.value);
            input.value = "";
        }
        return false;
    }
);