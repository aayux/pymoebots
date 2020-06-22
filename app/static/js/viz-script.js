import './amoebot.viz-objects.js';
import {nameSpaceURI, cameraDim, scale, originLoc} from './config.js';

function addAmoebot( x, y ) {
    // add amoebots to the grid
    return undefined;
}

function onClickPlace() {
    // get click position
    addAmoebot( x, y )
}

// async function requestHistory() {
//     /*
//     load the state history from JSON source file
//     returns :: 200 on success, 400 on failure
//     */
//     // GET request to downloading tracking data
//     const requestStatus = await fetch( "history" )
//                         .then( response => response.json() )
//                         .then( response => (config0 , tracks) = response ) // NOTE: fix this
//                         .then( () => { return 200; } )
//                         .catch( () => { return 400; } );
//     return requestStatus;
// }

function updateViz() {
    /*
    the primary visual update function, changes grid, particle and maze 
    positions relative to the origin calculated on drag
    */

    ( function updateOrigin() {
        // update the anchored origin
        var origin = document.getElementById( "origin" );
        origin.setAttribute( "cx", originLoc.x );
        origin.setAttribute( "cy", originLoc.y );
    })();

    ( function updateGrid() {
        // update grid lines
        var gridViz = document.getElementById( "grid" );
        var moduloX = originLoc.x;
        var moduloY = originLoc.y;
        gridViz.setAttribute("transform",
        "translate(" + moduloX + ", " + moduloY + ")"
        );
    })();
}

function drawGrid() {
    var camera = document.getElementById( "camera" );
    camera.setAttribute( "width", cameraDim.w );
    camera.setAttribute( "height", cameraDim.h );

    var gridLines = [];
    
    // horizontal distance between grid lines
    var gridDist = Math.floor( cameraDim.w / scale );

    // get points for longitudanal lines
    for( var i = -cameraDim.w * gridDist; i <= cameraDim.w * gridDist; i += gridDist ) {
        gridLines.push({
            p1: {x: i, y: - 30 *  ( cameraDim.h + 1 ) }, 
            p2: {x: i, y: 30 * ( cameraDim.h + 1 ) }
        });
    }

    for( var i = -cameraDim.w * gridDist; i <= cameraDim.w * gridDist; i += gridDist ) {
        // right sheared diagonal
        gridLines.push({
            p1: { x : i, y : - 30 * ( cameraDim.h + 1 ) },
            p2: { x : i - 30 * ( cameraDim.h + 1 ) * Math.sqrt( 3 ), y : 30 * (cameraDim.h + 1) }
        });
        
        // left sheared diagonal
        gridLines.push({
            p1: {x : i, y : - 30 * ( cameraDim.h + 1 ) },
            p2: {x : i + 30 * ( cameraDim.h + 1 ) * Math.sqrt( 3 ), y : 30 * (cameraDim.h + 1) }
        });
    }

    // draw the grid
    for( var gridLine of gridLines ) {
        var newLine = document.createElementNS( nameSpaceURI, "line" );
        newLine.setAttribute( "stroke", "black" );
        newLine.setAttribute( "stroke-width", ".5" );
        newLine.setAttribute( "x1", gridLine.p1.x );
        newLine.setAttribute( "x2", gridLine.p2.x );
        newLine.setAttribute( "y1", gridLine.p1.y );
        newLine.setAttribute( "y2", gridLine.p2.y );
        camera.getElementById( "grid" ).appendChild(newLine);
    }
}

function allowDragMotion() {
    /* 
    allow drag across the grid
    */
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
}

function initializeTracker() {
    /*
    instantiate the amoebot tracker and place particles on the grid
    returns :: -1 on failure, 0 on success
    */
    if ( JSON.stringify( config0 ) == "{}" ) {
      console.log( "ERROR: No bot data was received!" );
      return -1;
    }

    window.vtracker = new AmoebotVizTracker( config0, tracks );
    window.nBots, window.nSteps = window.vtracker.getConfigInfo();

    updateViz();
    return 0;
}

function updateDisplay( step ) {
    /*
    update configuration information on the web page
    */
    var curStep = document.querySelector( '#step' );
    var nBots = document.querySelector( '#num_bots' );

    curStep.textContent = `Step: ${step}`;
    nBots.textContent = `# Amoebots : ${window.nBots}`;
}

function onClickPlay( playback_speed ) {
    /*

    */
    var step = 0;

    motor = setInterval(
        function () {
            updateDisplay( step );
            if ( step <= window.nSteps ) {
                window.vtracker.vizOneStep( step );
                step ++;
            }
    }, playback_speed );
}

function onClickStep( step ) {
   step ++;
    if ( step <= window.nSteps ) {
        vtracker.vizOneStep( step );
        updateViz();
        return 1;
   }
   return 0;
}

/*
driver code; load history, draw the grid and set up visualiser
*/
// requestHistory().then(
//     ( requestStatus ) => {
//         console.log( requestStatus );
//         if ( requestStatus == 200 ) {
//             drawGrid();
//             allowDragMotion();
//             initializeTracker();
//         } else {
//             console.log("Error: No bot data was receieved.")
//         }
//     }
// );

drawGrid();
allowDragMotion();