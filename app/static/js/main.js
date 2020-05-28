nameSpaceURI = "http://www.w3.org/2000/svg";

var cameraDim = {w: 1500, h: 750};
var scale = 41;
var originLoc = {x: 0, y: 0};
var amoebotLoc = [];

class AmoebotVizManager {
    /*
    mantains visual information and current position of particles
    */
    constructor( state_history ) {
        this.state_history = state_history;
        this.state_dict = [];
        
        // Current round of simulation.
        this._round = 0;

        // Tracks whether the current round is through
        this.incompleteRound = false;

        for ( let ix in this.state_history[ '0' ] ) {
            this.state_dict.push(
                new AmoebotData(
                    this.state_history['0'][ix].x,
                    this.state_history['0'][ix].y, ix,
                )
            );
        }
      this.simData = null;
      if (this.state_history){
        this.simData = this.analyzeBotHistory();
      }
    }

    analyzeBotHistory() {
      /*
      Find out how many bots we have and how many rounds.
      */
      var bots   = Object.keys(this.bot_history['0']).length;
      var rounds = Object.keys(this.bot_history).length;
      return({rounds, bots});
    }

    singleBotStepFunction(round, bot, updateVis) {
      if (round <= this.simData.rounds) {
        if (round > 0) {
          this.incompleteRound = true;
        }
        if (bot <= this.simData.bots) {
          let historical_bot = this.bot_history[round][bot];
          let curr_bot = this.bot_dict[bot];

          curr_bot.head.x = (historical_bot.x % 2 == 0) ? historical_bot.x / 2 : (historical_bot.x - 1) / 2;
          curr_bot.head.y = historical_bot.y;

          curr_bot.tail.x = (historical_bot.x % 2 == 0) ? historical_bot.x / 2 : (historical_bot.x - 1) / 2;
          curr_bot.tail.y = historical_bot.y;

          curr_bot.agent_stage = historical_bot.agents_on;
          curr_bot.agent_statuses_stage = {
            'agent0': historical_bot.agent0,
            'agent1': historical_bot.agent1,
            'agent2': historical_bot.agent2
          };
          curr_bot.update();
          if (updateVis) updateVisuals();
        }
        if (round == this.simData.rounds) {
          this.incompleteRound = false;
        }
      }
    }

    stepFunction (updateVis) {
      /*
      Updates the bots' positions and states from previous step.
      One step is one full pass through all the bots.
      */
      this.step ++;
      for (let i in this.bot_history[this.step]) {

        this.singleBotStepFunction(this.step, i, updateVis);

      }
      //updateVisuals();
    }
  }


/*
function shearPoint( point ) {
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
*/

async function requestHistory() {
    /*
    load the state history from JSON source file
    returns :: 200 on success, 400 on failure
    */
    // GET request to downloading tracking data
    const response = await fetch( "history" )
                        .then( response => response.json() )
                        .then( data => state_history = data )
                        .then( () => { return 200; } )
                        .catch( () => { return 400; } );
    return response;
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

function updateViz() {
    // The primary visual update function :: changes bot positions and line 
    // positions relative to the origin calculated on drag
    
    
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

function initializeManager() {
    /*
    instantiate the amoebot manager and place particles on the grid
    returns :: -1 on failure, 0 on success
    */
    if ( JSON.stringify(state_history) == "{}" ) {
      console.log( "ERROR: No bot data was received!" );
      return -1;
    }
    vmanager = new AmoebotVizManager( state_history );
    updateViz();
    return 0;
}

/*
driver code :: load history, draw the grid and set up visualiser
*/
requestHistory().then(
    ( response ) => {
        console.log( response );
        if ( response == 200 ) {
            drawGrid();
            allowDragMotion();
            initializeManager();
        } else {
            console.log("Error: No bot data was receieved.")
        }
    }
);