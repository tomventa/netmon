/**
 * ----------------------------------------------
 * Authentication Module
 * ----------------------------------------------
 * This module is responsible for authentication.
 * ----------------------------------------------
 * @module auth
 * @requires api
 * @version 1.0.0
 * @author Tommaso Ventafridda
 * @license MIT
 * @date 2021-06-07 (yyyy-dd-mm)
 * @website https://github.com/tomventa/netmon
 * ----------------------------------------------
 */


/* Import API object */
import {api, apiBase} from './api.js'
/* Auth settings */
const renewBefore = 120; // 2 minutes before the token expires
const authPages = ["login", "register", "forgot", "logout"];

class Auth {
    constructor(check = true) {
        // Automatic check if needed
        if(check) this.check();
    }

    check(force = false) {
        // Default state: same as force state
        let check = force;
        // Check using last time check timestamp
        if (localStorage.getItem("authLogged") == undefined){
            check = true;
        } else if (localStorage.getItem("authLogged")==="false"){
            check = true;
        }else{
            let expire = localStorage.getItem("authExpire");
            let timestamp = Date.now() / 1000;
            if (timestamp >= parseInt(expire)) {
                check = true;
            }
        }
        // Update user cached data and recheck auth
        if (check) return this.updateMe();
        // Renew the token, if required
        this.renew();
        // Return true: auth is still valid
        return true;
    }

    renew(force = false){
        let toRenew = force;
        let timestamp = Date.now() / 1000;
        let expire = parseInt(localStorage.getItem("authExpire"));
        if (timestamp >= expire - renewBefore) {
            toRenew = true;
        }
        if (toRenew) {
            console.log("[Auth] Renewing token...");
            let response = api.call("auth/renew", {}, "GET");
            response.then(
                response => {
                    if ("access_token" in response){
                        localStorage.setItem(
                            "authExpire", 
                            this.getExpire(response.access_token).toString()
                        );
                        api.setBearer(response.access_token);
                        console.log("[Auth] Token renewed!");
                    }else{
                        console.log("[Auth] Token renewal failed!");
                    }
                }
            );
        }
    }

    updateMe() {
        // Check if logged
        let data = api.call("auth/me", {}, "GET");
        data.then(
            data => {
                // Update user data
                if (data.username != undefined) {
                    console.log("[Auth] Updated user data");
                    // Update user data
                    localStorage.setItem("authLogged", "true");
                    localStorage.setItem("authUsername", data.username);
                    localStorage.setItem("authTelegram", data.telegram);
                    localStorage.setItem("authFullName", data.full_name);
                    localStorage.setItem("authAdmin", data.admin.toString());
                } else if (this.isAuthPage() === false){
                    console.log("[Auth] Auth expired, redirecting...");
                    // Clear user data
                    this.setLogout();
                    // Rediret the user to the login page
                    window.location.replace("/login/");
                }
            }
        );
    }

    isAuthPage(){
        // Get current auth page, fixing common paths
        let page = window.location.pathname;
        page = page.replaceAll("/./", "");
        page = page.replaceAll("//", "/");
        page = page.replaceAll("/index.html", "/");
        page = page.replaceAll("/index", "/");
        if (page.endsWith("/"))   page = page.substring(0, page.length - 1);
        if (page.startsWith("/")) page = page.substring(1);

        // Check if current page is an auth page
        let ret = false
        authPages.forEach(pageName => {
            if(page==pageName) ret = true;
        });

        // In all other cases, return false
        return ret;
    }

    setLogout(){
        localStorage.clear();
        // localStorage.setItem("authExpire", "0");
        // localStorage.setItem("authLogged", "false");
        // localStorage.setItem("authAdmin", "false");
        // localStorage.setItem("authUsername", "false");
        // localStorage.setItem("authTelegram", "");
        // localStorage.setItem("authFullName", "Guest User");
    }

    
    async login(formData){
        let user = formData.username;
        let pwd = formData.password;
        let formStr = "username="+user+"&password="+pwd;
        let output = {
            "success": false,
            "message": "Unknown error detected!"
        }
        let response = await api.call_auth("auth/token", formStr);
        if ("access_token" in response){
            output["success"] = true;
            output["message"] = "Login successful!";
            api.setBearer(response.access_token);
            localStorage.setItem("jwt", response.access_token);
            localStorage.setItem(
                "authExpire", 
                this.getExpire(response.access_token).toString()
            );
        }else{
            output["message"] = response.detail;
        }
        return output;
    }

    getExpire(jwt){
        let jwt_parts = jwt.split(".");
        let jwt_payload = JSON.parse(atob(jwt_parts[1]));
        return jwt_payload.exp;
    }

    isLogged() {
        return localStorage.getItem("logged")==="true";
    }

    getUsername() {
        return localStorage.getItem("authUsername");
    }

    isAdmin() {
        return localStorage.getItem("authAdmin")==="true";
    }

    getApi(){
        return api;
    }
}

// Exporter
export var auth = new Auth();