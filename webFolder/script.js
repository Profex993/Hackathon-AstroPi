const imageElement = document.getElementById('image');
const imageElement1 = document.getElementById('image1');
const aiElement = document.getElementById('ai');
const exifElement = document.getElementById('exif');
const timeElement = document.getElementById('time');

fetch('data.json')  // Path to your JSON file
  .then(response => response.json())
  .then(data => {
      console.log(data)
      // Get the image element by ID
    imageElement.src = "../" + data.img;
      imageElement1.src = "../" + data.img1;
      aiElement.innerText = data.ai;
      exifElement.innerText = data.exif;
      timeElement.innerText = data.sleep;
  })
  .catch(error => {
    console.error('Error fetching the JSON:', error);
  });
