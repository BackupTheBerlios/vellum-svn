from nevow import athena
from nevow.livetrial import testcase

from webby import tabs

class TestInitialArguments(testcase.TestCase):
    jsClass = u'Tabby.Tests.TestTabs'
    def newTabWidget(self, *a):
        """Return a new tab widget"""
        w = tabs.TabsFragment()
        w.setFragmentParent(self)
        w.setInitialArguments(*a)
        return w
    athena.expose(newTabWidget)

