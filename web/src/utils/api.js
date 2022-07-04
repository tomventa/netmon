/**
 * ----------------------------------------------
 * API Module
 * ----------------------------------------------
 * This module is responsible for all API calls.
 * It is also responsible for the authentication.
 * ----------------------------------------------
 * @module api
 * @version 1.0.0
 * @author Tommaso Ventafridda
 * @license MIT
 * @date 2021-04-07 (yyyy-dd-mm)
 * @website https://github.com/tomventa/netmon
 * ----------------------------------------------
 */

/*
 * This is a VITE env variable
 * https://vitejs.dev/guide/env-and-mode.html
*/
const IS_PRODUCTION = import.meta.env.PROD

/**
 * Api endpoint url
 */
export const apiBase = IS_PRODUCTION ?
    '/api/' :
    'http://localhost:8000/api/'

class Api{
    constructor(base) {
        this.base = base;
        this.random = Math.floor(Math.random() * 100) + 1;
    }

    getSeed(){
        return this.random;
    }

    async call(url, data, method = 'GET') {
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
        headers.append('Accept', 'application/json');
        headers.append('X-Auth-Token', localStorage.getItem('token'));
        let options = {
            method: method,
            headers: headers,
            body: JSON.stringify(data)
        };
        let response = await fetch(this.base + url, options);
        let json = await response.json();
        return json;
    }
}

export var api = new Api(apiBase);