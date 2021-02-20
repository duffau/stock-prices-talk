const arrayCarousel = ['https://www.fillmurray.com/g/200/200', 
'https://www.fillmurray.com/200/200', 
'https://www.fillmurray.com/g/200/200', 
'https://www.fillmurray.com/200/100'];

counter = 0
const setImage = () => {
 document.getElementById("carousel-image").src = arrayCarousel[counter];
 counter = (counter+1)  % arrayCarousel.length;
}

setInterval(setImage, 1000);