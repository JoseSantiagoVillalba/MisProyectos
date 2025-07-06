const videoIds = [
  "AVC0YajmP4o",
  "jsTdReYp1gU",
  "BQrDPhEUsxY"
];

const container = document.querySelector('.video-container');

videoIds.forEach(id => {
  const iframe = document.createElement('iframe');
  iframe.width = "530";
  iframe.height = "300";
  iframe.src = `https://www.youtube.com/embed/${id}`;
  iframe.allowFullscreen = true;
  iframe.classList.add("video-frame");
  container.appendChild(iframe);
});