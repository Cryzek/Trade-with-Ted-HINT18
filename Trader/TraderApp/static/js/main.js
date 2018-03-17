if(!jQuery) {
    throw new Error("jQuery is required for the app to run.");
}

var NAVBAR_WIDTH = 280;

/* Global variables*/
var recognition,
    final_transcript = '',
    recognizing = false,
    ignore_onend,
    start_timestamp

var two_line = /\n\n/g,
    one_line = /\n/g,
    first_char = /\S/;  

/* Global DOM elements. Set after init*/
var $body,
    $header,
    $main,
    $sideNav,
    $voiceWidgetContainer,
    $startButton,
    $voiceText,
    $navToggleClose;

$(document).ready(init);

function init() {
    initElements();

    initMaterialize();

    loadPage();

    initMicrophone();

    initEvents();
}

function initElements() {
    $body = $("body");
    $header = $body.find("header");
    $main = $body.find("main");
    $sideNav = $body.find(".side-nav");
    $voiceWidgetContainer = $body.find("#voice-widget-container");
    
    $startButton = $voiceWidgetContainer.find("#voice-control-button-container button");
    
    $voiceText = $voiceWidgetContainer.find("#voice-text-container p");
    
    $navToggleClose = $sideNav.find("#nav-close");
};

function initMaterialize() {
    $("#nav-open").sideNav({
        menuWidth: NAVBAR_WIDTH,
        draggable: true
    });
};

function loadPage() {
    var $userStatsContainer = $main.find(".user-stats-container"),
        $statsAssetsDivider = $main.find(".stats-assets-divider"),
        $statsAssetsContainer = $main.find(".stats-assets-container");

    var arr = [$userStatsContainer, 
                $statsAssetsDivider, 
                $statsAssetsContainer,
                $voiceWidgetContainer];

    var tl = new TimelineMax();
    tl
    .to($body, 1, {
        opacity: 1
    })
    .staggerFromTo(arr, 0.75, {
        opacity: 0,
        y: 50
    }, {
        opacity: 1,
        y: 0
    }, 0.1);
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
};

function sendCommand(message) {
    console.log(message);
    if(!message) return;
    $.get("/api/decodeCommand", {text: message}, handleCommandDecode);
};

function handleCommandDecode(response) {
    var data = response;

    console.log(data);
    if(data.open) {
        plotGraph(data);
    }
};

function plotGraph(response) {

    Plotly.d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv', 
    function(err, rows){

        function unpack(rows, key) {
            return rows.map(function(row) { 
                return row[key]; 
            });
        }

        var $divForGraph = $("#div-for-graph");

        var trace = {
                x:['2018-03-17 00:50:00','2018-03-17 00:55:00'], 
                close: [43950.03,43991.96], 
                high: [43992.34,44022.23],  
                low: [41385.71,43949.58], 
                open:[ 41397.09,44016.17],
                // cutomise colors 
                increasing: {line: {color: 'black'}},
                decreasing: {line: {color: 'red'}},

                type: 'candlestick', 
                xaxis: 'x', 
                yaxis: 'y'
            };

        var data = [response];

        var layout = {
            dragmode: 'zoom', 
            showlegend: false, 
            xaxis: {
                autorange: true, 
                title: 'Date',
                rangeselector: {
                    x: 0,
                    y: 1.2,
                    xanchor: 'left',
                    font: {size:8},
                    buttons: [{
                        step: 'month',
                        stepmode: 'backward',
                        count: 1,
                        label: '1 month'
                    }, {
                            step: 'month',
                            stepmode: 'backward',
                            count: 6,
                            label: '6 months'
                    }, {
                            step: 'all',
                            label: 'All dates'
                    }]
                }
            }, 
            yaxis: {
                autorange: true, 
            }
        };

        Plotly.plot('div-for-graph', data, layout);
    });
};

function initEvents() {

    $navToggleClose.on("click", closeNavBar);

    $startButton.on("click", startRecording);
};

/* Functions used as event handlers*/
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
