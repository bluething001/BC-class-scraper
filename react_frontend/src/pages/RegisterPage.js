import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function RegisterPage() {
    const [createdUsername, setUsername] = useState("");
    const [createdPassword, setPassword] = useState("");
    const [confirmedPassword, setConfPassword] = useState("");
    const [userEmail, setEmail] = useState("");
    const [BCusername, setBCusername] = useState("");
    const [BCpassword, setBCpassword] = useState("");
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const handleAddClass = async (e) => {
        setLoading(true);
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:8000/register/", {
                createdUsername,
                createdPassword,
                confirmedPassword,
                userEmail,
                BCusername,
                BCpassword,
            });
            alert(response.data.message); // Display success message
            navigate("/login");
        } catch (error) {
            if (error.response && error.response.data) {
                alert(error.response.data.message); // Display error message
            } else {
                alert("An unexpected error occurred.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <form>
                <h1>Register an account to use the BC class availibility checker!</h1>
                <div style={{ padding: "20px", maxWidth: "500px", margin: "auto" }}>
                    <div style={{ marginBottom: "10px" }}>
                    <label style={{ display: "block", marginBottom: "5px" }}>
                        Create a Username
                    </label>
                        <input
                            type="text"
                            value={createdUsername}
                            onChange={(e) => setUsername(e.target.value)}
                            style={{ width: "100%", padding: "8px" }}
                        />
                    </div>
                    
                    <div style={{ marginBottom: "10px" }}>
                        <label style={{ display: "block", marginBottom: "5px" }}>
                            Create a Password
                        </label>
                        <input
                            type="password"
                            value={createdPassword}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{ width: "100%", padding: "8px" }}
                        />
                    </div>

                    <div style={{ marginBottom: "10px" }}>
                        <label style={{ display: "block", marginBottom: "5px" }}>
                            Confirm Password
                        </label>
                        <input
                            type="password"
                            value={confirmedPassword}
                            onChange={(e) => setConfPassword(e.target.value)}
                            style={{ width: "100%", padding: "8px" }}
                        />
                    </div>
                    
                    <div style={{ marginBottom: "10px" }}>
                        <label style={{ display: "block", marginBottom: "5px" }}>
                            Email to recieve notifications
                        </label>
                        <input
                            type="text"
                            value={userEmail}
                            onChange={(e) => setEmail(e.target.value)}
                            style={{ width: "100%", padding: "8px" }}
                        />
                    </div>

                    <div style={{ marginBottom: "10px" }}>
                        <label style={{ display: "block", marginBottom: "5px" }}>
                            BC Username
                        </label>
                        <input
                            type="text"
                            value={BCusername}
                            onChange={(e) => setBCusername(e.target.value)}
                            style={{ width: "100%", padding: "8px" }}
                        />
                    </div>
                    
                    <div style={{ marginBottom: "10px" }}>
                        <label style={{ display: "block", marginBottom: "5px" }}>
                            BC Password
                        </label>
                        <input
                            type="password"
                            value={BCpassword}
                            onChange={(e) => setBCpassword(e.target.value)}
                            style={{ width: "100%", padding: "8px" }}                        />
                    </div>
                </div>
                
                <button onClick={handleAddClass}>
                    Register
                </button>
                <button onClick={() => navigate("/login")}>
                    Back to Login
                </button>
            </form>
            {loading && (
                <div
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: "100%",
                        backgroundColor: "rgba(0, 0, 0, 0.5)",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        zIndex: 1000,
                        color: "#fff",
                        fontSize: "24px",
                    }}
                >
                    Registering...
                </div>
            )}
        </div>
    );
}

export default RegisterPage;