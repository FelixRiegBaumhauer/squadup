var videoClient;
var activeRoom;
var previewMedia;
var identity;
var roomName;

// Check for WebRTC
if (!navigator.webkitGetUserMedia && !navigator.mozGetUserMedia) {
  alert('WebRTC is not available in your browser.');
}

function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){    	
               //pair[1] = pair[1].substring(3,pair[1].length - 3);
               return pair[1];
               }
       }
       
       return(false);
}

// When we are about to transition away from this page, disconnect
// from the room, if joined.
window.addEventListener('beforeunload', leaveRoomIfJoined);

$.getJSON('/token', function (data) {
  
  identity = data.identity;

  // Create a Video Client and connect to Twilio
  videoClient = new Twilio.Video.Client(data.token);
  document.getElementById('room-controls').style.display = 'block';
console.log('hi');
  // Bind button to join room
    roomName = getQueryVariable('name');
      log("Joining room '" + roomName + "'...");
    
        $.ajax('/addcall', {
                        data: { calling : roomName},
                        type: 'POST'
            });
        
        
      videoClient.connect({ to: roomName}).then(roomJoined,
        function(error) {
          log('Could not connect to Twilio: ' + error.message);
        });
     

  // Bind button to leave room
  document.getElementById('button-leave').onclick = function () {
    log('Leaving room...');
    activeRoom.disconnect();
  };
});

// Successfully connected!
function roomJoined(room) {
  activeRoom = room;

  log("Joined as '" + identity + "'");
  document.getElementById('button-join').style.display = 'none';
  document.getElementById('button-leave').style.display = 'inline';

  // Draw local video, if not already previewing
  if (!previewMedia) {
    room.localParticipant.media.attach('#local-media');
  }

  room.participants.forEach(function(participant) {
    log("Already in Room: '" + participant.identity + "'");
    participant.media.attach('#remote-media');
  });

  // When a participant joins, draw their video on screen
  room.on('participantConnected', function (participant) {
    log("Joining: '" + participant.identity + "'");
       $.ajax('/deleteCalls', {
            data: { calling : ""},
            type: 'POST'
     });
    participant.media.attach('#remote-media');
  });

  // When a participant disconnects, note in log
  room.on('participantDisconnected', function (participant) {
    log("Participant '" + participant.identity + "' left the room");
       $.ajax('/deleteCalls', {
            data: { calling : ""},
            type: 'POST'
     });
    participant.media.detach();
  });

  // When we are disconnected, stop capturing local video
  // Also remove media for all remote participants
  room.on('disconnected', function () {
    log('Left');
    $.ajax('/deleteCalls', {
            data: { calling : ""},
            type: 'POST'
     });
    log('testingtesting');
    room.localParticipant.media.detach();
    room.participants.forEach(function(participant) {
      participant.media.detach();
    });
    activeRoom = null;
    document.getElementById('button-join').style.display = 'inline';
    document.getElementById('button-leave').style.display = 'none';
    window.location.href ="/";
  });
}

//  Local video preview
document.getElementById('button-preview').onclick = function () {
  if (!previewMedia) {
    previewMedia = new Twilio.Video.LocalMedia();
    Twilio.Video.getUserMedia().then(
    function (mediaStream) {
      previewMedia.addStream(mediaStream);
      previewMedia.attach('#local-media');
    },
    function (error) {
      console.error('Unable to access local media', error);
      log('Unable to access Camera and Microphone');
    });
  };
};

// Activity log
function log(message) {
  var logDiv = document.getElementById('log');
  logDiv.innerHTML += '<p>&gt;&nbsp;' + message + '</p>';
  logDiv.scrollTop = logDiv.scrollHeight;
}

function leaveRoomIfJoined() {
  if (activeRoom) {
    activeRoom.disconnect();
  }
}