import { nameSpaceURI, cameraDim, unit, originLoc } from './config.js';
import { getRequest } from './apis.request-handler.js';
import { 
        shearPoint, 
        addAmoebot, 
        AmoebotVizTracker 
    } from './amoebot.viz-objects.js';

function getPlayBackSpeed() {
    var playback = document.getElementById( 'playback' );

    // update the current slider value
    playback.oninput = function() {
        return this.value;
    }

}

function onClickPlace() {
    // get click position and save as format of `TriGrid` class
    var x; var y;
    addAmoebot( x, y )
}

async function requestHistory( runId ) {
    /*
    load the state history from JSON source file
    returns :: 200 on success, 400 on failure
    */
    // GET request to fetch configuration and tracker data
    const requestStatus = await getRequest( 'history/' + runId )
                        .then( requestStatus => requestStatus )
                        .then( reqResponse => response = reqResponse )
                        .then( () => { return 200; } )
                        .catch( () => { return 400; } );
    return requestStatus;
}

function updateViz() {
    /*
    the primary visual update function, changes grid, particle and maze 
    positions relative to the origin calculated on drag
    */

    ( function updateOrigin() {
        // update the anchored origin
        var origin = document.getElementById( 'origin' );
        origin.setAttribute( 'cx', originLoc.x );
        origin.setAttribute( 'cy', originLoc.y );
    })();

    ( function updateAmoebots() {
        /* update bots positions relative to the origin */
        var bot_list = window.vtracker.bot_list;
        for( let i = 0; i < bot_list.length; i++ ) {
            var botViz = bot_list[i].vizObject;
            var tailPosition = shearPoint(bot_list[i].tail);
            var headPosition = shearPoint(bot_list[i].head);

            var xHead = originLoc.x + headPosition.x;
            var yHead = originLoc.y + headPosition.y;

            var xTail = originLoc.x + tailPosition.x;
            var yTail = originLoc.y + tailPosition.y;

            botViz.vizBotH.setAttribute( 'cx', xHead );
            botViz.vizBotH.setAttribute( 'cy', yHead );

            botViz.vizBotT.setAttribute( 'cx', xTail );
            botViz.vizBotT.setAttribute( 'cy', yTail );

            if ( xHead == xTail || yHead == yTail ) {
                botViz.lineElement.setAttribute( 'x1', xTail );
                botViz.lineElement.setAttribute( 'x2', xHead );
                botViz.lineElement.setAttribute( 'y1', yTail );
                botViz.lineElement.setAttribute( 'y2', yHead );
                botViz.vizObject.appendChild( botViz.lineElement );
            }
        }
    })();

    ( function updateGrid() {
        // update grid lines
        var gridViz = document.getElementById( 'grid' );
        var moduloX = originLoc.x % ( unit * Math.sqrt( 3 ) );
        var moduloY = originLoc.y % unit;
        gridViz.setAttribute('transform',
        'translate(' + moduloX + ', ' + moduloY + ')'
        );
    })();
}

function drawGrid() {
    var camera = document.getElementById( 'camera' );
    camera.setAttribute( 'width', cameraDim.w );
    camera.setAttribute( 'height', cameraDim.h );

    var gridLines = [];

    // horizontal distance between grid lines
    var hGridDist = unit * Math.sqrt(3);

    // get points for longitudanal lines
    for( let i = - hGridDist; i <= cameraDim.w + hGridDist; i += hGridDist / 2 ) {
        gridLines.push({
            p1: {x: i, y: - 2 *  unit }, 
            p2: {x: i, y: cameraDim.h + ( 2 * unit ) }
        });
    }

    // vertical offsets on the grid
    var vGridOffset = ( Math.floor( cameraDim.h / ( 2 * unit ) ) + 1 ) * unit * 3;
    for( let i = -vGridOffset; i <= cameraDim.h + vGridOffset; i += unit ) {
        // right sheared diagonal
        gridLines.push({
            p1: { x : -2 * hGridDist, y : i },
            p2: { 
                    x : cameraDim.w + ( 2 * hGridDist ), 
                    y : i - ( cameraDim.w + 4 * hGridDist ) / Math.sqrt( 3 )
            }
        });
        
        // left sheared diagonal
        // TIP: swap x and y for p2 to see cool folds in the grid!
        gridLines.push({
            p1: {x : -2 * unit * Math.sqrt(3), y : i },
            p2: {
                    x : cameraDim.w + ( 2 * hGridDist ), 
                    y : i + (cameraDim.w + 4 * hGridDist) / Math.sqrt(3) 
                }
        });
    }

    // draw the grid
    for( let gridLine of gridLines ) {
        var newLine = document.createElementNS( nameSpaceURI, 'line' );
        newLine.setAttribute( 'stroke', 'black' );
        newLine.setAttribute( 'stroke-width', '.25' );
        newLine.setAttribute( 'x1', gridLine.p1.x );
        newLine.setAttribute( 'x2', gridLine.p2.x );
        newLine.setAttribute( 'y1', gridLine.p1.y );
        newLine.setAttribute( 'y2', gridLine.p2.y );
        camera.getElementById( 'grid' ).appendChild(newLine);
    }
}

function allowDragMotion() {
    /* 
    allow drag across the grid
    */
    var camera = document.getElementById( 'camera' );
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

function launchEventListener() {
    document.getElementById( 'btn-step' ).addEventListener( 'click', onClickStep);
}

function initializeTracker() {
    /*
    instantiate the amoebot tracker and place particles on the grid
    returns :: -1 on failure, 0 on success
    */
    if ( JSON.stringify( response.init0 ) == '{}' ) {
      console.log( "ERROR: Response string is empty" );
      return -1;
    }

    window.vtracker = new AmoebotVizTracker( 
                                response.init0, response.tracks 
                        );
    [window.nBots, window.nSteps] = window.vtracker.getConfigInfo();

    updateViz();
    return 0;
}

function updateDisplay() {
    /*
    update configuration information on the web page
    */
    var curStep = document.querySelector( '#step' );
    var nBots = document.querySelector( '#num_bots' );

    curStep.textContent = `Step: ${ step }`;
    nBots.textContent = `# Amoebots : ${ window.nBots }`;
}

function onClickPlay( playback_speed ) {
    /*
    */
    motor = setInterval(
        function () {
            updateDisplay();
            if ( step <= window.nSteps ) {
                window.vtracker.vizOneStep( step );
                step ++;
            }
    }, playback_speed );
}

/* global variables */
// step counter
var step = 0;
// json response variable
var response;

function onClickStep() {
    /*
    */
   if ( step <= window.nSteps ) {
        step += window.vtracker.vizOneStep( step );
        updateViz();
        return 1;
   }
   return 0;
}

/*
driver code; load history, draw the grid and set up visualiser
*/

drawGrid();

var runs = document.getElementById( 'config-files' )
runs.oninput = function() {
    requestHistory( this.files[0].name ).then(
        ( requestStatus ) => {
            if ( requestStatus == 200 ) {
                initializeTracker();
                allowDragMotion();
                launchEventListener();
            } else {
                console.log('ERROR: No bot data was receieved.')
            }
        }
    );
}