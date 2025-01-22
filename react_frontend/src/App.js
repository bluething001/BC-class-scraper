import React, { useState } from "react";
import './App.css';

function App() {
    // State management for inputs and list
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [className, setClassName] = useState("");
    const [section, setSection] = useState("");
    const [classes, setClasses] = useState([]);

    // Handlers
    const handleAddClass = () => {
        if (className.trim() && section.trim()) {
            // Combine class name and section into one entry
            setClasses([...classes, { name: className, section }]);
            setClassName(""); // Clear Class Name input field
            setSection("");   // Clear Section input field
        }
    };

    const handleRemoveClass = (index) => {
        const updatedClasses = classes.filter((_, i) => i !== index);
        setClasses(updatedClasses);
    };

    const handleStartScraper = () => {
        alert("Scraper started!");
    };

    const handleStopScraper = () => {
        alert("Scraper stopped!");
    };

    return (
        <div style={{ padding: "20px", maxWidth: "500px", margin: "auto" }}>
            <h1>Class Scraper</h1>
            <div style={{ marginBottom: "10px" }}>
                <label>Username:</label>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={{ marginLeft: "10px", width: "100%" }}
                />
            </div>
            <div style={{ marginBottom: "10px" }}>
                <label>Password:</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ marginLeft: "10px", width: "100%" }}
                />
            </div>
            <div style={{ marginBottom: "10px" }}>
                <label style={{ display: "block", marginBottom: "5px" }}>Class Details:</label>
                <div style={{ display: "flex", gap: "10px" }}>
                    <input
                        type="text"
                        placeholder="Class Name"
                        value={className}
                        onChange={(e) => setClassName(e.target.value)}
                        style={{ flex: 1 }}
                    />
                    <input
                        type="text"
                        placeholder="Section"
                        value={section}
                        onChange={(e) => setSection(e.target.value)}
                        style={{ flex: 1 }}
                    />
                    <button onClick={handleAddClass} style={{ marginLeft: "10px" }}>
                        Add
                    </button>
                </div>
            </div>
            <ul style={{ listStyleType: "none", padding: "0" }}>
                {classes.map((cls, index) => (
                    <li
                        key={index}
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            border: "1px solid #ccc",
                            padding: "5px",
                            marginBottom: "5px",
                        }}
                    >
                        <span>
                            <strong>Class:</strong> {cls.name} - <strong>Section:</strong> {cls.section}
                        </span>
                        <button onClick={() => handleRemoveClass(index)}>Remove</button>
                    </li>
                ))}
            </ul>
            <div style={{ marginTop: "20px" }}>
                <button onClick={handleStartScraper} style={{ marginRight: "10px" }}>
                    Start Scraper
                </button>
                <button onClick={handleStopScraper}>Stop Scraper</button>
            </div>
        </div>
    );
}

export default App;