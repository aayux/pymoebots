async function request( url, params, method = 'GET' ) {

    const options = {
        method,
        headers: {
            'Content-Type' : 'application/json'
        }
    };

    // if params exists and method is GET, add query string to url
    // otherwise, just add params as a "body" property to the options object
    if ( params ) {
        if ( method === 'GET' ) {
            url += '?' + objectToQueryString( params );
      } else {
            // body should match Content-Type in headers option
            options.body = JSON.stringify( params );
      }
    }

    const response = await fetch( url, options );
    const result = await response.json();

    return result;
}

function objectToQueryString( obj ) {
    return Object.keys( obj ).map( key => key + '=' + obj[ key ] ).join( '&' );
}


//methods that are currently legal?
const legalMethods = new Set(["GET", "POST", "PUT", "DELETE"])

//Request url with parameter and legal method
export function sendRequest(url, params, method="GET") {
  if(legalMethods.has(method)) {
    return request(url, params, method);
  }
}
