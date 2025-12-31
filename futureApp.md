Agent Identity
Name: react-native-jail-client

Role: Remote Media Interface & Stream Handler

Focus: Port 8000 Proxy Interaction & Native Buffer Management

Client Architecture OverView
The app is designed as a lightweight stateless interface that mirrors the server’s directory state while enforcing local security protocols (HTTPS/Cleartext validation).

1. Networking Strategy (The "Bridge")
Endpoint Target: All traffic is routed through a single BASE_URL (Port 8000).

Network Discovery:

Local Development: Targets IP-specific LAN addresses (e.g., 192.168.x.x).

Production Logic: Designed to handle dynamic IP shifts via manual configuration or mDNS.

Protocol: Communicates via REST for metadata (JSON) and Binary Stream for media (HLS/HTTP-Range).

2. Session & Auth Integration
FastAPI Handshake: The app mimics the browser’s login behavior. It performs a POST request to the supervisor's frontend to establish a session.

Credential Persistence: Uses expo-secure-store to keep encrypted session tokens/cookies on the device, ensuring the user doesn't re-authenticate after every app kill.

Header Injection: Automatically attaches Authorization or Cookie headers to every file request to pass the server’s "Jail Security" checks.

3. Media Handling Engine
Streaming (expo-av): Utilizes the native Android/iOS media frameworks to handle "Range Requests." This allows seeking through large video files without downloading the entire file into the phone's RAM.

File System Discovery: Maps the JSON response from the server’s /api/list (or similar) into a scrollable FlatList UI.

Extension Filtering: Logic-gate on the client-side to differentiate between streamable content (mp4, mkv) and downloadable content (pdf, zip).

4. Jail Security Compliance
Path Validation: The app only requests relative paths provided by the server. It never attempts to "guess" paths, respecting the server's Obfuscation policy.

Error Handling: 404 responses from the server (due to jail blocks) are handled gracefully with "Access Denied" or "File Missing" UI states rather than crashing.

Execution Protocol
Initialize: Set BASE_URL in the client configuration to match the Server IP.

Handshake: Perform login to sync with storage/db/server.db via the FastAPI proxy.

Mount: Render the CUSTOM_SERVE_DIR contents onto the mobile view.

Stream: Invoke the Native Video Controller for media playback on Port 8000.

Comparison of Environments
Feature	Browser Setup (Current)	React Native Setup (Mobile)
Address	localhost:8000	192.168.x.x:8000
Video Engine	HTML5 <video>	expo-av (Native Android Driver)
Security	Standard Web CORS	Android Cleartext Policy + JWT/Cookie
Storage	Browser Cache	SecureStore (Hardware Encrypted)


app code : app.JSON
```javascript
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, Button, FlatList, TouchableOpacity, Alert, Modal, Image } from 'react-native';
import { Video } from 'expo-av';
import * as SecureStore from 'expo-secure-store';

// ================= CONFIGURATION =================
// REPLACE THIS with your Computer's Local Network IP (e.g., 192.168.1.15)
const SERVER_IP = '192.168.1.XX'; 
const BASE_URL = `http://${SERVER_IP}:8000`;

// Adjust these based on your actual FastAPI Routes
const API_ENDPOINTS = {
  LOGIN: `${BASE_URL}/api/login`,      // Check your server routes
  FILES: `${BASE_URL}/api/list`,       // The route that returns the file list
  STREAM: `${BASE_URL}/api/stream`,    // The route to stream files
};

