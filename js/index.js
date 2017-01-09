//time is variable which represents current number of minutes since 12am
function currentperiod(time) {
    if (time < 480) {
        return "Before school";
    }
    else if (time < 525) {
        return "its first period";
    }
    else if (time < 571) {
        return "its second period";
    }
    else if (time < 680) {
        return "its third period";
    }
    else if (time < 666) {
        return "its 4th period";
    }
    else if (time < 712) {
        return "its 5th period";
    }
    else if (time < 758) {
        return "its 6th period";
    }
    else if (time < 804) {
        return "its 7th period";
    }
    else if (time < 849) {
        return "its 8th period";
    }
    else if (time < 894) {
        return "its 9th period";
    }
    else if (time < 935) {
        return "its 10th period";
    }
    else {
        return "its afterschool";
    }
    
}

var date = new Date();
var hours = date.getHours();
var minutes = date.getMinutes();

var sum_mins = (hours * 60) + minutes;
//console.log("hour is " + hours + "minutes is " + minutes);
console.log(currentperiod(sum_mins));



