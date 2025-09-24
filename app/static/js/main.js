// Simple slider for About page
(function(){
  const sliders = document.querySelectorAll('[data-slider]');
  sliders.forEach(slider => {
    const track = slider.querySelector('[data-track]');
    const items = slider.querySelectorAll('[data-item]');
    const prev = slider.querySelector('[data-prev]');
    const next = slider.querySelector('[data-next]');
    let index = 0;
    function show(i){
      index = (i + items.length) % items.length;
      track.style.transform = `translateX(${-index * 100}%)`;
    }
    prev && prev.addEventListener('click', () => show(index-1));
    next && next.addEventListener('click', () => show(index+1));
    setInterval(()=>show(index+1), 6000);
  });
})();
// Contact destination preview
(function(){
  const select = document.getElementById('contact-destination');
  if (!select || !window.tripPreviewData) return;
  const img = document.getElementById('dest-preview-img');
  const title = document.getElementById('dest-preview-title');
  const name = document.getElementById('dest-preview-name');
  const desc = document.getElementById('dest-preview-desc');

  function update() {
    const slug = select.value;
    if (!slug || !window.tripPreviewData[slug]) {
      name.textContent = 'Not yet decided';
      desc.textContent = 'Choose a destination to preview its photo and description.';
      title.textContent = 'Destination Preview';
      img.src = 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1600&auto=format&fit=crop';
      return;
    }
    const t = window.tripPreviewData[slug];
    name.textContent = t.name || 'Destination';
    desc.textContent = t.desc || '';
    title.textContent = t.name || 'Destination';
    img.src = t.image || 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1600&auto=format&fit=crop';
  }

  select.addEventListener('change', update);
  update();
})();
