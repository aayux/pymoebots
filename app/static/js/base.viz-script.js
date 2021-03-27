import { nameSpaceURI, cameraDim, unit} from './config.js';
import { sendRequest } from './apis.request-handler.js';
import {tri2Euclid, Amoebot, Wall} from './viz-objects.js';

//Multiply point by svg matrix inverse to get point in svg coordinates
function transformToSVGPoint(sVG, point) {
    var sVGPoint = sVG.createSVGPoint();
    sVGPoint.x = point.hasOwnProperty('x') ? point.x : point.clientX;
    sVGPoint.y = point.hasOwnProperty('y') ? point.y : point.clientY;
    return sVGPoint.matrixTransform(sVG.getScreenCTM().inverse());;
}

function nearestGridPoint(point) {
    /*
      take an svg point and convert to nearest grid coordinates
      to keep illegal coordinates from occuring, have to find the number
      of y units from line zero and double the total number of units
      from line zero.
      The equations are after reduction.
    */
    var xUnit = unit * Math.sqrt(3) / 2;
    var xTri = Math.round(point.x / xUnit);
    var yTri = Math.round(point.y / unit - xTri / 2);
    return {x:xTri, y:2 * yTri + xTri};
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


class directorController {
  constructor(sVG) {
    this.sVG = sVG;
    this.tracks = null;
    this.isPlayable = false;
    this.totalSteps = 0;
    this.step = 0;
    this.paused = false;
    this.playBackSpeed = 50;
    this.sVGDirector = new sVGDirector(sVG);
    this.objectDirector = new objectDirector(sVG);
    this._addLeftMenuEventListeners();
    this._addBottomMenuEventListeners();
  }

  loadAlgorithm(config0, tracks) {
    this.tracks = tracks;
    this.isPlayable = true;
    this.totalSteps = tracks.length;
    for(let i = 0; i < tracks[0].length; i++) {
      this.objectDirector.addAmoebot(i, config0["bots"][i]);
    }
    for(let i = 0; i < config0["walls"].length; i++) {
      this.objectDirector.addWall(i, config0["walls"][i]);
    }
  }

  _addLeftMenuEventListeners() {
    var self = this;
    document.getElementById("buttonStartEditMode").addEventListener('click', startEditMode);

    function startEditMode() {
      self.isPlayable = false;
      self.sVGDirector.isDraggable = false;
      self.objectDirector.isEditable = true;
    }
  }

  _addBottomMenuEventListeners() {
    var self = this;
    var slider = document.getElementById("playback");
    document.getElementById( 'buttonBack' ).addEventListener('click', onClickBack);
    document.getElementById( 'buttonStep' ).addEventListener('click', onClickStep);
    document.getElementById( 'buttonPlay' ).addEventListener('click', onClickPlay);
    slider.addEventListener( 'change', function () {
      self.playbackSpeed = 100 - slider.value;
    });
    document.getElementById("buttonPause").addEventListener('click', function() {
      self.paused = !self.paused;
    });

    function onClickPlay() {
      if(!self.isPlayable) return false;
      self.paused = false;
      function timedPlayback () {
        if(!self.paused && onClickStep()) {
          setTimeout(timedPlayback, self.playbackSpeed);
        } else {
          alert(' Finished! ');
        }
      }
      var playback = setTimeout(timedPlayback, self.playbackSpeed);
    }

    function onClickStep() {
      if(!self.isPlayable) return false;
      if(self.step < self.totalSteps) {
        self.objectDirector.updateVisuals(self.tracks[self.step]);
        self.step += 1;
         return true;
      }
      return false;
    }

    function onClickBack() {
      if(!self.isPlayable) return false;
      if(self.step > 0) {
        self.step -= 1;
        self.objectDirector.updateVisuals(self.tracks[self.step]);
      }
    }
  }
}


class sVGDirector {
  constructor(sVG) {
    this.isDraggable = true;
    this.sVG = sVG;
    this.sVG.setAttribute("viewBox", `0 0 ${cameraDim.w} ${cameraDim.h}`);
    this.gridGroup = this.createGrid();
    this._viewBox = this.sVG.viewBox.baseVal;
    this._moveDisplacement = {x:0, y:0};
    this._zoomDisplacement = {x:0, y:0};//In case ya want zoom.
    this.allowDragging();
  }

  moveBy(vectorX, vectorY) {
    this._moveDisplacement.x += vectorX;
    this._moveDisplacement.y += vectorY;
    this._viewBox.x = this._moveDisplacement.x + this._zoomDisplacement.x;
    this._viewBox.y = this._moveDisplacement.y + this._zoomDisplacement.y;
    this.updateVisuals();
  }

  allowDragging() {
    var self = this;
    var isDragging = false;
    var dragLoc = {x:0, y:0};
    self.sVG.addEventListener("mousedown", dragStart);
    self.sVG.addEventListener("mousemove", dragMid);
    self.sVG.addEventListener("mouseup", dragEnd);
    self.sVG.addEventListener("mouseleave", dragEnd);
    function dragStart( event ) {
      if(!self.isDraggable) return false;
      isDragging = true;
      dragLoc = transformToSVGPoint(self.sVG, event)
    }
    function dragMid( event ) {
      if(!isDragging) return false;
      const vectorSVG = transformToSVGPoint(self.sVG, event)
      self.moveBy(dragLoc.x - vectorSVG.x, dragLoc.y - vectorSVG.y);
    }
    function dragEnd() {
      if(!isDragging) return false;
      isDragging = false;
    }
  }

  createGrid() {
    var camera = document.getElementById( 'camera' );
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
  constructor(sVG) {
    this.sVG = sVG;
    this.isEditable = false;
    this.amoebotVisuals = sVG.getElementById("amoebots");
    this.wallVisuals = sVG.getElementById("walls");
    this.amoebots = [];
    this.walls = [];
    this.allowEditing();
  }

  allowEditing() {
    var self = this;
    self.sVG.addEventListener("mousedown", addAmoebot);

    function addAmoebot(event) {
      if(!self.isEditable) return false;
      var coordinate = transformToSVGPoint(self.sVG, event);
      console.log(coordinate);
      var triCoordinate = nearestGridPoint(coordinate);
      console.log(triCoordinate);
      self.addAmoebot(self.amoebots.length, [triCoordinate.x,  triCoordinate.y]);
    }
  }

  addAmoebot(name, location) {
    this.amoebots.push(new Amoebot(name, location, this.amoebotVisuals));
  }

  addWall(name, location, parentVisual) {
    this.walls.push(new Wall(name, location, this.wallVisuals));
  }

  updateVisuals(data) {
    for(let i = 0; i < this.amoebots.length; i++) {
      this.amoebots[i].updateVisuals(data[i]);
    }
  }
}


var controller = new directorController(camera);

/*
  driver code; load history, draw the grid and set up visualiser
*/
document.getElementById("loadRun").addEventListener("click", requestHistory);

async function requestHistory( runId ) {
    /*
    load the state history from JSON source file
    returns :: 200 on success, 400 on failure
    */
    // GET request to fetch configuration and tracker data
    var runName = document.getElementById("runName").value;
    var response = {status:200, values:{}};
    await sendRequest('history/' + runName)
      .then(reqResponse => {response.values = reqResponse;})
      .catch(() => {response.status = 400;});
    if(response.status == 200) {
      controller.loadAlgorithm(response.values.config0, response.values.tracks);
    } else {
      console.log('ERROR: No bot data was receieved.');
    }
}

(async function requestRunNames() {
  await sendRequest("algorithms/").then((response) => {
    var runList = document.getElementById("runList");
    var runs = response.Algorithms;
    for(let i = 0; i < runs.length; i++) {
      var run = document.createElement("option");
      run.value = runs[i];
      runList.appendChild(run);
    }
  })
})();
