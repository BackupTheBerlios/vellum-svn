<map version="0.8.0">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node COLOR="#000000" CREATED="1127245613704" ID="Freemind_Link_679227453" MODIFIED="1127425554119" TEXT="vellum todo">
<font NAME="SansSerif" SIZE="20"/>
<hook NAME="accessories/plugins/AutomaticLayout.properties"/>
<node COLOR="#0033ff" CREATED="1127245613704" ID="Freemind_Link_991957294" MODIFIED="1127425554041" POSITION="right" TEXT="fixes" VSHIFT="1">
<font NAME="SansSerif" SIZE="18"/>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_379815202" MODIFIED="1127425746435" TEXT="pydispatcher raises exception when Icon is gc&apos;d" VSHIFT="84">
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_1431028816" MODIFIED="1127425688353" TEXT="probably caused by a signal connected to itself">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_132797881" MODIFIED="1127425688353" TEXT="e.g. Modelable.__init__">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1127425267847" ID="Freemind_Link_197885427" MODIFIED="1127425696380" TEXT="replace Modelable method with lambda">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>I was using a method as the receiver of the signal.&#xa;Switched to using a lambda as an instance attribute &#xa;instead of a method (semantically, the same thing) and &#xa;the error went away.  I must conclude this is a subtle &#xa;pydispatcher bug, but not a serious one.</text>
</hook>
</node>
</node>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_994932207" MODIFIED="1127493606969" TEXT="add or remove icon" VSHIFT="19">
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_1582524538" MODIFIED="1127425554041" TEXT="right-clicks">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1127253716526" ID="_" MODIFIED="1127425554041" TEXT="add">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1127253718167" FOLDED="true" ID="Freemind_Link_1833411601" MODIFIED="1127436463526" TEXT="delete">
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1127425763130" ID="Freemind_Link_1284650284" MODIFIED="1127436463526" TEXT="stop canvas from grabbing mouse events">
<icon BUILTIN="button_ok"/>
</node>
</node>
</node>
</node>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_1248932810" MODIFIED="1127634247546" TEXT="use FilePasswordDB">
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127634188593" ID="Freemind_Link_1659193584" MODIFIED="1127634205000" TEXT="pb forces you to use this without a hash function">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_523415266" MODIFIED="1127676203390" TEXT="same username can login mult times w/o reusing avatar">
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_1698448917" MODIFIED="1127425554072" TEXT="&amp; superseded clones don&apos;t get events">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_791738793" MODIFIED="1127676183468" TEXT="original should dc on new connect">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_1855730006" MODIFIED="1127841897399" TEXT="models and uuids maintained independently on both sides">
<edge COLOR="#808080" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_688785933" MODIFIED="1127425554041" TEXT="should be one object to connect them, managed with a single call">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_1718961835" MODIFIED="1127841833383" TEXT="BiDict object implemented">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_1535484102" MODIFIED="1127859555652" TEXT="avatar initializer gets instance of realm">
<edge COLOR="#808080" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_116261161" MODIFIED="1127425554057" TEXT="only uses models, uuids, addModel">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_122606526" MODIFIED="1127859537733" TEXT="see BiDict object idea above">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_88553917" MODIFIED="1127865699812" TEXT="getInitialIcon -&gt; getGameState">
<edge COLOR="#808080" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_1249335940" MODIFIED="1127865662103" TEXT="return flattened hierarchy">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_1440282367" MODIFIED="1127865684897" TEXT="Modelables should implement marshal">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_522354774" MODIFIED="1128145703634" TEXT="object hierarchy for complex schema">
<edge COLOR="#808080" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_1416087954" MODIFIED="1127950445834" TEXT="e.g. Background, Icon, Note">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_806787178" MODIFIED="1127950445974" TEXT="should be flat">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_362401918" MODIFIED="1127950499521" TEXT="grouping object to facilitate flatness?">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1127950450037" ID="Freemind_Link_768350362" MODIFIED="1127950493489" TEXT="Map"/>
</node>
<node COLOR="#990000" CREATED="1127950548052" ID="Freemind_Link_1061997285" MODIFIED="1128145694133" TEXT="test passing hierarchy over wire">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_1125614771" MODIFIED="1128145733124" TEXT="new netclient / avatar marshalling">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1127245613704" ID="Freemind_Link_328539926" MODIFIED="1128145733124" TEXT="class Gameboy">
<font NAME="SansSerif" SIZE="12"/>
<icon BUILTIN="button_ok"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>class GameBoy:&#xa;  def perspective_getGameState()&#xa;    ret = []&#xa;    m = self.realm.models&#xa;    for id, model in m.items():&#xa;      ret.append((id, model.marshal())&#xa;    return ret</text>
</hook>
</node>
<node COLOR="#111111" CREATED="1127426087586" FOLDED="true" ID="Freemind_Link_1035492751" MODIFIED="1128145733124" TEXT="class NetClient">
<font NAME="SansSerif" SIZE="12"/>
<icon BUILTIN="button_ok"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>class NetClient:&#xa;  def gotGame(self, data):&#xa;    for id, string in data:&#xa;      dct = yaml.fromString(string)&#xa;      cls = eval(dct[&apos;class&apos;])&#xa;      self.addModel(cls.fromDict(dct), id)&#xa;      dispatcher.send(signal=New, &quot;initial&quot;, model=model)&#xa;</text>
</hook>
<node COLOR="#111111" CREATED="1127245613704" ID="Freemind_Link_1789178076" MODIFIED="1128145733124" TEXT="netclient.callRemote(&quot;getGameState&quot;).addCallback(self.gotGame)">
<font NAME="SansSerif" SIZE="12"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
</node>
</node>
<node COLOR="#00b439" CREATED="1127245613704" FOLDED="true" ID="Freemind_Link_1076507153" MODIFIED="1127425554072" TEXT="signals should be reified?">
<edge WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1127245613704" ID="Freemind_Link_1822322171" MODIFIED="1127425554072" TEXT="easy to send a signal with wrong args">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1127447009830" FOLDED="true" ID="Freemind_Link_704733548" MODIFIED="1127447028081" TEXT="easy to define a receiver with the wrong &#xa;args (it may even seem to work)">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1127447029815" ID="Freemind_Link_599156117" MODIFIED="1127447048582" TEXT="because dispatch analyzes the &#xa;receiver and omits some args"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1127447067286" FOLDED="true" ID="Freemind_Link_1612497864" MODIFIED="1128138796379" TEXT="duplicate functionality in avatar and client">
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_cancel"/>
<node COLOR="#990000" CREATED="1127447090366" ID="Freemind_Link_1604215725" MODIFIED="1127916466891" TEXT="2x3x remote_receiveFooSignal">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1127447101382" ID="Freemind_Link_1543832867" MODIFIED="1127916472495" TEXT="2x3x receiveFooSignal (from dispatch)">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
</node>
</node>
</map>
