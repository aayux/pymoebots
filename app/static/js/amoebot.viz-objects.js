import { nameSpaceURI, unit, pixels } from './config.js';

const amoebotsDOM = camera.getElementById( 'amoebots' );

export function shearPoint( point ) {
    // shear points from the Euclidean plane into the triangular grid
    var newPoint = { x : 0, y : 0 };
    newPoint.y += point.y * unit;
    if ( point.x % 2 == 1 ) { newPoint.y += ( 1 / 2 ) * unit; }
    newPoint.x += ( point.x * Math.sqrt( 3 ) / 2 ) * unit;
    return( newPoint );
}

export function addAmoebot( x, y , i) {
    /* 
    add amoebots to the grid
    */
    // create a new visual template object
    var bot = new AmoebotVizTemplate( i, [x, y], [x, y] );

    // update bot status
    // bot.update()

}

class WallVizElements {
    /*
    <g> SVG elements for visualising the particles on the grid
    */
   constructor( data ) {
        // object of class AmoebotVizTemplate 
        this.wall_data = data
        this.wall = data.wall

        // SVG element group
        this.vizObject = document.createElementNS( nameSpaceURI, 'g' );
        this.vizObject.setAttribute( 'class', 'wall' );
    }

    drawElements() {
        // ...
        this.vizWall = this.drawWall();
        camera.getElementById( 'amoebots' ).appendChild( this.vizObject );
    }

    drawWall() {
        /*
        draw a standard particle head element to stand on a point

        : returns : reference to the new element object
        */
        var vizElement = document.createElementNS( nameSpaceURI, 'circle' );
        vizElement.setAttribute( 'name', `W${ this.wall }` );

        // locate on the triangualr grid
        const position = shearPoint(
                            {
                                x : this.wall_data.x, 
                                y : this.wall_data.y
                            }
                        );
        
        vizElement.setAttribute( 'cx', position.x );
        vizElement.setAttribute( 'cy', position.y );
        vizElement.setAttribute( 'fill', 'red' );
        vizElement.setAttribute( 'r', `${ pixels }px` );
        vizElement.setAttribute( 'stroke', 'black' );
        vizElement.setAttribute( 'stroke-width', `${ pixels / 3 }px` );

        // add to SVG group
        this.vizObject.appendChild( vizElement );
        
        // return a reference
        return vizElement;
    }
}

class AmoebotVizElements {
    /*
    <g> SVG elements for visualising the particles on the grid
    */
   constructor( data ) {
        // object of class AmoebotVizTemplate 
        this.bot_data = data
        this.bot_id = data.bot_id

        // SVG element group
        this.vizObject = document.createElementNS( nameSpaceURI, 'g' );
        this.vizObject.setAttribute( 'class', 'amoebot' );
        this.vizObject.setAttribute( 'name', `B${ this.bot_id }` );
    }

    drawElements() {
        // create head and tail elements and connect
        // create representation objects and append
        this.vizBotH = this.drawHead();
        this.vizBotT = this.drawTail();

        camera.getElementById( 'amoebots' ).appendChild( this.vizObject );
    }

    drawHead() {
        /*
        draw a standard particle head element to stand on a point

        : returns : reference to the new element object
        */
        var vizElement = document.createElementNS( nameSpaceURI, 'circle' );
        vizElement.setAttribute( 'name', `H-B${ this.bot_id }` );
        
        
        // locate on the triangualr grid
        const position = shearPoint(
                            {
                                x : this.bot_data.head.x, 
                                y : this.bot_data.head.y
                            }
                        );
        
        vizElement.setAttribute( 'cx', position.x );
        vizElement.setAttribute( 'cy', position.y );
        vizElement.setAttribute( 'fill', 'white' );
        vizElement.setAttribute( 'r', `${ pixels }px` );
        vizElement.setAttribute( 'stroke', 'black' );
        vizElement.setAttribute( 'stroke-width', `${ pixels / 3 }px` );

        // add to SVG group
        this.vizObject.appendChild( vizElement );
        
        // return a reference
        return vizElement;
    }

