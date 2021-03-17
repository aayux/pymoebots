//import { nameSpaceURI, cameraDim, unit, originLoc } from './config.js';
import { nameSpaceURI, cameraDim, unit} from './config.js';
//import { getRequest } from './apis.request-handler.js';
import { sendRequest } from './apis.request-handler.js';
/*import {
        shearPoint,
        addAmoebot,
        AmoebotVizTracker
    } from './amoebot.viz-objects.js';*/
import {tri2Euclid, Amoebot, Wall} from './viz-objects.js';

const camera = document.getElementById("camera")
const amoebotsDOM = camera.getElementById("amoebots");


function transformToSVGPoint( coordinate ) {
    /*
    take a point and convert to svg coordinates, by applying each parent viewbox
    */
    var camera = document.getElementById( 'camera' );
    var svgPoint = camera.createSVGPoint();
    svgPoint.x = coordinate.clientX;
    svgPoint.y = coordinate.clientY;
    return svgPoint.matrixTransform( camera.getScreenCTM().inverse() );;
}

function  nearestGridPoint(point) {
    /*
    take an svg point and convert to grid coordinates
    */
    var x = Math.round( coordinate.x / ( unit * Math.sqrt( 3 ) / 2 ) );
    return {x : x, y : Math.round( coordinate.y / unit - x / 2 )};
}

function onClickPlace() {
    // get click position and save as format of `TriGrid` class
    var x; var y;
    addAmoebot( x, y )
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

function onClickPlay() {
    /*
    */

    // unset the pause condition to false
    var paused = false;

    // get the slider value before starting
    var slider = document.getElementById( 'playback' )
    var playbackSpeed = 100 - slider.value;
    slider.addEventListener( 'change',
                             function () {
                                playbackSpeed = 100 - slider.value;
                            });

    // listen for pause events
    document.getElementById( 'btn-pause' ).addEventListener(
                                            'click',
                                            function() {
                                                paused = !paused;
                                            });

    function timedPlayback () {
        // updateDisplay();
        if ( !paused && step < window.nSteps ) {
            step += 1;
            controller.objectDirector.updateVisuals(step);
            setTimeout( timedPlayback, playbackSpeed );
        } else {
            alert(' Finished! ');
        }
    }

    var playback = setTimeout( timedPlayback, playbackSpeed );
}

/* global variables */

// step counter
var step = 0;

function onClickStep() {
    if ( step < window.nSteps ) {
        step += 1;
        controller.objectDirector.updateVisuals(step);
        return 1;
   }
   return 0;
}

function onClickBack() {
    /*
    */

    if ( step > 0 ) {
        step -= 1
        window.vtracker.vizOneStep( step );
        updateViz();
        return 1;

   }
   return 0;
}






class directorController {
  constructor(sVG) {
    this.sVG = sVG;
    this.sVGDirector = new sVGDirector(sVG);
    this.objectDirector = null;
  }
  createObjectDirector(config0, tracks) {
    this.objectDirector = new objectDirector(config0, tracks, this.sVG);
  }
}


class sVGDirector {
  constructor(sVG) {
    this.sVG = sVG;
    this.sVG.setAttribute("viewBox", `0 0 ${cameraDim.w} ${cameraDim.h}`);
    this.gridGroup = this.createGrid();
    this._viewBox = this.sVG.viewBox.baseVal;
    this._moveDisplacement = {x:0, y:0};
    this._zoomDisplacement = {x:0, y:0};//In case ya want zoom.
    this.allowDragMotion();
  }
  moveBy(vectorX, vectorY) {
    this._moveDisplacement.x += vectorX;
    this._moveDisplacement.y += vectorY;
    this._viewBox.x = this._moveDisplacement.x + this._zoomDisplacement.x;
    this._viewBox.y = this._moveDisplacement.y + this._zoomDisplacement.y;
    this.updateVisuals();
  }
  allowDragMotion() {
    var self = this;
    var dragLoc = { x : 0, y : 0 };
    self.sVG.onmousedown = function( event ) {
      self.sVG.onmousemove = gridDrag;
      self.sVG.onmouseup = endDrag;
      self.sVG.onmouseleave = endDrag;
      dragLoc.x = event.clientX;
      dragLoc.y = event.clientY;
    }
    function gridDrag( event ) {
      self.moveBy(dragLoc.x - event.clientX, dragLoc.y - event.clientY);
      dragLoc.x = event.clientX;
      dragLoc.y = event.clientY;
    }
    function endDrag() {
      self.sVG.onmousemove = null;
      self.sVG.onmouseup = null;
      self.sVG.onmouseleave = null;
    }
  }
  createGrid() {
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
        p1: {x : -2 * hGridDist, y : i },
        p2: {x : cameraDim.w + ( 2 * hGridDist ),
           y : i - ( cameraDim.w + 4 * hGridDist ) / Math.sqrt( 3 )
        }
      });
        // left sheared diagonal
        // TIP :: swap x and y for p2 to see cool folds in the grid!
      gridLines.push({
        p1: {x : -2 * unit * Math.sqrt(3), y : i },
        p2: {x : cameraDim.w + ( 2 * hGridDist ),
           y : i + (cameraDim.w + 4 * hGridDist) / Math.sqrt(3)
        }
      });
    }
    var gridGroup = camera.getElementById( 'grid' );
    // draw the grid
    for( let gridLine of gridLines ) {
      var newLine = document.createElementNS( nameSpaceURI, 'line' );
      newLine.setAttribute( 'stroke', 'black' );
      newLine.setAttribute( 'stroke-width', '.25' );
      newLine.setAttribute( 'x1', gridLine.p1.x );
      newLine.setAttribute( 'x2', gridLine.p2.x );
      newLine.setAttribute( 'y1', gridLine.p1.y );
      newLine.setAttribute( 'y2', gridLine.p2.y );
      gridGroup.appendChild(newLine);
    }
    return gridGroup;
  }
  updateVisuals() {
    var wholeX = Math.floor(this._viewBox.x / (unit * Math.sqrt(3)));
    var wholeY = Math.floor(this._viewBox.y / unit);
    this.gridGroup.setAttribute('transform',
      `translate(${(unit * Math.sqrt(3)) * wholeX}, ${unit * wholeY})`
    );
  }
}


