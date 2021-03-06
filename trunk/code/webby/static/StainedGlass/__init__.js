// import Divmod
// import Nevow.Athena

RT = Divmod.Runtime.theRuntime;


/* fucking fucking javascript DOM -- this is the only goddamn way to get
   the absolute position of an element
 */
StainedGlass.getPosition = function _(node) { // {{{
	var left = 0;
	var top  = 0;

	while (node.offsetParent){
		left += node.offsetLeft;
		top  += node.offsetTop;
		node = node.offsetParent;
	}

	left += node.offsetLeft;
	top  += node.offsetTop;

	return {x:left, y:top};
} // }}}


/* abstract class that implements the state associated with a drag operation.
 * Call StainedGlass.draggable(
 */
StainedGlass.DragState = Divmod.Class.subclass('StainedGlass.DragState');
StainedGlass.DragState.methods( // {{{
    function _cleanupDragState(self) { // {{{
        DeanEdwards.removeEvent(window, 'mouseup', self.mouseup);
        DeanEdwards.removeEvent(window, 'mouseout', self.mouseout);
        DeanEdwards.removeEvent(window, 'mousemove', self.mousemove);
        self.mouseup = null;
        self.mouseout = null;
        self.mousemove = null;
        self.dragStartOffset = null; 
        window.droppable = null;
    }, // }}}

    function _restoreOriginalState(self) { /// {{{
        var n = self.node;
        n.style['top'] = self._savedTop;
        n.style['left'] = self._savedLeft;
        n.style['position'] = self._savedPosition;
        n.style['float'] = self._savedFloat;
    }, // }}}

    function _saveOriginalState(self) { // {{{
        var n = self.node;
        self._savedTop = n.style['top'];
        self._savedLeft = n.style['left'];
        self._savedPosition = n.style['position'];
        self._savedFloat = n.style['float'];
    }, // }}}

    function startDragging(self, event) { // {{{
        Divmod.debug("StainedGlass.DragState", "started dragging");

        // tables and things do weird stuff when you click and drag on them.
        // Don't let them do weird stuff.
        event.preventDefault();

        self._saveOriginalState();

        /* droppable nodes get saved in a window-global, so the drop consumers
         * can find them.
         */
        if (self.droppable) {
            self.dragStartOffset = {'x': 10, 'y': 0};
            window.droppable = self.node;
        } else {
            /* figure out the offset of the mouseclick from the top left of the
             * widget
             */
            var nodeCoords = StainedGlass.getPosition(self.node);
            self.dragStartOffset = {'x': event.pageX - nodeCoords['x'],
                                    'y': event.pageY - nodeCoords['y']};
        }

        /* set up mousemove event to follow the movement of the mouse */
        self.mousemove = function _(event) { return self.whileDragging(event) };
        DeanEdwards.addEvent(window, 'mousemove', self.mousemove);

        /* the mouseup event could happen *anywhere* so set up 
           cancelling events on the window
        */
        self.mouseup = function _(event) { return self.stopDragging(event) };
        self.mouseout = function _(event) { return self.cancelDragging(event) };
        DeanEdwards.addEvent(window, 'mouseup', self.mouseup);
        DeanEdwards.addEvent(window, 'mouseout', self.mouseout);
    }, // }}}

    function whileDragging(self, event) { // {{{
        var n = self.node;
        n.style['position'] = 'absolute';
        n.style['float'] = 'none';
        /* absolutely positioned nodes are positioned *RELATIVE TO THEIR
           offsetParent*.  This is <body> unless the node is, itself, inside
           an absolutely positioned node.  Either way, call
           getPosition(n.offsetParent) and adjust.
         */
        var offsetParentCoords = StainedGlass.getPosition(n.offsetParent);
        var l = (event.pageX - self.dragStartOffset['x'] - offsetParentCoords['x']);
        var t = (event.pageY - self.dragStartOffset['y'] - offsetParentCoords['y']);
        n.style['left'] = l + 'px';
        n.style['top'] = t + 'px';
    }, // }}}

    function stopDragging(self, event) { // {{{
        Divmod.debug("StainedGlass.DragState", "stopped dragging");
        self._cleanupDragState();
        /* droppable nodes don't really want to be moved.. snap them back when
         * released.
         */
        if (self.droppable) {
            self._restoreOriginalState();
        }
    }, // }}}

    function cancelDragging(self, event) { // {{{
        /* a little explanation:
         * When your mouse moves off the edge of the window, you're moving
         * FROM documentElement.
         * When you move from "dead space" into another element, you're 
         * also moving FROM documentElement, but you're moving INTO something 
         * else.
         * Therefore, the way we detect that we REALLY left the window
         * is if both target and explicitOriginalTarget are documentElement.
         */
        if (event.target === document.documentElement &&
            event.explicitOriginalTarget === document.documentElement) {
            Divmod.debug("StainedGlass.DragState", "cancelled dragging");
            self._cleanupDragState()
            self._restoreOriginalState()
            /* restore the position to the original position */
        } else {
            event.stopPropagation();
        }
    }, // }}}

    /* specify the node that will be draggable */
    function setDragHandle(self, node) { // {{{
        DeanEdwards.addEvent(node, 'mousedown', 
                function _(event) { return self.startDragging(event); }
        );
    } // }}}
); // }}}

