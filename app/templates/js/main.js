var nameSpaceURI = "http://www.w3.org/2000/svg";
var algName = "pymoebots";
var cameraDim = {w: 1800, h: 800};
var scale = 60;

var originLoc = {x: 0, y: 0};
var amoebotLoc = [];

( function drawGrid() {
    var camera = document.getElementById( "camera" );
    camera.setAttribute( "width", cameraDim.w );
    camera.setAttribute( "height", cameraDim.h );

    var gridLines = [];
    
    // horizontal distance between grid lines
    var gridDist = Math.floor( cameraDim.w / scale );

    // get points for longitudanal lines
    for( var i = -gridDist; i <= cameraDim.w + gridDist; i += gridDist ) {
        gridLines.push({
            p1: {x: i, y: -1 * (cameraDim.h + 1)}, 
            p2: {x: i, y: cameraDim.h + 1}
        });
    }

    for( var i = -cameraDim.w; i <= cameraDim.w * gridDist; i += gridDist ) {
        // right sheared diagonal
        gridLines.push({
            p1: { x : i, y : - ( cameraDim.h + 1 ) },
            p2: { x : i - ( cameraDim.h + 1 ) * Math.sqrt( 3 ), y : cameraDim.h + 1 }
        });
        
        // left sheared diagonal
        gridLines.push({
            p1: {x : i, y : -1 * (cameraDim.h + 1)},
            p2: {x : i + ( cameraDim.h + 1 ) * Math.sqrt( 3 ), y : cameraDim.h + 1 }
        });
    }

    // draw the grid
    for( gridLine of gridLines ) {
        var newLine = document.createElementNS( nameSpaceURI, "line" );
        newLine.setAttribute( "stroke", "black" );
        newLine.setAttribute( "stroke-width", ".5" );
        newLine.setAttribute( "x1", gridLine.p1.x );
        newLine.setAttribute( "x2", gridLine.p2.x );
        newLine.setAttribute( "y1", gridLine.p1.y );
        newLine.setAttribute( "y2", gridLine.p2.y );
        camera.getElementById( "grid" ).appendChild(newLine);
    }
})();


( function dragMotion() {
    // drag around the grid
    var camera = document.getElementById( "camera" );
    var dragLoc = { x : 0, y : 0 };

    camera.onmousedown = function( event ) {
        camera.onmousemove = gridDrag;
        camera.onmouseup = endDrag;
        camera.onmouseleave = endDrag;
        dragLoc.x = event.clientX;
        dragLoc.y = event.clientY;
    }

    function gridDrag( event ) {
        originLoc.x += event.clientX - dragLoc.x;
        originLoc.y += event.clientY - dragLoc.y;
        updateViz();
        dragLoc.x = event.clientX;
        dragLoc.y = event.clientY;
    }

    function endDrag() {
        camera.onmousemove = null;
        camera.onmouseup = null;
        camera.onmouseleave = null;
  } 
})();


function updateViz() {
    /* 
    The primary visual update function :: changes bot positions and line 
    positions relative to the origin calculated on drag
    */
    
    ( function updateOrigin() {
        // update the anchored origin
        var origin = document.getElementById( "origin" );
        origin.setAttribute( "cx", originLoc.x );
        origin.setAttribute( "cy", originLoc.y );
    })();
    
    /*
    ( function updateAmoebots() {
        // update bot positions relative to the origin
        var amoebotVis = manager.bot_dict;
        for( var i = 0; i < amoebotVis.length; i++ ) {
            var amoebotParts = amoebotVis[ i ].visualRep;
            var tailLocation = squareToTriangle( amoebotVis[ i ].tail );
            var headLocation = squareToTriangle( amoebotVis[ i ].head );

            amoebotParts.botTail.setAttribute( "cx", originLoc.x + tailLocation.x );
            amoebotParts.botTail.setAttribute( "cy", originLoc.y + tailLocation.y );

            amoebotParts.botHead.setAttribute( "cx", originLoc.x + headLocation.x );
            amoebotParts.botHead.setAttribute( "cy", originLoc.y + headLocation.y );
        }
    })(); 
    */

    ( function updateGrid() {
        // update grid lines
        var gridViz = document.getElementById( "grid" );
        var moduloX = originLoc.x % scale;
        var moduloY = originLoc.y % ( scale * Math.sqrt( 3 ) );
        gridViz.setAttribute("transform",
        "translate(" + moduloX + ", " + moduloY + ")"
        );
    })();
}

function squareToTriangle( point ) {
    // shear points from the Euclidean plane into the triangular grid
    newPoint = { x : 0, y : 0 };
    newPoint.x += point.x * scale;
    if ( point.y % 2 == 1 ) { newPoint.x += ( 1 / 2 ) * scale; }
    newPoint.y -= ( point.y * Math.sqrt( 3 ) / 2 ) * scale;
    return( newPoint );
}

function addAmoebot( x , y ) {
    // add amoebots to the grid
}