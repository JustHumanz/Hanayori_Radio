const wall = [
    "static/img/wall2.jpg",
    "static/img/wall3.jpg",
    "static/img/wall4.jpg"
  ]
  
  const node = document.getElementById("image-head");
  
  const cycleImages = (images, container, step) => {
      images.forEach((image, index) => (
        setTimeout(() => {
          container.style.backgroundImage = `url(${image})`  
      }, step * (index + 1))
    ))
    setTimeout(() => cycleImages(images, container, step), step * images.length)
  }
  
  cycleImages(wall, node, 1000)