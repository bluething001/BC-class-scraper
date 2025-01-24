import React from "react";
import { Link } from "react-router-dom";
import "./LoginPage.css"; // Import the CSS file

function LoginPage() {
    return (
        <div>
            <form>
                <h1>BC Class Checker Login</h1>
                <input type="text" placeholder="Username" /> 
                <input type="password" placeholder="Password" />
                <button type="submit">Login</button>
                <Link to="/register">Don't have an account? Register here!</Link>
            </form>
        </div>
    );
}

export default LoginPage;