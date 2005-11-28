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
<node BACKGROUND_COLOR="#99f433" COLOR="#00b439" CREATED="1128197081309" FOLDED="true" ID="Freemind_Link_1437433781" MODIFIED="1128207643811" TEXT="less indirection/duplication in Draggable event handlers in view">
<edge COLOR="#808080" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#990000" CREATED="1128197128137" ID="Freemind_Link_1208360324" MODIFIED="1128207636326" TEXT="indirection">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_cancel"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>new_Note and new_Icon call igroup.connect(&apos;event&apos;, event_disambiguator)&#xa;then event_disambiguator calls the real event handler&#xa;should be able to attach igroups directly to real event handlers</text>
</hook>
</node>
<node COLOR="#990000" CREATED="1128197138231" ID="Freemind_Link_378704758" MODIFIED="1128207633232" TEXT="duplication">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1128197497262" ID="Freemind_Link_84256301" MODIFIED="1128198821881" TEXT="on_foo_button_press, _motion, and _release are duplicated">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128197508684" ID="Freemind_Link_351555280" MODIFIED="1128198821881" TEXT="on_foo_event are identical for Draggables">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128198875161" ID="Freemind_Link_1063386291" MODIFIED="1128204980439" TEXT="drop_Note,Icon are the same">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128197419872" ID="Freemind_Link_1622294215" MODIFIED="1128207626982" TEXT="new_Note,Icon both clean up widget first">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128197442778" ID="Freemind_Link_864057045" MODIFIED="1128207630795" TEXT="both assign an igroup to widget">
<icon BUILTIN="button_cancel"/>
</node>
</node>
</node>
<node COLOR="#00b439" CREATED="1128203876286" ID="Freemind_Link_41198604" MODIFIED="1128463169708" TEXT="connectors">
<font NAME="SansSerif" SIZE="16"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>items which connect or apply to draggables should observe several properties.&#xa;* when draggable endpoints move, targetting arrow should update itself&#xa;* when either endpoint is Drop&apos;d, targetting arrow should disappear&#xa;</text>
</hook>
<node COLOR="#990000" CREATED="1128203907938" ID="Freemind_Link_1211805780" MODIFIED="1128203908390" TEXT="(e.g. targetting arrows) ">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1128237360966" ID="Freemind_Link_204437201" MODIFIED="1128237365337" TEXT="moving endpoint problem">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1128204099724" FOLDED="true" ID="Freemind_Link_50547549" MODIFIED="1128463327652" TEXT="connectors are observers">
<font NAME="SansSerif" SIZE="12"/>
<icon BUILTIN="full-1"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>if model in self.endpoints:&#xa;  self.do_appropriate_thing()&#xa;</text>
</hook>
<node COLOR="#111111" CREATED="1128237255803" ID="Freemind_Link_752862997" MODIFIED="1128237280290" TEXT="registered with box by main view (gui)"/>
<node COLOR="#111111" CREATED="1128237292627" ID="Freemind_Link_554445752" MODIFIED="1128237299808" TEXT="observer impl">
<node COLOR="#111111" CREATED="1128237304902" ID="Freemind_Link_113589197" MODIFIED="1128237323969" TEXT="watch for location changes of endpoints"/>
<node COLOR="#111111" CREATED="1128237324219" ID="Freemind_Link_586375096" MODIFIED="1128237330713" TEXT="when change happens, redraw arrow"/>
</node>
</node>
<node COLOR="#111111" CREATED="1128237080404" ID="Freemind_Link_1865347952" MODIFIED="1128463332543" TEXT="arrows grow location1, location2 properties">
<icon BUILTIN="full-2"/>
<node COLOR="#111111" CREATED="1128237120795" FOLDED="true" ID="Freemind_Link_493162952" MODIFIED="1128237130920" TEXT="these are dispatched">
<node COLOR="#111111" CREATED="1128556881546" ID="Freemind_Link_1694457481" MODIFIED="1128556894828" TEXT="BigController should handle and draw"/>
</node>
<node COLOR="#111111" CREATED="1128237131185" ID="Freemind_Link_1816095871" MODIFIED="1128463375856" TEXT="but not sent on the wire">
<icon BUILTIN="messagebox_warning"/>
<node COLOR="#111111" CREATED="1128463403013" ID="Freemind_Link_1580374356" MODIFIED="1128463418420" TEXT="or serialized when realm is saving"/>
<node COLOR="#111111" CREATED="1128463465077" ID="Freemind_Link_1865021823" MODIFIED="1128468041506" TEXT="dictify should filter">
<icon BUILTIN="help"/>
</node>
<node COLOR="#111111" CREATED="1128463468218" ID="Freemind_Link_1450062831" MODIFIED="1128463490703" TEXT="NetClient&apos;s receivePropertyChange &#xa;should filter"/>
</node>
<node COLOR="#111111" CREATED="1128237213869" ID="Freemind_Link_1696058820" MODIFIED="1128237759787" TEXT="connectors still need to be observers">
<node COLOR="#111111" CREATED="1128237224711" ID="Freemind_Link_1795355017" MODIFIED="1128237228823" TEXT="but observer impl is simpler"/>
<node COLOR="#111111" CREATED="1128237762286" ID="Freemind_Link_948841522" MODIFIED="1128237772300" TEXT="no redrawing (View does it)"/>
</node>
<node COLOR="#111111" CREATED="1129000367467" ID="Freemind_Link_1703388560" MODIFIED="1129005171651" TEXT="Implementation">
<font BOLD="true" NAME="SansSerif" SIZE="12"/>
</node>
</node>
<node COLOR="#111111" CREATED="1128234337416" FOLDED="true" ID="Freemind_Link_1166119285" MODIFIED="1128463334230" TEXT="View handles all this explicitly.. how &#xa;many such persistent connections will there be?">
<icon BUILTIN="button_cancel"/>
<icon BUILTIN="full-3"/>
<node COLOR="#111111" CREATED="1128234491894" ID="Freemind_Link_108718011" MODIFIED="1128234498365" TEXT="endpoints">
<node COLOR="#111111" CREATED="1128234607221" ID="Freemind_Link_730498447" MODIFIED="1128234609957" TEXT="Character"/>
<node COLOR="#111111" CREATED="1128234610472" ID="Freemind_Link_671022185" MODIFIED="1128234611957" TEXT="Drawing"/>
<node COLOR="#111111" CREATED="1128234613457" ID="Freemind_Link_812860250" MODIFIED="1128235563175" TEXT="Article"/>
</node>
<node COLOR="#111111" CREATED="1128234498787" ID="Freemind_Link_267057371" MODIFIED="1128234506429" TEXT="connectors">
<node COLOR="#111111" CREATED="1128235565895" ID="Freemind_Link_1702916802" MODIFIED="1128235567380" TEXT="TargetArrow"/>
<node COLOR="#111111" CREATED="1128235567661" ID="Freemind_Link_254134498" MODIFIED="1128235570130" TEXT="FollowArrow"/>
<node COLOR="#111111" CREATED="1128235570630" ID="Freemind_Link_1916412251" MODIFIED="1128235610500" TEXT="Drawing">
<hook NAME="accessories/plugins/NodeNote.properties">
<text>attached to a character or article as an effect</text>
</hook>
</node>
</node>
<node COLOR="#111111" CREATED="1128234507039" ID="Freemind_Link_1717961733" MODIFIED="1128234510274" TEXT="views">
<node COLOR="#111111" CREATED="1128234513556" ID="Freemind_Link_1920825558" MODIFIED="1128234543064" TEXT="NetClient does *not* have to update"/>
<node COLOR="#111111" CREATED="1128234544142" ID="Freemind_Link_322878224" MODIFIED="1128234562257" TEXT="BigView has to handle this"/>
<node COLOR="#111111" CREATED="1128234549191" ID="Freemind_Link_1091466922" MODIFIED="1128234564710" TEXT="mini map has to handle this"/>
<node COLOR="#111111" CREATED="1128234552488" ID="Freemind_Link_565945491" MODIFIED="1128234568289" TEXT="web map? has to handle this"/>
<node COLOR="#111111" CREATED="1128234555755" ID="Freemind_Link_885061303" MODIFIED="1128234556349" TEXT="etc."/>
</node>
<node COLOR="#111111" CREATED="1128236980378" ID="Freemind_Link_374940306" MODIFIED="1128236985754" TEXT="answer: TOO MANY"/>
</node>
</node>
<node COLOR="#990000" CREATED="1128237376342" ID="Freemind_Link_1036012661" MODIFIED="1128237381806" TEXT="resolving ids-to-models">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1128237383148" ID="Freemind_Link_1368215985" MODIFIED="1128237401209" TEXT="maybe box can take over remote_models list"/>
<node COLOR="#111111" CREATED="1128237596386" ID="Freemind_Link_1941201929" MODIFIED="1128237636854" TEXT="unmarshal() should resolve id&apos;s to models before returning model"/>
</node>
<node COLOR="#990000" CREATED="1128237486114" ID="Freemind_Link_334475158" MODIFIED="1128237541110" TEXT="connector-before-endpoint problem">
<font NAME="SansSerif" SIZE="14"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>if connector is Add&apos;d before endpoints, it will point to nothing&#xa;how do we make sure the endpoints are always built before connectors that refer to them?</text>
</hook>
</node>
</node>
<node COLOR="#00b439" CREATED="1128463170771" ID="Freemind_Link_720219263" MODIFIED="1128463220758" TEXT="why do objects stay &quot;grabbed&quot;?">
<font NAME="SansSerif" SIZE="16"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>newly added objects, or existing objects after an object &#xa;is right-click deleted, stay &quot;grabbed&quot; and move whenever&#xa;the mouse moves over them, even if the left button is not &#xa;down.  Why?&#xa;</text>
</hook>
</node>
<node COLOR="#00b439" CREATED="1128234904565" FOLDED="true" ID="Freemind_Link_1804626329" MODIFIED="1128234918756" TEXT="use inkscape to draw all visual items and effects needed">
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1128234922554" ID="Freemind_Link_1404182787" MODIFIED="1128234928821" TEXT="e.g.">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1128234930697" ID="Freemind_Link_1196874548" MODIFIED="1128628638722" TEXT="characters/articles">
<node COLOR="#111111" CREATED="1128234933651" ID="Freemind_Link_1480838479" MODIFIED="1128311734078" TEXT="unselected">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128234932338" ID="Freemind_Link_595366443" MODIFIED="1128311735828" TEXT="selected">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128235074797" ID="Freemind_Link_1372054555" MODIFIED="1128311737281" TEXT="hidden">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128235215694" ID="Freemind_Link_754174322" MODIFIED="1128312317796" TEXT="hovered">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128364916921" ID="Freemind_Link_263740035" MODIFIED="1128364921671" TEXT="name overflow">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128628334911" ID="Freemind_Link_1192609125" MODIFIED="1128628351036" TEXT="damage bar"/>
<node COLOR="#111111" CREATED="1128628353911" ID="Freemind_Link_161201153" MODIFIED="1128628357411" TEXT="incapacitated state"/>
</node>
<node COLOR="#111111" CREATED="1128234959533" FOLDED="true" ID="Freemind_Link_1250292606" MODIFIED="1128314729953" TEXT="sound/note icons">
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1128234985805" ID="Freemind_Link_645412772" MODIFIED="1128314720140" TEXT="unselected">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128364908453" ID="Freemind_Link_1732673167" MODIFIED="1128364911296" TEXT="hovered">
<icon BUILTIN="button_ok"/>
</node>
</node>
<node COLOR="#111111" CREATED="1128234929572" FOLDED="true" ID="Freemind_Link_381959095" MODIFIED="1128316434359" TEXT="arrows">
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1128235187624" ID="Freemind_Link_647983405" MODIFIED="1128364940437" TEXT="different lengths">
<icon BUILTIN="button_ok"/>
</node>
</node>
<node COLOR="#111111" CREATED="1128234943982" ID="Freemind_Link_94196267" MODIFIED="1128318849953" TEXT="things being renamed">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128234963784" FOLDED="true" ID="Freemind_Link_459484708" MODIFIED="1128452336447" TEXT="background">
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1128365086937" ID="Freemind_Link_1248884844" MODIFIED="1128451974730" TEXT="with band select">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128365089718" ID="Freemind_Link_499572551" MODIFIED="1128451974730" TEXT="with laser pointer">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128365105593" ID="Freemind_Link_1102303489" MODIFIED="1128451974715" TEXT="icons at diff zoom levels">
<icon BUILTIN="button_ok"/>
<hook NAME="accessories/plugins/NodeNote.properties">
<text>1. Labels will be at least as wide as the icon&#xa;2. When icon is tiny, label will reach a minimum size at which it&apos;s still readable (8 pixels high?)&#xa;3. Icon will reach a minimum size of (16x16?) pixels&#xa;</text>
</hook>
</node>
<node COLOR="#111111" CREATED="1128234965331" ID="Freemind_Link_433970316" MODIFIED="1128451974715" TEXT="obscurement mask">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128234949108" ID="Freemind_Link_1438057582" MODIFIED="1128452336447" TEXT="drawings">
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1128235095271" ID="Freemind_Link_675517978" MODIFIED="1128367802578" TEXT="visible">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128235097819" ID="Freemind_Link_1979097768" MODIFIED="1128452336447" TEXT="hidden">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128367803453" ID="Freemind_Link_1792268976" MODIFIED="1128451974715" TEXT="with hover label">
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#111111" CREATED="1128235097819" ID="Freemind_Link_501790211" MODIFIED="1128235100023" TEXT="hidden"/>
</node>
</node>
<node COLOR="#111111" CREATED="1128234975928" FOLDED="true" ID="Freemind_Link_468307816" MODIFIED="1128452361228" TEXT="selecting tools">
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1128452356119" ID="Freemind_Link_1692009519" MODIFIED="1128452362228" TEXT="band select">
<icon BUILTIN="button_ok"/>
</node>
</node>
<node COLOR="#111111" CREATED="1128234967503" ID="Freemind_Link_917812682" MODIFIED="1128234969066" TEXT="drawing tools"/>
<node COLOR="#111111" CREATED="1128628662331" ID="Freemind_Link_1316182577" MODIFIED="1128628664612" TEXT="waypoints">
<node COLOR="#111111" CREATED="1128628665097" ID="Freemind_Link_627157237" MODIFIED="1128628670628" TEXT="normal (with distance marks)"/>
<node COLOR="#111111" CREATED="1128628671018" ID="Freemind_Link_559224877" MODIFIED="1128628675331" TEXT="planning mode"/>
</node>
<node COLOR="#111111" CREATED="1128235126076" ID="Freemind_Link_1877968407" MODIFIED="1128235138626" TEXT="window layout">
<node COLOR="#111111" CREATED="1128235139924" ID="Freemind_Link_660191209" MODIFIED="1128235143393" TEXT="where&apos;s minimap"/>
<node COLOR="#111111" CREATED="1128235143643" ID="Freemind_Link_543198804" MODIFIED="1128235147457" TEXT="where does chat go"/>
<node COLOR="#111111" CREATED="1128235147723" ID="Freemind_Link_1096385156" MODIFIED="1128235148848" TEXT="combat"/>
<node COLOR="#111111" CREATED="1128235149223" ID="Freemind_Link_1027405960" MODIFIED="1128235166056" TEXT="character stat popup"/>
</node>
<node COLOR="#111111" CREATED="1128235170901" ID="Freemind_Link_316612973" MODIFIED="1128235173386" TEXT="context menus"/>
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
<node COLOR="#990000" CREATED="1128147944290" ID="Freemind_Link_1209346866" MODIFIED="1128185460897" TEXT="strategy?">
<font NAME="SansSerif" SIZE="14"/>
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
