/* Import API object */
import {api} from './api.js'
/* Auth settings */
const checkTimer = 3600; // 1 hour
const authPages = ["login", "register", "forgot", "logout"];

class Auth {
    constructor(check = true) {
        // Automatic check if needed
        if(check) this.check();
    }

    check(force = false) {
        // Default state: same as force state
        let toCheck = force;
        // Check using last time check timestamp
        if (localStorage.getItem("authLastCheck") == undefined){
            toCheck = true;
        }else if(localStorage.getItem("logged")==="false"){
            toCheck = true;
        }else{
            let lastCheck = localStorage.getItem("authLastCheck");
            let timestamp = Date.now() / 1000;
            if (timestamp - parseInt(lastCheck) > checkTimer) {
                toCheck = true;
            }
        }
        // Check if needed, and return the result
        if (toCheck) return this._check();
        // Return true: auth is still valid
        return true;
    }

    _check() {
        // Check if logged
        let data = api.call("auth/me", {}, "GET");
        data.then(
            data => {
                // Update last check timestamp
                let timestamp = Date.now() / 1000;
                localStorage.setItem("authLastCheck", timestamp.toString());
                // Update user data
                if (data.auth === true) {
                    console.log("[Auth] API check: auth is valid");
                    // Update user data
                    localStorage.setItem("logged", "true");
                    localStorage.setItem("username", data.username);
                    localStorage.setItem("role", data.role);
                    localStorage.setItem("userEssential", data.essential.toString());
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

        //return true;
        // Check if current page is an auth page
        let ret = false
        authPages.forEach(pageName => {
            if(page==pageName) ret = true;
        });

        // In all other cases, return false
        console.log("[Auth] Current page is not an auth page", page);
        return ret;
    }

    setLogout(){
        localStorage.setItem("logged", "false");
        localStorage.setItem("role", "guest");
        localStorage.setItem("userEssential", "false");
        localStorage.setItem("username", "Guest");
    }

    setLogin(username, password){
        
    }

    isLogged() {
        return localStorage.getItem("logged")==="true";
    }

    getUsername() {
        return localStorage.getItem("username");
    }

    getRole() {
        return localStorage.getItem("role");
    }

    getUserEssential() {
        return localStorage.getItem("userEssential")==="true";
    }
}

// Exporter
export var auth = new Auth();