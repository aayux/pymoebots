import { nameSpaceURI, cameraDim, unit} from './config.js';
import { sendRequest } from './apis.request-handler.js';
import {tri2Euclid, Amoebot, Wall} from './viz-objects.js';

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
    this.amoebotVisuals = sVG.getElementById("amoebots");
    this.wallVisuals = sVG.getElementById("walls");
    this.amoebots = [];
    this.walls = [];
    this.occupied = new Set();
  }

  determineOccupied() {
    this.occupied = new Set();
    for(let amoebot of this.amoebots) {
      this.occupied.add(`${amoebot.location.head_pos[0]},${amoebot.location.head_pos[1]}`);
      this.occupied.add(`${amoebot.location.tail_pos[0]},${amoebot.location.tail_pos[1]}`);
    }
  }

  resetObjects() {
    this.amoebotVisuals.innerHTML= '';
    this.wallVisuals.innerHTML= '';
    this.amoebots = [];
    this.walls = [];
  }

  addAmoebot(name, location) {
    if(this.occupied.has(`${location[0]},${location[1]}`)) return;
    this.amoebots.push(new Amoebot(name, location, this.amoebotVisuals));
    this.occupied.add(`${location[0]},${location[1]}`)
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


/*Class amoebotWebPageInterface
 */
class amoebotWebPageInterface {
  constructor(sVG) {
    this.mode = "MENU";//MENU:default, EDIT:addAmoebots, ANIM:animation,
    this.algorithm = {config0:[], tracks:[]};
    this.step = 0;
    this.totalSteps = 0;
    this.paused = false;
    this.playBackSpeed = 50;
    this.sVGDirector = new sVGDirector(sVG);
    this.objectDirector = new objectDirector(sVG);
  }
  async requestRunData(runName) {
    var response = {status:200, values:{}};
    await sendRequest('history/' + runName)
      .then(reqResponse => {response.values = reqResponse;})
      .catch(() => {response.status = 400;});
    if(response.status == 200) {
      this.step = 0;
      this.totalSteps = response.values.tracks.length;
      this.algorithm.config0 = response.values.config0;
      this.algorithm.tracks = response.values.tracks;
      this.objectDirector.resetObjects();
      this.loadAlgorithm();
    } else {
      console.log('ERROR: No bot data was receieved.');
    }
  }
  async requestSaveRunData() {
    var runNameSave = document.getElementById("runNameSave").value;
    var algorithmName = document.getElementById("algorithmName").value;
    var rounds = document.getElementById("rounds").value;
    var bots = [];
    var bot_tails = [];
    var walls = [];
    for(let amoebot of this.objectDirector.amoebots) {
      bots.push(amoebot.location.head_pos);
      bot_tails.push(amoebot.location.tail_pos);
    }
    for(let wall of this.objectDirector.walls) {
      walls.push(wall.location);
    }
    await sendRequest("algorithms/", {
      algorithm:algorithmName,
      name:runNameSave,
      rounds:+rounds,
      bots:bots,
      "bot tails":bot_tails,
      walls:walls
    }, "POST").then(response => {
      this.step = 0;
      this.totalSteps = response.tracks.length;
      this.algorithm.config0 = response.config0;
      this.algorithm.tracks = response.tracks;
      this.objectDirector.resetObjects();
      this.loadAlgorithm();
    });
  }
  loadAlgorithm() {
    for(let i = 0; i < this.algorithm.tracks[0].length; i++) {
      this.objectDirector.addAmoebot(i, this.algorithm.config0["bots"][i]);
    }
    for(let i = 0; i < this.algorithm.config0["walls"].length; i++) {
      this.objectDirector.addWall(i, this.algorithm.config0["walls"][i]);
    }
  }
}


/*HTML to JavaScript Controls*/
var webPage = new amoebotWebPageInterface(document.getElementById("camera"));
/*Initializers*/
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
/*Listeners*/
/*SVG*/
document.getElementById("camera").addEventListener("click", (event) => {
  if(webPage.mode != "EDIT") return false;
  var coordinate = transformToSVGPoint(document.getElementById("camera"), event);
  var triCoordinate = nearestGridPoint(coordinate);
  webPage.objectDirector.addAmoebot(webPage.objectDirector.amoebots.length,
    [triCoordinate.x,  triCoordinate.y]
  );
});

/*Left Menu Buttons*/
document.getElementById("buttonOpenLoadMenu").addEventListener("click", async () => {
  document.getElementById("menuLoad").classList.toggle("hide");
  document.getElementById("menuSave").classList.add("hide");
});
document.getElementById("loadRun").addEventListener("click", () => {
  var runNameLoad = document.getElementById("runNameLoad").value;
  webPage.requestRunData(runNameLoad);
  document.getElementById("menuLoad").classList.add("hide");
  webPage.mode = "ANIM";
});
document.getElementById("buttonStartEditMode").addEventListener("click", () => {
  document.getElementById("menuLoad").classList.add("hide");
  document.getElementById("menuSave").classList.add("hide");
  webPage.objectDirector.determineOccupied();
  webPage.mode = "EDIT";
});
document.getElementById("buttonOpenSaveMenu").addEventListener("click", () => {
  document.getElementById("menuSave").classList.toggle("hide");
  document.getElementById("menuLoad").classList.add("hide");
});
document.getElementById("saveRun").addEventListener("click", () => {
  webPage.requestSaveRunData();
  document.getElementById("menuSave").classList.add("hide");
  webPage.mode = "ANIM";
});

/*Bottom Menu Buttons*/
document.getElementById("buttonStep").addEventListener('click', () => {
  if(webPage.mode != "ANIM") return false;
  if(webPage.step < webPage.totalSteps) {
    webPage.objectDirector.updateVisuals(webPage.algorithm.tracks[webPage.step]);
    webPage.step += 1;
  }
});
document.getElementById( 'buttonBack' ).addEventListener('click', () => {
  if(webPage.mode != "ANIM") return false;
  if(webPage.step > 0) {
    webPage.step -= 1;
    webPage.objectDirector.updateVisuals(webPage.algorithm.tracks[webPage.step]);
  }
});
document.getElementById( 'buttonPlay' ).addEventListener('click', () => {
  if(webPage.mode != "ANIM") return false;
  webPage.paused = false;
  function timedPlayback () {
    if(!webPage.paused) {
      if(webPage.step < webPage.totalSteps) {
        webPage.objectDirector.updateVisuals(webPage.algorithm.tracks[webPage.step]);
        webPage.step += 1;
        setTimeout(timedPlayback, webPage.playbackSpeed);
      }
    } else {
      alert("Finished!");
    }
  }
  var playback = setTimeout(timedPlayback, webPage.playbackSpeed);
});
document.getElementById("playback").addEventListener("change", () => {
  webPage.playbackSpeed = 100 - document.getElementById("playback").value;
});
document.getElementById("buttonPause").addEventListener("click", () => {
  webPage.paused = !webPage.paused;
});
