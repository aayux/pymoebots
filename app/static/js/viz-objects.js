import { nameSpaceURI, unit, radius } from './config.js';


export function tri2Euclid(point) {
  return { x: point.x * unit * Math.sqrt(3) / 2, y: unit * (point.y + point.x / 2)};
}


export class Amoebot {
  constructor(name, data) {
    this.name = name;
    this.segment = {
      head : {x:data[0], y:data[1]},
      tail : {x:data[0], y:data[1]}
    }
    this.visual = {
      head : this.createCircle(`H-B${ this.name }`),
      tail : this.createCircle(`T-B${ this.name }`),
      body : this.createLine()
    }
  }

  createLine() {
    lineElement = document.createElementNS(nameSpaceURI, 'line');
    const headPosition = tri2Euclid(this.segment.head)
    const tailPosition = tri2Euclid(this.segment.tail)
    lineElement.setAttribute('stroke', 'black' );
    lineElement.setAttribute('stroke-width', `${ radius / 2 }px`);
    lineElement.setAttribute('x1', headPosition.x);
    lineElement.setAttribute('x2', tailPosition.x);
    lineElement.setAttribute('y1', headPosition.y);
    lineElement.setAttribute('y2', tailPosition.y);
    amoeBotsDOM.appendChild(lineElement);
    return lineElement;
  }

  createCircle(name) {
    var vizElement = document.createElementNS( nameSpaceURI, 'circle' );
    const position = tri2Euclid(this.point)
    vizElement.setAttribute( 'cx', position.x );
    vizElement.setAttribute( 'cy', position.y );
    vizElement.setAttribute( 'fill', 'white' );
    vizElement.setAttribute( 'r', `${ radius }px` );
    vizElement.setAttribute( 'stroke', 'black' );
    vizElement.setAttribute( 'stroke-width', `${ radius / 3 }px` );
    amoebotsDOM.appendChild(vizElement)
    return vizElement;
  }

  updateVisuals() {
    const headPosition = tri2Euclid(this.segment.head)
    const tailPosition = tri2Euclid(this.segment.tail)
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
  constructor(name, data) {
    this.name = name;
    this.x = data[0];
    this.y = data[1];
    this.visual = this.createCircle(`H-B${ this.name }`);
  }

  createCircle(name) {
    var vizElement = document.createElementNS( nameSpaceURI, 'circle' );
    const position = tri2Euclid(this.point)
    vizElement.setAttribute( 'cx', position.x );
    vizElement.setAttribute( 'cy', position.y );
    vizElement.setAttribute( 'fill', 'red' );
    vizElement.setAttribute( 'r', `${ radius }px` );
    vizElement.setAttribute( 'stroke', 'black' );
    vizElement.setAttribute( 'stroke-width', `${ radius / 3 }px` );
    amoebotsDOM.appendChild(vizElement)
    return vizElement;
  }
}