/* Create the necessary events for a node to be draggable 
 * @arg vehicle: the node that will be moved around when you drag it
 * @arg handle: if specified, the node that you click on to move the vehicle
 * @arg droppable: if specified, dropstate will be attached as well.
 */
StainedGlass.draggable = function _(vehicle, handle, droppable) { // {{{
    var dragBehavior = new StainedGlass.DragState();

    dragBehavior.node = vehicle;

    vehicle.dragBehavior = dragBehavior; // keep dragBehavior from being gc'd

    if (handle) {
        // dragging the handle drags the node
        dragBehavior.setDragHandle(handle);
    } else {
        // dragging anywhere in the node drags the node
        dragBehavior.setDragHandle(vehicle);
    }

    dragBehavior.droppable = droppable;

    return vehicle;
}; // }}}

StainedGlass.Enclosure = Nevow.Athena.Widget.subclass('StainedGlass.Enclosure');
StainedGlass.Enclosure.methods( // {{{
    /* adds the title to the iconified node */
    function _decorateIconifiedTitle(self, titleNode) {
        var title2 = titleNode.cloneNode(true /* clone children */);
        var structure = document.createElement('div');
        structure.setAttribute('class', 'titlebar');
        var windowTitleNode = document.createElement('div');
        windowTitleNode.setAttribute('class', 'windowTitle');
        while (title2.childNodes.length > 0) {
            var n = title2.removeChild(title2.childNodes[0]);
            windowTitleNode.appendChild(n);
        }
        structure.appendChild(windowTitleNode);
        var minimizer = document.createElement('a');
        minimizer.setAttribute('class', 'minimizer');
        minimizer.appendChild(document.createTextNode('^'));
        structure.appendChild(minimizer);
        self.iconified.appendChild(structure);
    },

    function __init__(self, node) { // {{{
        StainedGlass.Enclosure.upcall(self, '__init__', node);
        try {
            var minimizer = self.firstNodeByClass('minimizer');
            DeanEdwards.addEvent(minimizer, 'click', 
                function onMinimize(event) { return self.minimize() });
            // Create an iconified node at the end of the widget's parent.
            // The iconfied version is what is shown when the widget minimizes.
            self.iconified = document.createElement('div');
            self.iconified.className = 'iconified-hidden';
            self._decorateIconifiedTitle(self.firstNodeByClass('windowTitle'));
            var restore = RT.firstNodeByAttribute(self.iconified, 'class', 
                    'minimizer');
            DeanEdwards.addEvent(restore, 'click', 
                    function onRestore(event) { return self.restore() 
            });

            node.parentNode.appendChild(self.iconified);
        } catch (e) { 
            if (!e.toString().match(/Failed to discover .*minimizer.*/)) {
                throw e;
            } else {
                // nothing
            }
        }

        /* set up dragging */
        if (node.className.match(/.*\bdraggable\b.*/)) {
            var titlebar = self.firstNodeByAttribute('class', 'titlebar');
            StainedGlass.draggable(self.node, titlebar);
        }

    }, // }}}

    function minimize(self) { // {{{
        var n = self.node;
        n.className = n.className.replace('enclosure', 'enclosure-hidden');
        var icon = self.iconified;
        icon.className = icon.className.replace('iconified-hidden', 'iconified');
    }, // }}}

    function restore(self) { // {{{
        var n = self.node;
        n.className = n.className.replace('enclosure-hidden', 'enclosure');
        var icon = self.iconified;
        icon.className = icon.className.replace('iconified', 'iconified-hidden');
    } // }}}
); // }}}

StainedGlass.TextArea = Nevow.Athena.Widget.subclass('StainedGlass.TextArea');
StainedGlass.TextArea.methods( // {{{
    function __init__(self,  // {{{
                      node, 
                      /* OPTIONAL */ initialContent) {
        StainedGlass.TextArea.upcall(self, '__init__', node);

        if (initialContent !== undefined)
            self.appendTo(initialContent);
    }, // }}}

    function appendTo(self, content) // {{{
    {
        RT.appendNodeContent(self.node, content);
        self.node.scrollTop = self.node.scrollHeight;
    } // }}}
); // }}}

// vi:foldmethod=marker
