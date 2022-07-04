import {api} from './api.js'
/* Get environment information */
let logged = localStorage.getItem("logged");
let lastCheck = localStorage.getItem("authLastCheck");
let page = window.location.pathname;
let timestamp = Date.now() / 1000;
let checkTimer = 3600; // 1 hour
let apiEndPoint = "http://localhost:8000/api/"

console.log(api.getSeed())


/* Redirect if not in already in login page */
let isLoginPage = page.replaceAll("/", "") === "login";
if (logged !== "true" && isLoginPage == false) {
    console.log("[Auth] You are not logged, redirecting...")
    window.location.replace("/login/");
} else if (isLoginPage && logged) {
    console.log("[Auth] You are already logged, redirecting...")
    window.location.replace("/");
}

/* Check last Auth check via API */
if (1 == 1 || lastCheck != undefined && (timestamp - parseInt(lastCheck)) > checkTimer) {
    console.log("[Auth] Last check was more than 1 hour ago, checking API...")
    fetch(apiEndPoint + "auth/me").then(response => response.json()).then(
        data => {
            if (data.auth === true) {
                console.log("[Auth] API confirmed: auth is still valid")
                localStorage.setItem("authLastCheck", timestamp.toString());
                localStorage.setItem("username", data.username);
                localStorage.setItem("capitalizeUsername", data.capitalize.toString());
                localStorage.setItem("role", data.role);
                localStorage.setItem("userEssential", data.essential.toString());
            } else {
                console.log("[Auth] Auth expired confirmed by API, redirecting...");
                localStorage.setItem("logged", "false");
                window.location.replace("/login/");
            }
        }
    );
}

/* Resolve current username (using capitalize preference)*/
let username = localStorage.getItem("username");
if (localStorage.getItem("userCapitalize") == "true") {
    username = username.charAt(0).toUpperCase() + username.slice(1);
}