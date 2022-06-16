var SpeechRecognition = window.webkitSpeechRecognition;
  
var recognition = new SpeechRecognition();

var Textbox = $('#textbox');
var instructions = $('#instructions');

var Content = '';

recognition.continuous = true;

recognition.onresult = function(event) {

  var current = event.resultIndex;

  var transcript = event.results[current][0].transcript;
    // pass the transcript to server with ajax
   
        $.ajax({
          type: 'GET',
          url: "/post_message/" + transcript,
          success: function (response) {
           console.log(response)
          },
        });
    Content += transcript;
    Textbox.val(Content);
  
};

recognition.onspeechend = function() {
  console.log("WORKING");

  recognition.abort();
  instructions.text('No activity.');
}

recognition.onstart = function() { 
  console.log("STARTED");
  instructions.text('Voice recognition is ON.');
}


recognition.onerror = function(event) {
  console.log(event.error)
  if(event.error == 'no-speech') {
    instructions.text('Try again.');  
  }
}

$('#start-btn').on('click', function(e) {
  if (Content.length) {
    Content += ' ';
  }
  recognition.start();
});

Textbox.on('input', function() {
  Content = $(this).val();
})