// function education(imgSrc,educationLevel,year,percentage){
//     return `<tr>
//     <td rowspan="2">
//         <img class="image" src="${imgSrc}">
//     </td>
//     <td><p>${educationLevel}</p></td>
//     </tr>
//     <tr>
//         <td><p>${year}</p></td>
//     </tr>`
// }
setInterval(function(){
    today=new Date();
    date=today.getDate();
    month=today.getMonth();
    hours=today.getHours();
    mins=today.getMinutes();
    secs=today.getSeconds();
    if(date<10)
        date='0'+date;
    if(month+1<10)
        month='0'+(month+1);
    if(hours<10)
        hours='0'+hours;
    if(mins<10)
        mins='0'+mins;
    if(secs<10)
        secs='0'+secs;
    document.getElementById('time').innerHTML=`${date}-${month}-${today.getFullYear()} ${hours}:${mins}:${secs}`;
},1000);