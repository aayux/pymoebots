import {nameSpaceURI, unit} from './config.js';

// TODO :: re-write for vertical anchor grid
export function shearPoint( point ) {
    // shear points from the Euclidean plane into the triangular grid
    var newPoint = { x : 0, y : 0 };
    newPoint.y += point.y * unit;
    if ( point.x % 2 == 1 ) { newPoint.y += ( 1 / 2 ) * unit; }
    newPoint.x += ( point.x * Math.sqrt( 3 ) / 2 ) * unit;
    return( newPoint );
}

class AmoebotVizElements {
    /*
    <g> SVG elements for visualising the particles on the grid
    */
   constructor( data ) {
        // object of class AmoebotVizTemplate 
        this.bot_data = data
        this.bot_id = data.bot_id
        
        // create head and tail elements and connect
        // create representation objects and append

        // SVG element group
        this.vizObject = document.createElementNS( nameSpaceURI, 'g' );
        this.vizObject.setAttribute( 'class', 'amoebot' );
        this.vizObject.setAttribute( 'name', `B${this.bot_id}` );

        this.botHead = this.drawHead( this.bot_id );
        this.botTail = this.drawTail( this.bot_id , this.botHead );

        camera.getElementById( 'amoebots' ).appendChild( this.vizObject );

        // updateViz();
    }

    drawHead( bot_id ) {
        /*
        draw a standard particle head element to stand on a point

        : returns : reference to the new element object
        */
        let newElement = document.createElementNS( nameSpaceURI, 'circle' );
        newElement.setAttribute( 'name', `H-B${bot_id}` );
        
        
        // locate on the triangualr grid
        const position = shearPoint(
                            {
                                x : this.bot_data.head.x, 
                                y : this.bot_data.head.y
                            }
                        );
        
        newElement.setAttribute( 'cx', position.x );
        newElement.setAttribute( 'cy', position.y );
        newElement.setAttribute( 'fill', 'black' );
        newElement.setAttribute( 'r', `${pixels}px` );
        
        // add to SVG group
        this.vizObject.appendChild( newElement );
        
        // return a reference
        return newElement;
    }

    drawTail( bot_id, botHead ) {
        /*
        draw a standard particle tail element to stand on a point, and draw
        the connecting line from head to tail (if they are not the same).

        : returns : reference to the new element object
        */
       let newElement = document.createElementNS( nameSpaceURI, 'circle' );
       newElement.setAttribute( 'name', `T-B${bot_id}` );
       
       
       // locate on the triangualr grid
       const position = shearPoint(
                           {
                               x : this.bot_data.tail.x, 
                               y : this.bot_data.tail.y
                           }
                       );
       
        newElement.setAttribute( 'cx', position.x );
        newElement.setAttribute( 'cy', position.y );
        newElement.setAttribute( 'fill', 'black' );
        newElement.setAttribute( 'r', `${pixels}px` );
       
       // TODO :: check if head and tail are same, if not draw a line element
       
       // add to SVG group
       this.vizObject.appendChild( newElement );
       
       // return a reference
       return newElement;
    }

    drawTrace() {
        /*
        draw a standard particle trace element as needed to stand on a point

        : returns : reference to the new element object
        */
        let newElement = document.createElementNS( nameSpaceURI, 'circle' );
        return;
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

    update() {
        // update status
        return undefined;
    }
}

class AmoebotVizInit {
    /*
    mantains visual information and tracks current position of particles
    */

    constructor( config0, tracks ) {
        // starting configuration of the system
        this.config0 = config0;

        // motion history tracker
        this.tracks = tracks;

        // step of simulation
        this.step = 0;

        // dictionary of particle positions on triangular grid
        this.bot_dict = [];

        for ( let bot_id in this.config0 ) {
            this.bot_dict.push(
                new AmoebotVizTemplate(
                    bot_id,
                    this.config0[ bot_id ].head_pos,
                    this.config0[ bot_id ].tail_pos
                )
            );
        }

        placeBotsOnGrid();
    }

    placeBotsOnGrid() {

        // get positions on the triangular grid
        for ( let bot_id in this.config0 ) {
            var bot = this.bot_dict[bot_id];
            bot.update();
        }

        // updateViz();
    }
}

class AmoebotVizTracker extends AmoebotVizInit{
    /*
    extends initializer class and provides step-wise execution capability
    */

    getConfigInfo() {
        var nBots = this.config0.length;
        var nSteps = this.tracks.length;
        return([nBots, nSteps]);
    }

    vizOneStep( step ) {
        // one step is one bot movement
        var track = this.tracks[ step ];
        this.bot_id = track.move_bot;
        var bot = this.bot_dict[ this.bot_id ];
        bot = new AmoebotVizTemplate(
                                        this.bot_id,
                                        track.config.head_pos,
                                        track.config.tail_pos
                                    );
        bot.update();   // NOTE :: is this operation in place? we still need to delete old position

        // updateViz();

    }
}
