if(!jQuery) {
    throw new Error("jQuery is required for the app to run.");
}

/* Global variables*/
var recognition,
    final_transcript = '',
    recognizing = false,
    ignore_onend,
    start_timestamp;

var two_line = /\n\n/g,
    one_line = /\n/g,
    first_char = /\S/;  

/* Global DOM elements. Set after init*/
var $startButton,
    $voiceText,
    $navToggleClose;

$(document).ready(init);

function init() {
    initElements();

    initMaterialize();

    initMicrophone();

    initEvents();
}

function initElements() {
    $startButton = $("#voice-control-button-container button");
    $voiceText = $("#voice-text-container p");
    $navToggleClose = $("#nav-close");
}

function initMicrophone() {
    /**
     * Language codes -
     * en-US :- English US
     * en-IN :- English India
     * change at line "recognition.lang = ''"
    **/

    if (!('webkitSpeechRecognition' in window)) {
        upgrade();
    } else {
        showInfo("The microphone is available to use");
        $startButton.prop("disabled", false);

        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onstart = function() {
            recognizing = true;
            showInfo('Speak Now');
        };

        recognition.onerror = function(event) {
            if (event.error == 'no-speech') {
                showInfo('No speech input');
                ignore_onend = true;
            }
            if (event.error == 'audio-capture') {
                showInfo("Microphone is not available");
                ignore_onend = true;
            }
            if (event.error == 'not-allowed') {
                if (event.timeStamp - start_timestamp < 100) {
                    showInfo('Blocked');
                } else {
                    showInfo('Denied');
                }
                ignore_onend = true;
            }
        };    

        recognition.onend = function() {
            recognizing = false;
            if (ignore_onend) {
                return;
            }
            if (!final_transcript) {
                showInfo('Press the button to begin again');
                return;
            }
            showInfo('');
        };

        recognition.onresult = function(event) {
            var interim_transcript = '';
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    final_transcript += event.results[i][0].transcript;
                } else {
                    interim_transcript += event.results[i][0].transcript;
                }
            }
            final_transcript = capitalize(final_transcript);
            var transcript = linebreak(final_transcript) + linebreak(interim_transcript); 
            $voiceText.text(transcript);
        };
    }

    function upgrade() {
        $startButton.prop("disabled", true);
        console.error("webkitSpeechRecognition API not found.");
        showInfo('info_upgrade');
    }

    
    function linebreak(s) {
        return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
    }

    function capitalize(s) {
        return s.replace(first_char, function(m) { return m.toUpperCase(); });
    }

    function showInfo(s) {
        if (s) {
            Materialize.toast(s, 1000);
        }
    }
}

function sendCommand(message) {
    console.log(message);
    $.get("/api/decodeCommand", {text: message}, handleCommandDecode);
}

function handleCommandDecode(response) {
    console.log(response);
}

function initMaterialize() {
    $("#nav-open").sideNav({
        menuWidth: "300",
        draggable: true
    });
};

function initEvents() {

    $navToggleClose.on("click", closeNavBar);

    $startButton.on("click", startRecording);

};

function closeNavBar(event) {
    event.preventDefault();
    // $(this).sideNav("hide");
    $("#sidenav-overlay").trigger("click");    
}

function startRecording(event) {
    if (recognizing) {
        sendCommand(final_transcript);
        console.log(final_transcript);
        recognition.stop();
        $startButton.removeClass("recording");
        return;
    }

    $startButton.addClass("recording");
    final_transcript = '';
    recognition.lang = "en-US";
    recognition.start();
    ignore_onend = false;
    start_timestamp = event.timeStamp;
};