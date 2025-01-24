import React, { useState } from "react";
import axios from "axios";
function ScrapingPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [className, setClassName] = useState("");
    const [section, setSection] = useState("");
    const [classes, setClasses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [expanded, setExpanded] = useState([]); // Tracks expanded classes
    const [showHelpText, setShowHelpText] = useState(false);

    const handleAddClass = async () => {
        setLoading(true);
        try {
            const response = await axios.post("http://127.0.0.1:8000/get_class_data/", {
                username,
                password,
                class_name: className,
                section: parseInt(section),
            });

            const classdata = response.data.classdata;
            setClasses([
                ...classes,
                {
                    name: classdata.class_name ?? className,
                    instructors: classdata.instructors ?? [],
                    availableSeats: classdata.available_seats ?? "Unknown",
                    schedule: classdata.schedule ?? [],
                },
            ]);
        } catch (error) {
            console.error("Error starting scraper:", error);
            alert("Failed to add class. Check console for details.");
        } finally {
            setLoading(false);
        }
    };

    const handleRemoveClass = (index) => {
        const updatedClasses = classes.filter((_, i) => i !== index);
        setClasses(updatedClasses);
        setExpanded((prev) => prev.filter((_, i) => i !== index));
    };

    const toggleExpand = (index) => {
        if (expanded.includes(index)) {
            setExpanded(expanded.filter((i) => i !== index));
        } else {
            setExpanded([...expanded, index]);
        }
    };

    return (
        <div style={{ padding: "20px", maxWidth: "500px", margin: "auto" }}>
            <h1>Class Scraper</h1>
            <div style={{ marginBottom: "10px" }}>
                <label>BC Username:</label>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={{width: "97%" }}
                />
            </div>
            <div style={{ marginBottom: "10px" }}>
                <label>BC Password:</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{width: "97%" }}
                />
            </div>
            <div style={{ marginBottom: "10px" }}>
                <div style={{ display: "flex", alignItems: "center" }}>
                <label style={{ marginRight: "auto", fontSize: "16px", fontWeight: "bold" }}>
                    Class Details:
                </label>
                <button
                    onClick={() => setShowHelpText(!showHelpText)}
                    style={{
                    backgroundColor: "#007BFF",
                    color: "#fff",
                    border: "none",
                    padding: "5px 10px",
                    borderRadius: "4px",
                    cursor: "pointer",
                    fontSize: "14px",
                    marginLeft: "10px",
                    }}
                >
                    Having trouble adding a class?
                </button>
                </div>
                {showHelpText && (
                <div
                    style={{
                    marginTop: "10px",
                    backgroundColor: "#f8f9fa",
                    padding: "10px",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                    color: "#333",
                    fontSize: "14px",
                    }}
                >
                    If there is a failed to add class error, or the class added is not what you intended, ensure that when searching the class in the search courses tab on the registration page, the first class that appears is your intended class. If the full course name does not achieve this, a workaround is to copy a portion of the class description and paste it into the search bar/class name box.
                </div>
                )}
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
                <button onClick={handleAddClass} className="add-class-button">
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
                            flexDirection: "column",
                            border: "1px solid #ccc",
                            padding: "10px",
                            marginBottom: "10px",
                            backgroundColor: cls.availableSeats > 0 ? "#d4edda" : "#f8d7da",
                        }}
                    >
                        <div>
                            <strong>Class Name:</strong> {cls.name}
                        </div>
                        <button
                            onClick={() => toggleExpand(index)}
                            style={{
                                marginTop: "10px",
                                alignSelf: "flex-start",
                                backgroundColor: "#007BFF",
                                color: "#fff",
                                padding: "5px 10px",
                                border: "none",
                                cursor: "pointer",
                            }}
                        >
                            {expanded.includes(index) ? "Hide Details" : "Show Details"}
                        </button>
                        {expanded.includes(index) && (
                            <div>
                                <div>
                                    <strong>Instructors:</strong>
                                    <ul style={{ paddingLeft: "20px", marginTop: "5px" }}>
                                        {cls.instructors.map((instructor, i) => (
                                            <li key={i}>{instructor}</li>
                                        ))}
                                    </ul>
                                </div>
                                <div>
                                    <strong>Available Seats:</strong>{" "}
                                    {Array.isArray(cls.availableSeats)
                                        ? cls.availableSeats.join(", ")
                                        : cls.availableSeats}
                                </div>
                                <div>
                                    <strong>Schedule:</strong>
                                    <ul style={{ paddingLeft: "20px", marginTop: "5px" }}>
                                        {cls.schedule.map((time, i) => (
                                            <li key={i}>{time}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}
                        <button
                            onClick={() => handleRemoveClass(index)}
                            style={{
                                marginTop: "10px",
                                alignSelf: "flex-end",
                                backgroundColor: "#dc3545",
                                color: "#fff",
                                padding: "5px 10px",
                                border: "none",
                                cursor: "pointer",
                            }}
                        >
                            Remove
                        </button>
                    </li>
                ))}
            </ul>
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
                    Adding Class... (This may take around half a minute or longer depending on the checker's traffic)
                </div>
            )}
        </div>
    );
}
export default ScrapingPage;