class objectDirector {
  constructor(config0, tracks, sVG) {
    // starting configuration of the system
    this.init_b = config0[ 'bots' ];
    this.init_w = config0[ 'walls' ];

    // motion history tracker
    this.tracks = tracks;
    console.log(this.tracks);

    this.amoebotVisuals = sVG.getElementById("amoebots");
    this.wallVisuals = sVG.getElementById("walls");
    this.amoebots = this.createAmoebots();
    this.walls = this.createWalls();
  }
  createAmoebots() {
    if(this.init_b.length == 0) return;
    var allAmoebots = [];
    for(let i = 0; i < this.init_b.length; i++) {
      allAmoebots.push(new Amoebot(i, this.tracks[0][i], this.amoebotVisuals));
    }
    return allAmoebots;
  }
  createWalls() {
    if(this.init_w.length == 0) return;
    var allWalls = [];
    for(let i = 0; i < this.init_w.length; i++) {
      allWalls.push(new Wall(i, this.init_w[i], this.amoebotVisuals));
    }
    return allWalls;
  }
  updateVisuals(step) {
    for(let i = 0; i < this.amoebots.length; i++) {
      this.amoebots[i].updateVisuals(this.tracks[step][i]);
    }
  }
}


// json response variable
var response;
var controller = new directorController(camera);

/*
  driver code; load history, draw the grid and set up visualiser
*/
var runs = document.getElementById( 'config-files' )
runs.oninput = function() {
    requestHistory( this.files[0].name ).then(
        ( requestStatus ) => {
            if ( requestStatus == 200 ) {
                controller.createObjectDirector(response.config0, response.tracks);
                window.nSteps = controller.objectDirector.tracks.length
                launchEventListener();
            } else {
                console.log( 'ERROR: No bot data was receieved.' );
            }
        }
    );
}


async function requestHistory( runId ) {
    /*
    load the state history from JSON source file
    returns :: 200 on success, 400 on failure
    */
    // GET request to fetch configuration and tracker data
    //const requestStatus = await getRequest( 'history/' + runId )
    const requestStatus = await sendRequest( 'history/' + runId )
                        .then( requestStatus => requestStatus )
                        .then( reqResponse => response = reqResponse )
                        .then( () => { return 200; } )
                        .catch( () => { return 400; } );
    return requestStatus;
}

/*
function initializeTracker() {

    instantiate the amoebot tracker and place particles on the grid
    returns :: -1 on failure, 0 on success

    if ( JSON.stringify( response.config0 ) == '{}' ) {
      console.log( "ERROR: Response string is empty" );
      return -1;
    }
    window.vtracker = new AmoebotVizTracker(
                                response.config0, response.tracks
                        );
    //FIX THIS PLEASE SELF
    window.vtracker = new directorController(sVG, response.config0, response.tracks);
    [ window.nBots, window.nSteps ] = window.vtracker.getConfigInfo();
    updateViz();
    return 0;
}
*/

function launchEventListener() {
    document.getElementById( 'btn-step' ).addEventListener( 'click',
                                                            onClickStep
                                                        );
    document.getElementById( 'btn-play' ).addEventListener( 'click',
                                                            onClickPlay
                                                        );
}