    drawTail() {
        /*
        draw a standard particle tail element to stand on a point, and draw
        the connecting line from head to tail (if they are not the same).

        : returns : reference to the new element object
        */
       var vizElement = document.createElementNS( nameSpaceURI, 'circle' );
       vizElement.setAttribute( 'name', `T-B${ this.bot_id }` );
       
       
       // locate on the triangualr grid
       const position = shearPoint(
                           {
                               x : this.bot_data.tail.x, 
                               y : this.bot_data.tail.y
                           }
                       );
       
        vizElement.setAttribute( 'cx', position.x );
        vizElement.setAttribute( 'cy', position.y );
        vizElement.setAttribute( 'fill', 'black' );
        vizElement.setAttribute( 'r', `${ 3 * pixels / 4 }px` );

        // add to SVG group
        this.vizObject.appendChild( vizElement );

        // check if head and tail are same, if not draw a line element

        var xHead = this.vizBotH.getAttribute( 'cx' );
        var yHead = this.vizBotH.getAttribute( 'cy' );

        this.lineElement = document.createElementNS( nameSpaceURI, 'line' );
        this.lineElement.setAttribute( 'stroke', 'black' );
        this.lineElement.setAttribute( 'stroke-width', `${ pixels / 2 }px` );

        if ( position.x != xHead || position.y != yHead ) {
            this.lineElement.setAttribute( 'x1', position.x );
            this.lineElement.setAttribute( 'x2', xHead );
            this.lineElement.setAttribute( 'y1', position.y );
            this.lineElement.setAttribute( 'y2', yHead );
       }

       this.vizObject.appendChild( this.lineElement );

       // return a reference
       return vizElement;
    }
}

class WallVizTemplate {
    /*
    template representation for current state, contains reference to the SVG 
    elements object
    */

    constructor( wall, point) {
        // unique identifier usefuol for vizualisation
        this.wall = wall

        // correct for skew in tri-grid layout
        this.x = point[ 0 ], 
        this.y = (point[ 1 ] % 2 == 0 ) ? point[ 1 ] / 2 : ( point[ 1 ] - 1 ) / 2

        // visualisation object
        this.vizObject = new WallVizElements( this );
    }
}

class AmoebotVizTemplate {
    /*
    template representation for current state, contains reference to the SVG 
    elements object
    */

    constructor( bot_id, head, tail) {
        // unique identifier usefuol for vizualisation
        this.bot_id = bot_id

        // correct for skew in tri-grid layout
        this.head = { 
            x : head[ 0 ], 
            y : ( head[ 1 ] % 2 == 0 ) ? head[ 1 ] / 2 : ( head[ 1 ] - 1 ) / 2
        };
        
        this.tail = { 
            x : tail[ 0 ], 
            y : ( tail[ 1 ] % 2 == 0 ) ? tail[ 1 ] / 2 : ( tail[ 1 ] - 1 ) / 2
        };

        // visualisation object
        this.vizObject = new AmoebotVizElements( this );
    }
}

class AmoebotVizInit {
    /*
    mantains visual information and tracks current position of particles
    */

    constructor( config0, tracks ) {
        // starting configuration of the system
        this.config0_bots = this.init_b = config0[ 'bots' ];
        this.config0_walls = this.init_w = config0[ 'walls' ];

        // motion history tracker
        this.tracks = tracks;

        this.placeBotsOnGrid();
        this.placeWallsOnGrid();

    }

    placeBotsOnGrid() {

        // list of particle positions on triangular grid
        this.bot_list = [];

        // clear all svg objects
        amoebotsDOM.innerHTML = '';

        for( let bot_id in this.init_b ) {
            this.bot_list.push(
                new AmoebotVizTemplate(
                    bot_id,
                    this.init_b[ bot_id ], 
                    this.init_b[ bot_id ]
                )
            );

            this.bot_list[ bot_id ].vizObject.drawElements();
        }
    }

    moveBotsOnGrid() {

        // list of particle positions on triangular grid
        this.bot_list = [];

        // clear all svg objects
        amoebotsDOM.innerHTML = '';

        for( let bot_id in this.init_b ) {
            this.bot_list.push(
                new AmoebotVizTemplate(
                    bot_id,
                    this.init_b[ bot_id ].head_pos, 
                    this.init_b[ bot_id ].tail_pos
                )
            );

            this.bot_list[ bot_id ].vizObject.drawElements();
        }
    }

    placeWallsOnGrid() {
        // 
        this.wall_list = [];

        for( let wall in this.init_w ) {
            this.wall_list.push(
                new WallVizTemplate(
                    wall,
                    this.init_w[ wall ]
                )
            );

            this.wall_list[ wall ].vizObject.drawElements();
        }
    }
}

export class AmoebotVizTracker extends AmoebotVizInit{
    /*
    extends initializer class and provides step-wise execution capability
    */

    getConfigInfo() {
        var nBots = this.config0_bots.length;
        var nWalls = this.config0_walls.length;
        var nSteps = this.tracks.length;
        return( [ nBots, nSteps ] );
    }

    vizOneStep( step ) {
        // one step is one bot movement
        this.init_b = this.tracks[ step ];

        this.moveBotsOnGrid();
        this.placeWallsOnGrid();
        // bot.update();
        // updateViz();
        return 1;
    }
}
