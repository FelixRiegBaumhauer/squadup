 $(document).ready(function() {
    var round = 1;
    var points = 0;
    var roundScore = 0;
    var totalScore = 0;
    ranOut = false;
    var distance;

    svinitialize();
    mminitialize();

    // Init Timer
    resetTimer();

  function timer() {
      count = count-1;
      if (count <= 0) {
        console.log('finished');
        if (round < 5){
          endRound();
        } else if (round >= 5){
          endGame();
        };
        clearInterval(counter);
      }
      $("#timer").html(count);
    };

    // Guess Button
    $('#guessButton').click(function (){
      doGuess();
      rminitialize();
    });

    // End of round continue button click
    $('#roundEnd').on('click', '.closeBtn', function () {
      $('#roundEnd').fadeOut(500);

      // Reload maps to refresh coords
      svinitialize();
      mminitialize();
      rminitialize();

      // Reset Timer
      resetTimer();
    });

    // End of game 'play again' button click
    $('#endGame').on('click', '.playAgain', function () {
      window.location.reload();
    });

    //
    // Functions
    //

    // Reset Timer
    function resetTimer(){
      count = 15;
      counter = setInterval(timer, 1000);
    }

    // Calculate distance between points function
    function calcDistance(fromLat, fromLng, toLat, toLng) {
      return google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(fromLat, fromLng), new google.maps.LatLng(toLat, toLng));
    };

    function doGuess(){
      if (ranOut == false){

        // Stop Counter
        clearInterval(counter);

        // Reset marker function
        function resetMarker() {
            //Reset marker
            if (guessMarker != null) {
                guessMarker.setMap(null);
            }
        };

        // Explode latLng variables into separate variables for calcDistance function
        locLatLongs = window.locLL.toString();
        guessLatLongs = window.guessLatLng.toString();

        // Make arrays and clean from (){} characters
        window.locArray = locLatLongs.replace(/[\])}[{(]/g,'').split(',');
        window.guessArray = guessLatLongs.replace(/[\])}[{(]/g,'').split(',');

        // Calculate distance between points, and convert to kilometers
        distance = Math.ceil(calcDistance(window.locArray[0], window.locArray[1], window.guessArray[0], window.guessArray[1]) / 1000);

        // Calculate points awarded via guess proximity
        function inRange(x, min, max) {
            return (min <= x && x <= max);
        };

        // Real basic point thresholds depending on kilometer distances
        if(inRange(distance, 0.1, 0.5)) {
          points = 50;
        }
         else if(inRange(distance, 0.51, 1.5)) {
          points = 30;
        } else if(inRange(distance, 1.5, 5.00)) {
          points = 20;
        } else if(inRange(distance, 5.01, 8.00)) {
          points = 10;
        } else if(inRange(distance, 8.01, 13.00)) {
          points = 5;
        } else {
          points = 0;
        };

        if (round < 5){

          endRound();
        } else if (round >= 5){
          endGame();
        };

      } else {

        // They ran out

      }

      timer();
      window.guessLatLng = '';

    };

    function endRound(){
      round++
      if(ranOut==true){
        roundScore = 0;
      } else {
        roundScore = points;
        totalScore = totalScore + points;
      }

      $('.round').html('Current Round: <b>'+round+'/5</b>');
      $('.roundScore').html('Last Round Score: <b>'+roundScore+'</b>');
      $('.totalScore').html('Total Score: <b>'+totalScore+'</b>');

      // If distance is undefined, that means they ran out of time and didn't click the guess button
      if(typeof distance === 'undefined' || ranOut == true){
        $('#roundEnd').html('<p> You took too long!.<br/> You didn\'t score any points this round!<br/><br/><button class="btn btn-primary closeBtn" type="button">Continue</button></p></p>');
        $('#roundEnd').fadeIn();

        // Stop Counter
        clearInterval(counter);

        // Reset marker function
        function resetMarker() {
            //Reset marker
            if (guessMarker != null) {
                guessMarker.setMap(null);
            }
        };

        window.guessLatLng = '';
        ranOut = false;

        points = 0;

      } else {
        $('#roundEnd').html('<p>Your guess was<br/><strong><h1>'+distance+'</strong>km</h1> away from the actual location.<br/><div id="roundMap"></div><br/> You have scored<br/><h1>'+roundScore+' points</h1> this round!<br/><br/><button class="btn btn-primary closeBtn" type="button">Continue</button></p></p>');
        $('#roundEnd').fadeIn();
      };

      // Reset Params
      window.guessLatLng = '';
      ranOut = false;

    };

    function endGame(){

      roundScore = points;
      totalScore = totalScore + points;

      $('#miniMap, #pano, #guessButton, #scoreBoard').hide();
      $('#endGame').html('<h1>Congrats!</h1><h2>Your final score was:</h2><h1>'+totalScore+'!</h1><br/><button class="btn btn-large btn-success playAgain" type="button">Play Again?</button><br><br><a href="/">End Game </a>' );
      $('#endGame').fadeIn(500);

      rminitialize();

      // We're done with the game
      window.finished = true;
    }


  });
