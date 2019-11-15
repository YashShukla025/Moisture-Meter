  var config = {
    apiKey: "AIzaSyDQiFJGXzQqfV3a7-JnrkyhyZngBKqF9Vw",
    authDomain: "raspberrypi-4fd97.firebaseapp.com",
    databaseURL: "https://raspberrypi-4fd97.firebaseio.com/",
    projectId: "raspberrypi-4fd97",
    storageBucket: "raspberrypi-4fd97.appspot.com",
    messagingSenderId: "1009679351463"
  };
  firebase.initializeApp(config);
// Reference messages collection
var messagesRef = firebase.database().ref('sensor/dht22');
function ui(){
messagesRef.on('value',gotData,errData);
}
function gotData(data){
//console.log(data.val());
var msg =data.val();
var keys=Object.keys(msg);
var tab1="<table><tr><th>Humidity</th><th>Moisture Sensor 1</th><th>Moisture Sensor 2</th><th>Moisture Sensor 3</th><th>Temperature</th><th>Time</th><tr>";
for (var i = 0; i < keys.length; i++) {
  var k =keys[i];
  var now = msg[k].now;
    var humidity = msg[k].humidity;
    var temp = msg[k].temp;
    var s1 = msg[k].s1;
    var s2 = msg[k].s2;
    var s3 = msg[k].s3;

    
    tab1+="<td>"+humidity+"</td>"+"<td>"+s1+"</td>"+"<td>"+s2+"</td>"+"<td>"+s3+"</td>"+"<td>"+temp+"</td>"+"<td>"+now+"</td>"+"</tr>";
}

    document.getElementById("demo").innerHTML=tab1;
}
function errData(data){
console.log('Error');
console.log(err); 
}
