//time is variable which represents current number of minutes since 12am
function currentperiod(time) {
    if (time < 480) {
        return 0;
    }
    else if (time < 525) {
        return 1;
    }
    else if (time < 571) {
        return 2;
    }
    else if (time < 680) {
        return 3;
    }
    else if (time < 666) {
        return 4;
    }
    else if (time < 712) {
        return 5;
    }
    else if (time < 758) {
        return 6;
    }
    else if (time < 804) {
        return 7;
    }
    else if (time < 849) {
        return 8;
    }
    else if (time < 894) {
        return 9;
    }
    else if (time < 935) {
        return 10;
    }
    else {
        return 0;
    }
    
}

var date = new Date();
var hours = date.getHours();
var minutes = date.getMinutes();

var sum_mins = (hours * 60) + minutes;
//console.log("hour is " + hours + "minutes is " + minutes);
console.log(currentperiod(sum_mins));