export default function App() {
  const [token, setToken] = useState(null);
  const [currentScreen, setCurrentScreen] = useState('login'); // login, browser, player
  const [files, setFiles] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);

  // --- 1. AUTHENTICATION ---
  const handleLogin = async (username, password) => {
    try {
      console.log(`Attempting login to ${API_ENDPOINTS.LOGIN}...`);
      const response = await fetch(API_ENDPOINTS.LOGIN, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        // Assuming your server returns { token: "xyz" } or sets a cookie.
        // If it sets a cookie, React Native handles it automatically.
        // If it returns a token, we store it:
        const userToken = data.token || "session_active"; 
        
        setToken(userToken);
        setCurrentScreen('browser');
        fetchFiles(userToken);
      } else {
        Alert.alert("Login Failed", "Invalid credentials or server rejected handshake.");
      }
    } catch (error) {
      Alert.alert("Connection Error", "Is the server running on 0.0.0.0? \n" + error.message);
    }
  };

  // --- 2. FILE BROWSER ---
  const fetchFiles = async (authToken) => {
    try {
      // Pass token in header if your server requires it (Bearer Auth)
      const headers = authToken ? { 'Authorization': `Bearer ${authToken}` } : {};
      
      const response = await fetch(API_ENDPOINTS.FILES, { headers });
      const data = await response.json();
      
      // Adapt this if your server returns { files: [...] } instead of direct array
      setFiles(Array.isArray(data) ? data : data.files || []);
    } catch (error) {
      console.error(error);
      Alert.alert("Error", "Could not fetch file list.");
    }
  };

  const onFileSelect = (file) => {
    // Basic logic to check extension
    const isVideo = file.name.match(/\.(mp4|mkv|mov|avi)$/i);
    
    if (isVideo) {
      setSelectedVideo(file.name);
      setCurrentScreen('player');
    } else {
      Alert.alert("File Selected", `You selected ${file.name} (Not a supported video)`);
    }
  };

  // --- 3. RENDER COMPONENTS ---
  if (currentScreen === 'login') {
    return <LoginScreen onLogin={handleLogin} />;
  }

  if (currentScreen === 'player') {
    return (
      <VideoPlayer 
        fileName={selectedVideo} 
        serverUrl={BASE_URL}
        onClose={() => setCurrentScreen('browser')} 
        authToken={token}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>📂 Server Files</Text>
      <FlatList
        data={files}
        keyExtractor={(item) => item.name || item} // Adjust based on your JSON structure
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.fileItem} onPress={() => onFileSelect(item)}>
            <Text style={styles.fileText}>
              {item.name?.match(/\.(mp4|mkv)$/i) ? "🎬" : "📄"} {item.name || item}
            </Text>
          </TouchableOpacity>
        )}
      />
      <Button title="Logout" onPress={() => setCurrentScreen('login')} color="red" />
    </View>
  );
}

// --- SUB-COMPONENTS ---

const LoginScreen = ({ onLogin }) => {
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');

  return (
    <View style={styles.centerContainer}>
      <Text style={styles.title}>Architecture 2.0 Client</Text>
      <TextInput 
        placeholder="Username" 
        style={styles.input} 
        value={user} 
        onChangeText={setUser} 
        autoCapitalize="none"
      />
      <TextInput 
        placeholder="Password" 
        style={styles.input} 
        secureTextEntry 
        value={pass} 
        onChangeText={setPass} 
      />
      <Button title="Connect to Server" onPress={() => onLogin(user, pass)} />
    </View>
  );
};

const VideoPlayer = ({ fileName, serverUrl, onClose, authToken }) => {
  // We attach the token to the video request just in case the server needs it
  const videoSource = {
    uri: `${serverUrl}/api/stream/${encodeURIComponent(fileName)}`,
    headers: authToken ? { Authorization: `Bearer ${authToken}` } : {}
  };

  return (
    <View style={styles.blackContainer}>
      <Video
        source={videoSource}
        rate={1.0}
        volume={1.0}
        isMuted={false}
        resizeMode="contain"
        shouldPlay
        useNativeControls
        style={styles.video}
        onError={(e) => console.log("Video Error:", e)}
      />
      <Button title="Close Video" onPress={onClose} />
    </View>
  );
};

// --- STYLES ---
const styles = StyleSheet.create({
  container: { flex: 1, paddingTop: 50, paddingHorizontal: 20, backgroundColor: '#f4f4f4' },
  centerContainer: { flex: 1, justifyContent: 'center', padding: 20 },
  blackContainer: { flex: 1, backgroundColor: 'black', justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  header: { fontSize: 22, fontWeight: 'bold', marginBottom: 15 },
  input: { borderWidth: 1, borderColor: '#ccc', padding: 10, marginBottom: 15, borderRadius: 5, backgroundColor: 'white' },
  fileItem: { padding: 15, backgroundColor: 'white', borderBottomWidth: 1, borderColor: '#eee', flexDirection: 'row' },
  fileText: { fontSize: 16 },
  video: { width: '100%', height: 300, marginBottom: 20 },
});

```
