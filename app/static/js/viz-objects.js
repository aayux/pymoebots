import { nameSpaceURI, unit, radius } from './config.js';


export function tri2Euclid(point) {
  const x = point[0] * unit * Math.sqrt(3) / 2;
  var y = unit * (point[1] - point[0] / 2)
  /*The y-coordinate of the point vertically translated onto line zero,
   *line zero is the line through the coordinate (0, 0)
   */
  const lineZeroPointY = x / Math.sqrt(3);
  /*Half the distance between the point and lineZeroPointY
   * moves it closer to line zero, causing 1/2 compression.
   */
  y += (lineZeroPointY - y) / 2;
  return {x, y};
}

export function shearPoint( point ) {
    // shear points from the Euclidean plane into the triangular grid
    var newPoint = { x : 0, y : 0 };
    newPoint.y += point[1] * unit;
    if ( point[0] % 2 == 1 ) { newPoint.y += ( 1 / 2 ) * unit; }
    newPoint.x += ( point[0] * Math.sqrt( 3 ) / 2 ) * unit;
    return( newPoint );
}


export class Amoebot {
  constructor(name, data, parentVisual) {
    this.name = name;
    this.parentVisual = parentVisual;
    this.location = data;
    this.visual = {
      head : this.createCircle(`H-B${ this.name }`, "head_pos"),
      tail : this.createCircle(`T-B${ this.name }`, "tail_pos"),
      body : this.createLine()
    }
  }

  createLine() {
    var lineElement = document.createElementNS(nameSpaceURI, 'line');
    const headPosition = tri2Euclid(this.location.head_pos)
    const tailPosition = tri2Euclid(this.location.tail_pos)
    lineElement.setAttribute('stroke', 'black' );
    lineElement.setAttribute('stroke-width', `${ radius / 2 }px`);
    lineElement.setAttribute('x1', headPosition.x);
    lineElement.setAttribute('x2', tailPosition.x);
    lineElement.setAttribute('y1', headPosition.y);
    lineElement.setAttribute('y2', tailPosition.y);
    this.parentVisual.appendChild(lineElement);
    return lineElement;
  }

  createCircle(name, segment) {
    var vizElement = document.createElementNS( nameSpaceURI, 'circle' );
    var position = tri2Euclid(this.location[segment]);
    vizElement.setAttribute( 'cx', position.x );
    vizElement.setAttribute( 'cy', position.y );
    vizElement.setAttribute( 'fill', 'white' );
    vizElement.setAttribute( 'r', `${ radius }px` );
    vizElement.setAttribute( 'stroke', 'black' );
    vizElement.setAttribute( 'stroke-width', `${ radius / 3 }px` );
    this.parentVisual.appendChild(vizElement)
    return vizElement;
  }

  updateVisuals(where) {
    const headPosition = tri2Euclid(where["head_pos"])
    const tailPosition = tri2Euclid(where["tail_pos"])
    this.visual.head.setAttribute('cx', headPosition.x);
    this.visual.head.setAttribute('cy', headPosition.y);
    this.visual.body.setAttribute('x1', headPosition.x);
    this.visual.body.setAttribute('y1', headPosition.y);
    this.visual.tail.setAttribute('cx', tailPosition.x);
    this.visual.tail.setAttribute('cy', tailPosition.y);
    this.visual.body.setAttribute('x2', tailPosition.x);
    this.visual.body.setAttribute('y2', tailPosition.y);
  }
}


export class Wall {
  constructor(name, data, parentVisual) {
    this.name = name;
    this.parentVisual = parentVisual;
    this.position = data;
    this.visual = this.createCircle(`H-B${ this.name }`);
  }

  createCircle(name) {
    var vizElement = document.createElementNS( nameSpaceURI, 'circle' );
    const position = tri2Euclid(this.position)
    vizElement.setAttribute( 'cx', position.x );
    vizElement.setAttribute( 'cy', position.y );
    vizElement.setAttribute( 'fill', 'red' );
    vizElement.setAttribute( 'r', `${ radius }px` );
    vizElement.setAttribute( 'stroke', 'black' );
    vizElement.setAttribute( 'stroke-width', `${ radius / 3 }px` );
    this.parentVisual.appendChild(vizElement)
    return vizElement;
  }
}
