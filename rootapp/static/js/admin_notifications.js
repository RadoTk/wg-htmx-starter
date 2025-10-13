(function() {
  // Création de l'élément cloche
  const notificationBell = document.createElement('div');
  notificationBell.id = 'notification-bell';
  notificationBell.style.position = 'relative';
  notificationBell.style.cursor = 'pointer';
  notificationBell.style.marginLeft = '20px';

  // Icône cloche (SVG simple)
  notificationBell.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
      <path d="M8 16a2 2 0 0 0 1.985-1.75h-3.97A2 2 0 0 0 8 16zm.104-14.995a1 1 0 1 0-2.208 0 4.002 4.002 0 0 0-3.747 3.999c0 1.098-.404 2.02-1 2.684h11.7c-.596-.663-1-1.586-1-2.684a4.002 4.002 0 0 0-3.745-3.999z"/>
    </svg>
    <span id="notification-count" style="
      display:none;
      position:absolute;
      top:0;
      right:0;
      background:#ff0000;
      color:#fff;
      border-radius:50%;
      width:16px;
      height:16px;
      font-size:12px;
      text-align:center;
      line-height:16px;
      font-weight:bold;
      user-select:none;
    ">0</span>
  `;

  // On insère la cloche dans la barre d'admin (ex: après l'élément avec class .header__menu)
  const headerMenu = document.querySelector('.header__menu');
  if (headerMenu) {
    headerMenu.appendChild(notificationBell);
  }
})();
