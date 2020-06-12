nameSpaceURI = 'http://www.w3.org/2000/svg';

class AmoebotVizElements {
    /*
    SVG elements for visualising the particles on the grid
    */
   constructor( bot ) {
        this.bot = bot
        // DO:
        //      create head and tail elements and connect
        //      create representation objects and appendChild

        // NOTE: elements must be created in reverse order of visualization ie., 
        // create the tail first and head last so head is on top.

    }

    drawHead() {
        /*
        draw a standard particle head element as needed to stand on a point

        : returns : reference to the new element object
        */
        let newElement = document.createElementNS(nameSpaceURI, 'circle');
        return newElement;
    }

    drawTail() {
        /*
        draw a standard particle tail element as needed to stand on a point

        : returns : reference to the new element object
        */
        let newElement = document.createElementNS(nameSpaceURI, 'circle');
        return newElement;
    }

    drawTrace() {
        /*
        draw a standard particle trace element as needed to stand on a point

        : returns : reference to the new element object
        */
        let newElement = document.createElementNS(nameSpaceURI, 'circle');
        return newElement;
    }

}

class AmoebotVizTemplate {
    /*
    template representation for current state, contains reference to the SVG 
    elements object
    */

    constructor( head, tail ) {
        // FIX: correct for skew in tri-grid layout
        this.head = { x : head[ 0 ], y : head[ 1 ] };
        this.tail = { x : tail[ 0 ], y : tail[ 1 ] };

        // visualisation object
        this.vizObject = new AmoebotVizElements( this );
    }
}

class AmoebotVizTracker {
    /*
    mantains visual information and tracks current position of particles
    */

    constructor( tracks ) {
        // complete state history tracked
        this.tracks = tracks;

        // list of particle positions in single round
        this.botlist = [];
    }

    vizOneRound( round ) {
        this.botlist = this.tracks[ round ]
        // launch concurrent threads per particle in round DO:
        //      create a temporary AmoebotVizTemplate object
        //      
    }
}