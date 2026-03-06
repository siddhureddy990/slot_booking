const slotsDiv = document.getElementById("slots");
const bookedDiv = document.getElementById("bookedSlots");

const API_URL = "http://localhost:5050";


function loadSlots(){

fetch(API_URL + "/get_slots")
.then(res => res.json())
.then(data => {

slotsDiv.innerHTML = "";

data.available_slots.forEach(slot => {

let btn = document.createElement("button");

btn.innerText = slot.slot_time;

btn.onclick = function(){

let name = prompt("Enter your name");

if(!name){
alert("Enter name");
return;
}

fetch(API_URL + "/book_slot",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
slot_id:slot.id,
name:name
})

})
.then(res=>res.json())
.then(response=>{

alert(response.msg);

loadSlots();
loadBookedSlots();

});

};

slotsDiv.appendChild(btn);

});

});

}



function loadBookedSlots(){

fetch(API_URL + "/booked_slots")
.then(res=>res.json())
.then(data=>{

bookedDiv.innerHTML = "";

data.booked_slots.forEach(slot=>{

let div = document.createElement("div");

div.className = "booked-item";

div.innerText = slot.slot_time + " - " + slot.booked_by;

bookedDiv.appendChild(div);

});

});

}



loadSlots();
loadBookedSlots();
