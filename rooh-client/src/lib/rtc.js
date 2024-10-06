import { sdpFilterCodec } from "$lib/utils.js";

export let pc = null;

async function negotiate(workout) {
  try {
    const offer = await pc.createOffer({ iceGatheringTimeout: 1000000000 });
    await pc.setLocalDescription(offer);

    const localDescription = pc.localDescription;
    localDescription.sdp = sdpFilterCodec(
      "video",
      "H264",
      localDescription.sdp
    );

    // Send offer to the server
    const response = await fetch("http://127.0.0.1:8080/offer", {
      body: JSON.stringify({
        sdp: localDescription.sdp,
        type: localDescription.type,
        workout,
      }),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
    });

    // Parse the server's response
    const answer = await response.json();

    // Set the remote description
    await pc.setRemoteDescription(answer);
  } catch (e) {
    console.log(e);
  }
}

async function initializeRTCConnection(workout) {
  pc = new RTCPeerConnection({
    iceServers: [{ urls: ["stun:stun.l.google.com:19302"] }],
  });

  console.log("RTC connection established");

  pc.addEventListener("track", (evt) => {
    console.log(evt);
    document.getElementById("video").srcObject = evt.streams[0];
    console.log("Videostream sent");
  });

  // Acquire media and start negociation.
  await navigator.mediaDevices.getUserMedia({ video: true }).then(
    (stream) => {
      stream.getTracks().forEach((track) => {
        pc.addTrack(track, stream);
      });
      negotiate(workout);
    },
    (err) => {
      console.log("Could not acquire media: " + err);
    }
  );
}

function cleanupConnection() {
  if (pc) {
    // close transceivers
    if (pc.getTransceivers) {
      pc.getTransceivers().forEach((transceiver) => {
        if (transceiver.stop) {
          transceiver.stop();
        }
      });
    }

    // close local audio / video
    pc.getSenders().forEach((sender) => {
      sender.track.stop();
    });

    if (pc) {
      pc.close();
      pc = null;
    }
  }
}

function initializeConnection(store, workout) {
  const socket = new WebSocket("ws://127.0.0.1:8080/ws");

  socket.onopen = () => {
    console.log("WebSocket connection established.");
    socket.send("2init");
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed.");
  };

  socket.onmessage = (e) => {
    if (e.data === "init") {
      initializeRTCConnection(workout);
    } else {
      let data = JSON.parse(e.data);
      for (let obj in store) {
        try {
          store[obj].set(data[obj]);
        } catch (err) {
          console.log("Error updating store:", err);
        }
      }
    }
  };
}

export { initializeConnection, cleanupConnection };
